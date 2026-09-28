"""Keyword/category retrieval for DAVIET knowledge (V1).

Designed to be replaceable with embeddings later without changing ChatService.
Includes smart alias expansions, conversational context awareness, and typo tolerances.
"""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from typing import List, Sequence, Tuple

from app.core.logging import get_logger
from app.models.knowledge import KnowledgeItem
from app.repositories.knowledge_repository import KnowledgeRepository

logger = get_logger(__name__)

# Lightweight stopwords — keep domain terms intact
_STOPWORDS = {
    "a",
    "an",
    "the",
    "is",
    "are",
    "was",
    "were",
    "what",
    "which",
    "who",
    "whom",
    "where",
    "when",
    "how",
    "do",
    "does",
    "did",
    "can",
    "could",
    "would",
    "should",
    "i",
    "me",
    "my",
    "we",
    "our",
    "you",
    "your",
    "please",
    "tell",
    "give",
    "about",
    "of",
    "in",
    "on",
    "at",
    "to",
    "for",
    "and",
    "or",
    "with",
    "from",
    "info",
    "information",
}

# Extensive alias map covering typos, shorthands, abbreviations, and informal speech
_ALIAS_MAP = {
    "tpo": "training placement office",
    "placement cell": "training placement",
    "placements": "placement training package company",
    "ug blok": "core block undergraduate cse ece electrical infrastructure",
    "ug block": "core block undergraduate cse ece electrical infrastructure",
    "core blok": "core block undergraduate infrastructure",
    "rd blok": "r&d block research principal infrastructure",
    "audi": "auditorium lala chanchal dass infrastructure",
    "auditoriom": "auditorium lala chanchal dass infrastructure",
    "auditoriam": "auditorium lala chanchal dass infrastructure",
    "library timing": "library timings knowledge centre hours",
    "library time": "library timings knowledge centre hours",
    "librari": "library central knowledge centre books",
    "lib": "library central knowledge centre",
    "college address": "address contact jalandhar punjab location",
    "phone number": "contact phone numbers office administration",
    "helpline": "toll free contact administration",
    "course fee": "btech fee tuition fee ptu fees semester cost",
    "fee struct": "btech fee tuition ptu fee structure semester",
    "fee structure": "btech fee tuition ptu fee structure semester",
    "fees structure": "btech fee tuition ptu fee structure semester",
    "btech fee": "btech fee tuition semester fee ptu",
    "tuition fee": "tuition fee btech semester ptu",
    "fees": "fee tuition ptu cost semester structure",
    "fee": "fees tuition ptu cost semester structure",
    "ptu": "punjab technical university affiliation ikg",
    "ikgptu": "punjab technical university affiliation ikg",
    "cse": "computer science engineering department program",
    "ece": "electronics communication engineering department program",
    "mech": "mechanical engineering department workshop",
    "civil": "civil engineering department",
    "ee": "electrical engineering department",
    "hostel": "hostel accommodation sutlej raavi beas rooms mess",
    "hostels": "hostel accommodation sutlej raavi beas rooms mess",
    "canteen": "canteen food cafeteria tuck shop infrastructure",
    "principal": "principal office administration leadership r&d block",
    "college is open": "college working hours operating schedule academic timings",
    "is college open": "college working hours operating schedule academic timings",
    "open rn": "college working hours operating schedule academic timings currently",
    "open now": "college working hours operating schedule academic timings currently",
    "working hours": "college working hours operating schedule academic timings",
    "college timings": "college working hours operating schedule academic timings",
    "timings": "college working hours operating schedule library timings",
    "timing": "college working hours operating schedule library timings",
    "rn": "currently right now today schedule hours",
    "calendar": "academic calendar ptu ikgptu schedule semester session",
    "calander": "academic calendar ptu ikgptu schedule semester session",
    "academic calendar": "academic calendar ptu ikgptu schedule semester session",
    "acedmic calendar": "academic calendar ptu ikgptu schedule semester session",
    "acedmic calander": "academic calendar ptu ikgptu schedule semester session",
    "ptu calendar": "ikg-ptu academic calendar odd even semester session",
    "ikgptu calendar": "ikg-ptu academic calendar odd even semester session",
}


@dataclass
class ScoredKnowledgeItem:
    item: KnowledgeItem
    score: float


class RetrievalService:
    """Keyword & contextual retrieval with typo tolerance and campus domain expansions."""

    def __init__(
        self,
        repository: KnowledgeRepository | None = None,
        dynamic_items: Sequence[KnowledgeItem] | None = None,
    ) -> None:
        self._repo = repository or KnowledgeRepository()
        self._dynamic_items = list(dynamic_items or [])

    def register_dynamic_items(self, items: Sequence[KnowledgeItem]) -> None:
        self._dynamic_items.extend(items)

    def retrieve(
        self,
        query: str,
        *,
        limit: int = 4,
        min_score: float = 2.0,
        conversation: Sequence[Tuple[str, str]] | None = None,
    ) -> List[KnowledgeItem]:
        """Return ranked knowledge items relevant to the query.
        
        Incorporates recent conversational context to handle follow-up queries smoothly.
        """
        # If query is very brief (e.g. "and library?", "auditorium", "hostel?"),
        # combine key tokens from previous turns for contextual continuity
        effective_query = query
        if conversation and len(query.strip().split()) <= 3:
            last_user_turns = " ".join([u for u, _ in conversation[-2:]])
            effective_query = f"{query} {last_user_turns}"

        normalized = self._normalize_query(effective_query)
        if not normalized:
            return []

        tokens = self._tokenize(normalized)
        if not tokens:
            return []

        pool = list(self._repo.list_all()) + self._dynamic_items
        seen_keys = set()
        deduped_pool: List[KnowledgeItem] = []
        for item in pool:
            key = (item.title.strip().lower(), item.category.strip().lower())
            if key not in seen_keys:
                seen_keys.add(key)
                deduped_pool.append(item)

        scored: List[ScoredKnowledgeItem] = []
        for item in deduped_pool:
            score = self._score(item, normalized, tokens)
            if score >= min_score:
                scored.append(ScoredKnowledgeItem(item=item, score=score))

        scored.sort(key=lambda s: s.score, reverse=True)
        results = [s.item for s in scored[:limit]]

        logger.info(
            "Retrieval query_tokens=%s matches=%s top_score=%s",
            tokens[:12],
            len(results),
            scored[0].score if scored else 0,
        )
        return results

    def _normalize_query(self, query: str) -> str:
        text = (query or "").lower().strip()
        # Clean special characters first
        text = re.sub(r"[^a-z0-9\s&+.-]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        # Direct & Fuzzy Alias Matching
        words = text.split()
        expanded_parts = []
        skip_indices = set()

        # Two-word alias check (e.g. "ug blok", "fee struct")
        for i in range(len(words) - 1):
            pair = f"{words[i]} {words[i+1]}"
            if pair in _ALIAS_MAP:
                expanded_parts.append(_ALIAS_MAP[pair])
                skip_indices.add(i)
                skip_indices.add(i + 1)

        for i, word in enumerate(words):
            if i in skip_indices:
                continue
            if word in _ALIAS_MAP:
                expanded_parts.append(_ALIAS_MAP[word])
            else:
                # Fuzzy match for typos in single words (e.g. "blok" -> "block")
                matched_alias = None
                for alias_key, replacement in _ALIAS_MAP.items():
                    if len(word) >= 4 and len(alias_key) >= 4 and " " not in alias_key:
                        sim = difflib.SequenceMatcher(None, word, alias_key).ratio()
                        if sim >= 0.82:
                            matched_alias = replacement
                            break
                if matched_alias:
                    expanded_parts.append(matched_alias)
                else:
                    expanded_parts.append(word)

        combined = " ".join(expanded_parts)
        return re.sub(r"\s+", " ", combined).strip()

    def _tokenize(self, text: str) -> List[str]:
        tokens = [t for t in text.split() if t and t not in _STOPWORDS and len(t) > 1]
        extras = [t for t in text.split() if t in {"ai", "ml", "tpo", "cse", "ece", "mba", "mca", "ptu", "fee", "fees", "ug", "rd"}]
        return list(dict.fromkeys(tokens + extras))

    def _score(self, item: KnowledgeItem, query: str, tokens: Sequence[str]) -> float:
        score = 0.0
        title = item.title.lower()
        category = item.category.lower()
        keywords = {k.lower() for k in item.keywords}
        content = item.content.lower()
        haystack = item.searchable_text()

        # Multi-word keyword matches
        for keyword in keywords:
            if len(keyword) >= 3 and keyword in query:
                score += 4.5

        if category.replace("_", " ") in query or category in query:
            score += 3.5

        if title in query:
            score += 6.0

        for token in tokens:
            if token in keywords:
                score += 3.5
            if token in title.split():
                score += 3.0
            if token == category or token in category.replace("_", " ").split():
                score += 2.5
            if token in content:
                score += 0.8
            # Substring / partial hit
            for keyword in keywords:
                if token in keyword or keyword in token:
                    score += 1.2
                    break

        strong = any(
            [
                any(token in keywords for token in tokens),
                any(token in title for token in tokens),
                any(token in category.replace("_", " ") for token in tokens),
                any(len(k) >= 3 and k in query for k in keywords),
            ]
        )
        if not strong and score < 3.5:
            return 0.0

        present = sum(1 for token in tokens if token in haystack)
        if tokens:
            coverage = present / len(tokens)
            if coverage >= 0.4:
                score += coverage * 2.0

        return score

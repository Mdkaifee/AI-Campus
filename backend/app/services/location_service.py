"""Campus location service for location assistance, navigation, and Google Maps mapping."""

from __future__ import annotations

import difflib
import re
from typing import Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.location import CampusLocation

logger = get_logger(__name__)

# Core DAVIET Campus Destination Directory with comprehensive aliases, abbreviations & typo keywords
DEFAULT_CAMPUS_LOCATIONS: List[CampusLocation] = [
    CampusLocation(
        id="central-library",
        name="Central Library (Knowledge Centre)",
        aliases=[
            "library", "central library", "reading room", "knowledge centre library",
            "books", "lib", "librari", "knowledge centre", "study room"
        ],
        block="Knowledge Centre",
        floor="Ground & 1st Floor",
        description="Located inside the Knowledge Centre, adjacent to the campus bank/ATM and directly opposite Lala Chanchal Dass Auditorium.",
        latitude=31.3486,
        longitude=75.5789,
    ),
    CampusLocation(
        id="tpo-office",
        name="Training and Placement Office (TPO)",
        aliases=[
            "tpo", "placement office", "placement cell", "training and placement",
            "placement", "tpo cell", "placements", "placements cell"
        ],
        block="R & D Block",
        floor="1st Floor",
        description="Located in the R&D Block near the Convention Hall corridor, adjacent to the Principal's administrative wing.",
        latitude=31.3484,
        longitude=75.5786,
    ),
    CampusLocation(
        id="auditorium",
        name="Lala Chanchal Dass DAVIET Auditorium",
        aliases=[
            "auditorium", "chanchal dass", "main hall", "audi", "auditoriam",
            "auditoriom", "college audi", "open audi", "indoor auditorium"
        ],
        block="Auditorium Complex",
        floor="Ground Floor",
        description="Centrally air-conditioned 1200-seat auditorium situated right at the front entrance of the campus, opposite Knowledge Centre.",
        latitude=31.3488,
        longitude=75.5792,
    ),
    CampusLocation(
        id="rd-block",
        name="R & D Block (Research & Administration)",
        aliases=[
            "r&d block", "rd block", "research block", "principal office",
            "admin office", "accounts office", "r and d block", "r&d", "rd"
        ],
        block="R & D Block",
        floor="Ground & 1st Floor",
        description="Houses the Principal's Office, Accounts and Administrative Wings, Robotics and Nano-technology labs, and Convention Hall.",
        latitude=31.3484,
        longitude=75.5785,
    ),
    CampusLocation(
        id="core-block",
        name="Core Block (Engineering & Applied Sciences)",
        aliases=[
            "core block", "ug block", "ug blok", "undergraduate block",
            "cse department", "ece department", "electrical department",
            "computer centre", "core blok", "ug", "btech block", "b.tech block"
        ],
        block="Core Block",
        floor="Ground to 3rd Floor",
        description="Primary academic block accommodating the Computer Science (CSE), Electronics (ECE), Electrical Engineering departments, and the Central Computer Centre.",
        latitude=31.3483,
        longitude=75.5780,
    ),
    CampusLocation(
        id="material-science-block",
        name="Material Science Block (Workshops & Labs)",
        aliases=[
            "workshop", "workshops", "mechanical workshop", "material science",
            "metrology lab", "carpentry", "fitting shop", "welding shop",
            "foundry shop", "civil lab", "workshop block"
        ],
        block="Material Science Block",
        floor="Ground Floor",
        description="Houses central engineering workshops, machine tools, carpentry, fitting, foundry, and the specialized Mitutoyo Metrology Lab.",
        latitude=31.3479,
        longitude=75.5775,
    ),
    CampusLocation(
        id="sutlej-hostel",
        name="Sutlej Boys Hostel",
        aliases=[
            "sutlej hostel", "sutlej", "boys hostel", "boys mess",
            "sutlej block", "boys accommodation"
        ],
        block="Boys Hostel Complex",
        floor="Multiple Floors (Lift available)",
        description="On-campus boys hostel accommodation with attached dining mess, indoor sports room, and 24/7 power backup.",
        latitude=31.3475,
        longitude=75.5770,
    ),
    CampusLocation(
        id="raavi-hostel",
        name="Raavi Girls Hostel",
        aliases=[
            "raavi hostel", "raavi", "girls hostel", "girls mess",
            "raavi block", "girls accommodation"
        ],
        block="Girls Hostel Complex",
        floor="Multiple Floors",
        description="Secure on-campus girls hostel accommodation with round-the-clock security, attached dining mess, and recreation rooms.",
        latitude=31.3478,
        longitude=75.5795,
    ),
    CampusLocation(
        id="beas-hostel",
        name="Beas Hostel",
        aliases=[
            "beas hostel", "beas", "beas block"
        ],
        block="Hostel Complex",
        floor="Multiple Floors",
        description="Boys hostel wing within the residential campus perimeter.",
        latitude=31.3474,
        longitude=75.5772,
    ),
    CampusLocation(
        id="canteen",
        name="Campus Canteen & Cafeteria",
        aliases=[
            "canteen", "cafeteria", "food court", "tuck shop",
            "cafe", "mess", "nescafe", "canteen food"
        ],
        block="Central Campus Area",
        floor="Ground Floor",
        description="Vibrant student food court and tuck shop serving fresh meals, snacks, beverages, and daily necessities.",
        latitude=31.3482,
        longitude=75.5782,
    ),
]


class LocationService:
    """Detects location intent and matches destinations for navigation assistance."""

    def __init__(self, db: Optional[AsyncIOMotorDatabase] = None) -> None:
        self._db = db
        self._memory_locations: Dict[str, CampusLocation] = {
            loc.id: loc for loc in DEFAULT_CAMPUS_LOCATIONS
        }

    def bind(self, db: AsyncIOMotorDatabase) -> None:
        self._db = db

    async def sync_locations_to_mongo(self) -> int:
        """Seed default verified campus locations into MongoDB if empty."""
        if self._db is None:
            return 0
        try:
            collection = self._db["campus_locations"]
            synced = 0
            for loc in DEFAULT_CAMPUS_LOCATIONS:
                doc = loc.to_dict()
                await collection.update_one(
                    {"id": doc["id"]},
                    {"$set": doc},
                    upsert=True,
                )
                synced += 1
            logger.info("Synced %d campus locations to MongoDB campus_locations", synced)
            return synced
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to sync campus locations to MongoDB: %s", type(exc).__name__)
            return 0

    def match_location(
        self,
        message: str,
        conversation_context: Optional[List[tuple[str, str]]] = None,
    ) -> Optional[CampusLocation]:
        """Detect if message is seeking a campus destination or location.
        
        Supports fuzzy typo matching (e.g. 'ug blok' -> Core Block) and conversational follow-ups.
        """
        raw_text = (message or "").strip().lower()
        if not raw_text:
            return None

        # Clean punctuation except alphanumeric and spaces
        cleaned = re.sub(r"[^a-z0-9\s]", " ", raw_text)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        words = cleaned.split()

        # Check if previous context was location-focused
        was_location_context = False
        if conversation_context:
            last_turns = " ".join([f"{u} {a}" for u, a in conversation_context[-2:]]).lower()
            location_hints = ("where is", "location", "navigate", "directions", "floor", "block", "maps")
            was_location_context = any(h in last_turns for h in location_hints)

        # Direct Location Intent Keywords
        location_keywords = [
            "where", "location", "locate", "directions", "direction", "map", "maps",
            "how to reach", "navigate", "navigation", "which block", "which floor",
            "block", "blok", "floor", "way to", "find", "place", "building", "reach",
            "situated", "situated at"
        ]
        has_intent = any(kw in raw_text for kw in location_keywords) or was_location_context

        # Check exact and fuzzy match against each location
        best_match: Optional[CampusLocation] = None
        highest_score = 0.0

        for loc in self._memory_locations.values():
            score = 0.0

            # 1. Exact Name match in text
            if loc.name.lower() in raw_text:
                score += 12.0

            # 2. Check each alias
            for alias in loc.aliases:
                alias_lower = alias.lower()
                # Whole word match regex
                pattern = r"\b" + re.escape(alias_lower) + r"\b"
                if re.search(pattern, cleaned):
                    score += 10.0
                elif alias_lower in cleaned:
                    score += 6.0
                else:
                    # Fuzzy match on phrases/tokens to catch typos like 'ug blok', 'librari', 'audi'
                    # Test sequence similarity against full cleaned input or sliding n-grams
                    alias_words_count = len(alias_lower.split())
                    if len(words) >= alias_words_count:
                        for i in range(len(words) - alias_words_count + 1):
                            ngram = " ".join(words[i : i + alias_words_count])
                            ratio = difflib.SequenceMatcher(None, alias_lower, ngram).ratio()
                            if ratio >= 0.85:
                                score = max(score, ratio * 9.0)
                            elif ratio >= 0.75 and has_intent:
                                score = max(score, ratio * 7.0)

            # Check individual fuzzy token match for single words (e.g. 'canteen', 'audi', 'blok')
            for token in words:
                for alias in loc.aliases:
                    if len(token) >= 4 and len(alias) >= 4:
                        ratio = difflib.SequenceMatcher(None, token, alias).ratio()
                        if ratio >= 0.88:
                            score = max(score, ratio * 8.0)

            if score > highest_score:
                highest_score = score
                best_match = loc

        # Thresholds:
        # If strong alias / name hit (score >= 7.0) or (has_intent and score >= 4.5)
        # Even if user just types "tpo" or "audi" without 'where is', score is >= 8.0
        if best_match and (highest_score >= 7.0 or (has_intent and highest_score >= 4.5)):
            logger.info("Matched location destination: %s (score=%.2f)", best_match.name, highest_score)
            return best_match

        return None

"""Knowledge-base domain models."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class KnowledgeItem:
    title: str
    category: str
    content: str
    source_url: str
    updated_at: str
    keywords: List[str] = field(default_factory=list)
    id: Optional[str] = None

    def searchable_text(self) -> str:
        parts = [
            self.title,
            self.category,
            self.content,
            " ".join(self.keywords),
        ]
        return " ".join(parts).lower()

    def to_dict(self) -> dict:
        return {
            "id": self.id or f"{self.category}-{abs(hash(self.title)) % 10000}",
            "title": self.title,
            "category": self.category,
            "content": self.content,
            "source_url": self.source_url,
            "updated_at": self.updated_at,
            "keywords": self.keywords,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "KnowledgeItem":
        return cls(
            id=str(data.get("id") or data.get("_id") or ""),
            title=str(data.get("title", "")).strip(),
            category=str(data.get("category", "")).strip(),
            content=str(data.get("content", "")).strip(),
            source_url=str(data.get("source_url", "")).strip(),
            updated_at=str(data.get("updated_at", "")).strip(),
            keywords=[
                str(k).strip().lower()
                for k in (data.get("keywords") or [])
                if str(k).strip()
            ],
        )

"""Chat history domain models."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class ChatSource:
    title: str
    url: str
    category: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"title": self.title, "url": self.url}
        if self.category:
            payload["category"] = self.category
        if self.updated_at:
            payload["updated_at"] = self.updated_at
        return payload


@dataclass
class ChatTurn:
    session_id: str
    user_message: str
    assistant_message: str
    sources: List[ChatSource] = field(default_factory=list)
    location: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=utc_now)
    provider: Optional[str] = None
    model: Optional[str] = None

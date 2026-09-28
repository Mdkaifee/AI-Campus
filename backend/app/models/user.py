"""User domain model for authentication."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class User:
    id: str
    name: str
    email: str
    hashed_password: str
    salt: str
    created_at: datetime = field(default_factory=utc_now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "salt": self.salt,
            "created_at": self.created_at,
        }

"""Persist chat turns in MongoDB without storing extra personal data."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.chat import ChatSource, ChatTurn

logger = get_logger(__name__)


class ChatRepository:
    def __init__(self, db: Optional[AsyncIOMotorDatabase] = None) -> None:
        self._db = db

    def bind(self, db: AsyncIOMotorDatabase) -> None:
        self._db = db

    def _collection(self):
        if self._db is None:
            return None
        settings = get_settings()
        return self._db[settings.chat_history_collection]

    async def save_turn(self, turn: ChatTurn) -> None:
        collection = self._collection()
        if collection is None:
            logger.warning("Chat history not saved — database unavailable")
            return

        document = {
            "session_id": turn.session_id,
            "user_message": turn.user_message,
            "assistant_message": turn.assistant_message,
            "created_at": turn.created_at,
            "sources": [source.to_dict() for source in turn.sources],
            "location": turn.location,
            "provider": turn.provider,
            "model": turn.model,
        }
        await collection.insert_one(document)

    async def list_turns(self, session_id: str, *, limit: int = 50) -> List[ChatTurn]:
        collection = self._collection()
        if collection is None:
            return []

        cursor = (
            collection.find({"session_id": session_id})
            .sort("created_at", 1)
            .limit(limit)
        )
        turns: List[ChatTurn] = []
        async for row in cursor:
            turns.append(self._to_turn(row))
        return turns

    async def list_recent_turns(self, session_id: str, *, limit: int = 4) -> List[ChatTurn]:
        collection = self._collection()
        if collection is None:
            return []

        cursor = (
            collection.find({"session_id": session_id})
            .sort("created_at", -1)
            .limit(limit)
        )
        rows = [self._to_turn(row) async for row in cursor]
        rows.reverse()
        return rows

    async def list_sessions(self, *, limit: int = 30) -> List[Dict[str, Any]]:
        collection = self._collection()
        if collection is None:
            return []

        pipeline = [
            {"$sort": {"created_at": 1}},
            {
                "$group": {
                    "_id": "$session_id",
                    "title": {"$first": "$user_message"},
                    "updated_at": {"$last": "$created_at"},
                    "message_count": {"$sum": 1},
                }
            },
            {"$sort": {"updated_at": -1}},
            {"$limit": limit},
        ]
        sessions: List[Dict[str, Any]] = []
        async for row in collection.aggregate(pipeline):
            sessions.append(
                {
                    "session_id": row["_id"],
                    "title": (row.get("title") or "New chat")[:80],
                    "updated_at": row.get("updated_at") or datetime.utcnow(),
                    "message_count": int(row.get("message_count") or 0),
                }
            )
        return sessions

    async def delete_session(self, session_id: str) -> bool:
        collection = self._collection()
        if collection is None:
            return False
        result = await collection.delete_many({"session_id": session_id})
        return result.deleted_count > 0

    def _to_turn(self, row: Dict[str, Any]) -> ChatTurn:
        sources = []
        for source in row.get("sources") or []:
            if not isinstance(source, dict):
                continue
            sources.append(
                ChatSource(
                    title=str(source.get("title") or "Source"),
                    url=str(source.get("url") or ""),
                    category=source.get("category"),
                    updated_at=source.get("updated_at"),
                )
            )
        return ChatTurn(
            session_id=str(row.get("session_id") or ""),
            user_message=str(row.get("user_message") or ""),
            assistant_message=str(row.get("assistant_message") or ""),
            sources=sources,
            location=row.get("location"),
            created_at=row.get("created_at") or datetime.utcnow(),
            provider=row.get("provider"),
            model=row.get("model"),
        )

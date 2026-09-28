"""Store operational error audits without secrets or extra personal data."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class ErrorAuditRepository:
    def __init__(self, db: Optional[AsyncIOMotorDatabase] = None) -> None:
        self._db = db

    def bind(self, db: AsyncIOMotorDatabase) -> None:
        self._db = db

    def _collection(self):
        if self._db is None:
            return None
        settings = get_settings()
        return self._db[settings.error_audit_collection]

    async def record(
        self,
        *,
        error_type: str,
        message: str,
        endpoint: str = "/api/chat",
        session_id: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        status_code: Optional[int] = None,
        attempt: Optional[int] = None,
        resolved: bool = False,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        collection = self._collection()
        payload = {
            "timestamp": datetime.now(timezone.utc),
            "session_id": session_id,
            "endpoint": endpoint,
            "error_type": error_type,
            "provider": provider,
            "model": model,
            "attempt": attempt,
            "status_code": status_code,
            "message": message[:500],
            "resolved": resolved,
            "extra": extra or {},
        }
        logger.error(
            "audit error_type=%s provider=%s model=%s status=%s",
            error_type,
            provider,
            model,
            status_code,
        )
        if collection is None:
            return
        try:
            await collection.insert_one(payload)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to persist error audit: %s", type(exc).__name__)

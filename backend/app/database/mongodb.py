"""MongoDB connection via Motor (async)."""

from typing import Optional

import certifi
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongo() -> None:
    """Open the MongoDB client and ensure useful indexes exist."""
    global _client, _db

    settings = get_settings()
    if not settings.mongodb_uri:
        raise RuntimeError(
            "MONGODB_URI is not set. Add it to backend/.env before starting the API."
        )

    logger.info("Connecting to MongoDB database=%s", settings.database_name)
    _client = AsyncIOMotorClient(
        settings.mongodb_uri,
        serverSelectionTimeoutMS=8000,
        tlsCAFile=certifi.where(),
    )
    # Fail fast if URI/network is wrong
    await _client.admin.command("ping")
    _db = _client[settings.database_name]
    await _ensure_indexes(_db)
    logger.info("MongoDB connected")


async def _ensure_indexes(db: AsyncIOMotorDatabase) -> None:
    settings = get_settings()

    chat = db[settings.chat_history_collection]
    await chat.create_index("session_id")
    await chat.create_index("created_at")

    knowledge = db[settings.knowledge_collection]
    await knowledge.create_index("category")
    await knowledge.create_index("updated_at")
    await knowledge.create_index("keywords")

    audit = db[settings.error_audit_collection]
    await audit.create_index("timestamp")
    await audit.create_index("error_type")

    # Phase 2 prep — collection ready for campus locations later
    locations = db["campus_locations"]
    await locations.create_index("name")
    await locations.create_index("aliases")


async def close_mongo_connection() -> None:
    global _client, _db
    if _client is not None:
        _client.close()
        logger.info("MongoDB connection closed")
    _client = None
    _db = None


def get_database() -> AsyncIOMotorDatabase:
    if _db is None:
        raise RuntimeError("Database is not initialized. Call connect_to_mongo first.")
    return _db


def is_database_ready() -> bool:
    return _db is not None


async def check_mongo_health() -> bool:
    """Return True if MongoDB responds to ping."""
    if _client is None:
        return False
    try:
        await _client.admin.command("ping")
        return True
    except Exception as exc:  # noqa: BLE001 — health check must not raise
        logger.warning("MongoDB health check failed: %s", type(exc).__name__)
        return False

"""Shared FastAPI dependencies."""

from functools import lru_cache
from typing import Optional

from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import Settings, get_settings
from app.database.mongodb import get_database, is_database_ready
from app.repositories.chat_repository import ChatRepository
from app.repositories.error_audit_repository import ErrorAuditRepository
from app.services.ai_service import AIService
from app.services.auth_service import AuthService, verify_access_token
from app.services.chat_service import ChatService
from app.services.retrieval_service import RetrievalService


def settings_dep() -> Settings:
    return get_settings()


def database_dep(request: Request) -> AsyncIOMotorDatabase:
    """Prefer app-state DB; fall back to module getter."""
    db = getattr(request.app.state, "db", None)
    if db is not None:
        return db
    return get_database()


def get_auth_service(request: Request) -> AuthService:
    service = getattr(request.app.state, "auth_service", None)
    if service is not None:
        return service
    db = getattr(request.app.state, "db", None)
    service = AuthService(db)
    request.app.state.auth_service = service
    return service


def get_current_user_email(request: Request) -> Optional[str]:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ", 1)[1].strip()
    payload = verify_access_token(token)
    if payload and payload.get("email"):
        return str(payload["email"]).strip().lower()
    return None


@lru_cache
def get_retrieval_service() -> RetrievalService:
    return RetrievalService()


def get_chat_service(request: Request) -> ChatService:
    service = getattr(request.app.state, "chat_service", None)
    if service is not None:
        return service

    db = getattr(request.app.state, "db", None)
    if db is None and is_database_ready():
        db = get_database()

    chat_repo = ChatRepository(db)
    audit_repo = ErrorAuditRepository(db)
    service = ChatService(
        retrieval=get_retrieval_service(),
        ai=AIService(),
        chat_repo=chat_repo,
        audit_repo=audit_repo,
    )
    request.app.state.chat_service = service
    return service

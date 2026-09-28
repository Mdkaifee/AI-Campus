"""Authentication service: password hashing, JWT tokens, and user management."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.user import User

logger = get_logger(__name__)

JWT_SECRET = "daviet_campus_ai_secure_jwt_secret_key_2026"
TOKEN_EXPIRY_SECONDS = 30 * 24 * 3600  # 30 days


def _hash_password(password: str, salt: str) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with 100,000 iterations."""
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
    ).hex()


def _b64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64_decode(data: str) -> bytes:
    padding = 4 - (len(data) % 4)
    if padding != 4:
        data += "=" * padding
    return base64.urlsafe_b64decode(data.encode("utf-8"))


def create_access_token(payload: Dict[str, Any]) -> str:
    """Generate HS256 signed JWT token without external dependencies."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload_copy = dict(payload)
    payload_copy["exp"] = int(time.time()) + TOKEN_EXPIRY_SECONDS
    payload_copy["iat"] = int(time.time())

    encoded_header = _b64_encode(json.dumps(header).encode("utf-8"))
    encoded_payload = _b64_encode(json.dumps(payload_copy).encode("utf-8"))
    signature_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")

    signature = hmac.new(
        JWT_SECRET.encode("utf-8"), signature_input, hashlib.sha256
    ).digest()
    encoded_signature = _b64_encode(signature)

    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"


def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify HS256 signed JWT token."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        encoded_header, encoded_payload, encoded_signature = parts
        signature_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")

        expected_signature = hmac.new(
            JWT_SECRET.encode("utf-8"), signature_input, hashlib.sha256
        ).digest()
        actual_signature = _b64_decode(encoded_signature)

        if not hmac.compare_digest(expected_signature, actual_signature):
            return None

        payload = json.loads(_b64_decode(encoded_payload).decode("utf-8"))
        if payload.get("exp", 0) < time.time():
            return None  # Token expired

        return payload
    except Exception as exc:
        logger.warning("Token verification failed: %s", type(exc).__name__)
        return None


class AuthService:
    def __init__(self, db: Optional[AsyncIOMotorDatabase] = None) -> None:
        self._db = db
        self._memory_users: Dict[str, User] = {}  # In-memory fallback if mongo is down

    def bind(self, db: AsyncIOMotorDatabase) -> None:
        self._db = db

    def _collection(self):
        if self._db is None:
            return None
        return self._db["users"]

    async def get_user_by_email(self, email: str) -> Optional[User]:
        clean_email = email.strip().lower()
        collection = self._collection()

        if collection is not None:
            doc = await collection.find_one({"email": clean_email})
            if doc:
                return User(
                    id=str(doc.get("id") or doc.get("_id")),
                    name=str(doc.get("name", "")),
                    email=str(doc.get("email", "")),
                    hashed_password=str(doc.get("hashed_password", "")),
                    salt=str(doc.get("salt", "")),
                    created_at=doc.get("created_at") or datetime.now(timezone.utc),
                )

        return self._memory_users.get(clean_email)

    async def signup(self, name: str, email: str, password: str) -> tuple[User, str]:
        clean_email = email.strip().lower()
        existing = await self.get_user_by_email(clean_email)
        if existing is not None:
            raise ValueError("An account with this email already exists.")

        user_id = str(uuid.uuid4())
        salt = secrets.token_hex(16)
        hashed_password = _hash_password(password, salt)
        user = User(
            id=user_id,
            name=name.strip(),
            email=clean_email,
            hashed_password=hashed_password,
            salt=salt,
            created_at=datetime.now(timezone.utc),
        )

        collection = self._collection()
        if collection is not None:
            try:
                await collection.insert_one(user.to_dict())
            except Exception as exc:
                logger.warning("Could not persist user to Mongo, using in-memory: %s", type(exc).__name__)

        self._memory_users[clean_email] = user

        token = create_access_token({
            "sub": user.id,
            "name": user.name,
            "email": user.email,
        })
        return user, token

    async def login(self, email: str, password: str) -> tuple[User, str]:
        clean_email = email.strip().lower()
        user = await self.get_user_by_email(clean_email)
        if user is None:
            raise ValueError("Invalid email or password.")

        hashed_check = _hash_password(password, user.salt)
        if not hmac.compare_digest(user.hashed_password, hashed_check):
            raise ValueError("Invalid email or password.")

        token = create_access_token({
            "sub": user.id,
            "name": user.name,
            "email": user.email,
        })
        return user, token

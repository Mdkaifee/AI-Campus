"""Pydantic schemas for authentication and user profiles."""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class UserSignUpRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=60, description="Full Name")
    email: str = Field(..., min_length=3, max_length=120, description="Student / User Email Address")
    password: str = Field(..., min_length=6, max_length=100, description="Password (at least 6 characters)")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip().lower()
        if "@" not in v or "." not in v:
            raise ValueError("Please provide a valid email address")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters")
        return v


class UserLoginRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=120, description="Registered Email Address")
    password: str = Field(..., min_length=1, description="Password")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return v.strip().lower()


class UserProfile(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime


class AuthResponse(BaseModel):
    token: str
    user: UserProfile
    message: str = "Authentication successful"

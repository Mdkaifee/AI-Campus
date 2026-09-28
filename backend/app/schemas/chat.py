"""Chat request/response schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class ChatSource(BaseModel):
    title: str
    url: str
    category: Optional[str] = None
    updated_at: Optional[str] = None


class ChatRequest(BaseModel):
    message: str = Field(..., description="Student question")
    session_id: Optional[str] = Field(
        default=None,
        description="Existing chat session. Omit to start a new session.",
    )

    @field_validator("message")
    @classmethod
    def message_not_blank(cls, value: str) -> str:
        cleaned = (value or "").strip()
        if not cleaned:
            raise ValueError("Please enter a question.")
        if len(cleaned) > 4000:
            raise ValueError("Please keep your question under 4000 characters.")
        return cleaned


from app.schemas.location import CampusLocationResponse


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: List[ChatSource] = Field(default_factory=list)
    location: Optional[CampusLocationResponse] = Field(
        default=None,
        description="Optional campus location navigation details with Google Maps if query is location-related.",
    )
    unavailable: bool = Field(
        default=False,
        description="True when the knowledge base did not contain a reliable answer.",
    )


class ChatTurnResponse(BaseModel):
    user_message: str
    assistant_message: str
    sources: List[ChatSource] = Field(default_factory=list)
    location: Optional[CampusLocationResponse] = Field(default=None)
    created_at: datetime


class ChatSessionResponse(BaseModel):
    session_id: str
    title: str
    updated_at: datetime
    message_count: int


class ChatHistoryResponse(BaseModel):
    session_id: str
    turns: List[ChatTurnResponse] = Field(default_factory=list)

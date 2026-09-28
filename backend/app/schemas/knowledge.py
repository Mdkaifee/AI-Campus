"""Pydantic schemas for knowledge items."""

from typing import List, Optional

from pydantic import BaseModel, Field


class KnowledgeItemSchema(BaseModel):
    title: str
    category: str
    content: str
    source_url: str
    updated_at: str
    keywords: List[str] = Field(default_factory=list)
    id: Optional[str] = None


class KnowledgeSourceSchema(BaseModel):
    title: str
    url: str
    category: Optional[str] = None
    updated_at: Optional[str] = None


class RetrievalResultSchema(BaseModel):
    items: List[KnowledgeItemSchema]
    query: str
    matched: bool

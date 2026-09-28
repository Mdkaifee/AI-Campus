"""Health check schemas."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"] = Field(
        description="Overall API status. degraded if a dependency is unavailable."
    )
    database: Optional[Literal["ok", "unavailable"]] = Field(
        default=None,
        description="MongoDB connectivity status when checked.",
    )

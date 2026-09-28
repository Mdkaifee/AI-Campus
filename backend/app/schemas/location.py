"""Campus location schemas for Phase 2 navigation preparation."""

from typing import List, Optional
from pydantic import BaseModel, Field


class CampusLocationBase(BaseModel):
    id: str = Field(..., description="Unique location identifier, e.g., 'tpo-office'")
    name: str = Field(..., description="Destination display name")
    aliases: List[str] = Field(default_factory=list, description="Common names or acronyms")
    block: Optional[str] = Field(None, description="Campus block / building name")
    floor: Optional[str] = Field(None, description="Floor level, e.g., 'Ground Floor', '1st Floor'")
    description: Optional[str] = Field(None, description="Location description or directions")
    latitude: Optional[float] = Field(None, description="GPS Latitude")
    longitude: Optional[float] = Field(None, description="GPS Longitude")
    maps_url: Optional[str] = Field(None, description="Google Maps navigation link")
    embed_map_url: Optional[str] = Field(None, description="Google Maps embed iframe link")
    search_map_url: Optional[str] = Field(None, description="Pre-filled search URL for opening in a new tab")


class CampusLocationResponse(CampusLocationBase):
    pass

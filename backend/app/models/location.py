"""Campus location domain model for Phase 2 navigation preparation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CampusLocation:
    """Campus destination model prepared for Phase 2 navigation."""

    id: str
    name: str
    aliases: List[str] = field(default_factory=list)
    block: Optional[str] = None
    floor: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    maps_url: Optional[str] = None
    embed_map_url: Optional[str] = None
    search_map_url: Optional[str] = None

    def __post_init__(self) -> None:
        import urllib.parse
        encoded_query = urllib.parse.quote(f"DAVIET Jalandhar {self.name}")
        if not self.embed_map_url:
            self.embed_map_url = f"https://maps.google.com/maps?q={encoded_query}&t=&z=17&ie=UTF8&iwloc=&output=embed"
        if not self.search_map_url:
            self.search_map_url = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
        if not self.maps_url:
            self.maps_url = self.search_map_url

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "aliases": self.aliases,
            "block": self.block,
            "floor": self.floor,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "maps_url": self.maps_url,
            "embed_map_url": self.embed_map_url,
            "search_map_url": self.search_map_url,
        }

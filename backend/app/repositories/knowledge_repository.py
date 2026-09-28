"""Load and query DAVIET knowledge JSON files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.knowledge import KnowledgeItem

logger = get_logger(__name__)


class KnowledgeRepository:
    """File-backed knowledge repository (JSON). Swap later for MongoDB without changing callers."""

    def __init__(self, knowledge_dir: Optional[Path] = None) -> None:
        settings = get_settings()
        self._dir = Path(knowledge_dir or settings.knowledge_base_dir)
        self._items: List[KnowledgeItem] = []
        self._loaded = False

    def load(self, force: bool = False) -> None:
        if self._loaded and not force:
            return

        items: List[KnowledgeItem] = []
        if not self._dir.exists():
            logger.error("Knowledge directory missing: %s", self._dir)
            self._items = []
            self._loaded = True
            return

        for path in sorted(self._dir.glob("*.json")):
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                logger.error("Failed to read knowledge file %s: %s", path.name, type(exc).__name__)
                continue

            if not isinstance(raw, list):
                logger.warning("Skipping %s — expected a JSON array", path.name)
                continue

            for index, entry in enumerate(raw):
                if not isinstance(entry, dict):
                    continue
                try:
                    item = KnowledgeItem(
                        id=f"{path.stem}-{index}",
                        title=str(entry.get("title", "")).strip(),
                        category=str(entry.get("category", path.stem)).strip(),
                        content=str(entry.get("content", "")).strip(),
                        source_url=str(entry.get("source_url", "")).strip(),
                        updated_at=str(entry.get("updated_at", "")).strip(),
                        keywords=[
                            str(k).strip().lower()
                            for k in (entry.get("keywords") or [])
                            if str(k).strip()
                        ],
                    )
                except Exception as exc:  # noqa: BLE001
                    logger.warning(
                        "Invalid knowledge entry in %s[%s]: %s",
                        path.name,
                        index,
                        type(exc).__name__,
                    )
                    continue

                if item.title and item.content:
                    items.append(item)

        self._items = items
        self._loaded = True
        logger.info("Loaded %s knowledge items from %s", len(items), self._dir)

    def list_all(self, force_reload: bool = False) -> List[KnowledgeItem]:
        self.load(force=force_reload)
        return list(self._items)

    def list_by_category(self, category: str) -> List[KnowledgeItem]:
        self.load()
        category_l = category.lower().strip()
        return [item for item in self._items if item.category.lower() == category_l]

    def get_by_id(self, item_id: str) -> Optional[KnowledgeItem]:
        self.load()
        for item in self._items:
            if item.id == item_id:
                return item
        return None

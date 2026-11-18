"""
Character Registry - Canonical Identity Storage
Persists character identities, model versions, voice mappings, and relationship webs.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json

class CharacterRegistry:
    """Manages permanent character registry across all seasons and episodes."""

    def __init__(self, storage_path: Optional[str] = None):
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            self.storage_path = Path("E:/YT/series/series_001/characters/canonical_registry.json")
        self.characters: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self):
        if self.storage_path.exists():
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.characters = json.load(f)
            except Exception:
                self.characters = {}

    def save(self):
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.characters, f, indent=2)

    def register_character(self, spec: Dict[str, Any]):
        char_id = spec["character_id"]
        self.characters[char_id] = spec
        self.save()

    def get_character(self, char_id: str) -> Optional[Dict[str, Any]]:
        return self.characters.get(char_id)

    def list_characters(self) -> List[Dict[str, Any]]:
        return list(self.characters.values())

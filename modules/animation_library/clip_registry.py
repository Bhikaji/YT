"""
Standard Animation Clip Registry
Catalogs, tags, and retrieves skeletal animation clips mapped to UHD-54 standard.
"""

from typing import Dict, Any, List, Optional
import json
import os
from pathlib import Path

class AnimationClipRegistry:
    """Manages the internal library of reusable skeletal animations."""

    def __init__(self, storage_dir: str = r"E:\YT\assets\animations"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.registry_index_file = self.storage_dir / "clip_index.json"
        self._load_index()

    def _load_index(self):
        if self.registry_index_file.exists():
            with open(self.registry_index_file, "r", encoding="utf-8") as f:
                self.clips = json.load(f)
        else:
            self.clips = self._default_clip_library()
            self._save_index()

    def _save_index(self):
        with open(self.registry_index_file, "w", encoding="utf-8") as f:
            json.dump(self.clips, f, indent=2)

    def _default_clip_library(self) -> Dict[str, Any]:
        return {
            "anim_walk_cycle_01": {
                "name": "Brisk Confident Walk Cycle",
                "category": "locomotion",
                "duration_seconds": 1.2,
                "loopable": True,
                "fps": 30,
                "skeleton_type": "UHD54",
                "tags": ["walk", "locomotion", "confident", "adventure"],
                "file_path": str(self.storage_dir / "walk_cycle_01.bvh")
            },
            "anim_run_cycle_01": {
                "name": "Heroic Sprint Run Cycle",
                "category": "locomotion",
                "duration_seconds": 0.8,
                "loopable": True,
                "fps": 30,
                "skeleton_type": "UHD54",
                "tags": ["run", "sprint", "fast", "urgent"],
                "file_path": str(self.storage_dir / "run_cycle_01.bvh")
            },
            "anim_point_wonder_01": {
                "name": "Hand Raise & Forward Pointing in Awe",
                "category": "acting",
                "duration_seconds": 2.5,
                "loopable": False,
                "fps": 30,
                "skeleton_type": "UHD54",
                "tags": ["point", "gesture", "wonder", "discovery"],
                "file_path": str(self.storage_dir / "point_wonder_01.bvh")
            },
            "anim_idle_inquisitive_01": {
                "name": "Inquisitive Breathing Idle with Head Tilt",
                "category": "idle",
                "duration_seconds": 3.0,
                "loopable": True,
                "fps": 30,
                "skeleton_type": "UHD54",
                "tags": ["idle", "breathing", "inquisitive", "curious"],
                "file_path": str(self.storage_dir / "idle_inquisitive_01.bvh")
            }
        }

    def search_clips(self, tag: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for clip_id, data in self.clips.items():
            if category and data.get("category") != category:
                continue
            if tag and tag.lower() not in [t.lower() for t in data.get("tags", [])]:
                continue
            res = {"clip_id": clip_id}
            res.update(data)
            results.append(res)
        return results

    def get_clip(self, clip_id: str) -> Optional[Dict[str, Any]]:
        return self.clips.get(clip_id)

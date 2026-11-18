"""
BVH Motion Capture Parser
Reads BVH files and extracts joint hierarchies and motion channels.
"""

from typing import Dict, Any, List, Optional
import os

class BVHParser:
    """Parses standard Biovision Hierarchy (BVH) files into skeletal data structures."""

    @classmethod
    def parse_header_and_frame_count(cls, bvh_path: str) -> Dict[str, Any]:
        """Reads BVH metadata: bones present, total frames, frame interval."""
        if not os.path.exists(bvh_path):
            return {"error": f"BVH file not found: {bvh_path}", "is_valid": False}

        bones = []
        frame_count = 0
        frame_time = 0.033333

        with open(bvh_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        in_motion_section = False
        for line in lines:
            line_str = line.strip()
            if line_str.startswith("ROOT ") or line_str.startswith("JOINT "):
                bone_name = line_str.split()[1]
                bones.append(bone_name)
            elif line_str.startswith("Frames:"):
                frame_count = int(line_str.split(":")[1].strip())
            elif line_str.startswith("Frame Time:"):
                frame_time = float(line_str.split(":")[1].strip())

        return {
            "is_valid": len(bones) > 0 and frame_count > 0,
            "bones": bones,
            "bone_count": len(bones),
            "frame_count": frame_count,
            "frame_time": frame_time,
            "fps": round(1.0 / frame_time) if frame_time > 0 else 30
        }

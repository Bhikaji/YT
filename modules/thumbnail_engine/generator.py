"""
High-CTR Thumbnail Engine
Creates click-worthy thumbnails with high visual contrast, character emotion, and punchy typography.
"""

from typing import Dict, Any, Optional
from pathlib import Path
from backend.app.services.thumbnail_engine.typography_styler import ThumbnailGenerator

class ProductionThumbnailEngine:
    """Automates production of high-converting YouTube thumbnails (1280x720 / 1080x1920)."""

    @classmethod
    def generate_thumbnail(
        cls,
        base_frame_path: str,
        output_thumbnail_path: str,
        headline_text: str = "CANNOT UNSEE THIS!",
        emotion_tag: str = "SHOCK",
        format_type: str = "SHORT"
    ) -> Dict[str, Any]:
        """
        Renders styled thumbnail with outlined text and cinematic contrast.
        """
        thumb_path = ThumbnailGenerator.create_thumbnail(
            base_frame_path=base_frame_path,
            output_thumbnail_path=output_thumbnail_path,
            headline_text=headline_text,
            emotion_tag=emotion_tag,
            format_type=format_type
        )

        return {
            "success": True,
            "thumbnail_path": thumb_path,
            "headline": headline_text,
            "emotion": emotion_tag,
            "format": format_type
        }

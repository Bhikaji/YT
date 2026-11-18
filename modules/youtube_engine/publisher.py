"""
YouTube Data API v3 Publisher Engine
Handles OAuth2 authentication, video uploading, thumbnail binding, and release scheduling.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from backend.app.services.youtube_engine.uploader import YouTubeUploader

class YouTubePublishingEngine:
    """Manages YouTube Data API v3 staging, playlist management, and automated release."""

    @classmethod
    def publish_video(
        cls,
        video_file_path: str,
        thumbnail_path: str,
        title: str,
        description: str,
        tags: List[str],
        privacy_status: str = "unlisted",
        made_for_kids: bool = False,
        publish_mode: str = "HUMAN_APPROVAL"
    ) -> Dict[str, Any]:
        """
        Gated publishing engine. Ensures videos are safely staged before going live.
        """
        return YouTubeUploader.publish_video(
            video_file_path=video_file_path,
            thumbnail_path=thumbnail_path,
            title=title,
            description=description,
            tags=tags,
            privacy_status=privacy_status,
            made_for_kids=made_for_kids,
            approval_mode=publish_mode
        )

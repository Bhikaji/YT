import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from backend.app.config import settings

class YouTubeUploader:
    """Manages YouTube Data API v3 authentication, staging, and video uploads."""

    @classmethod
    def publish_video(
        cls,
        video_file_path: str,
        thumbnail_path: Optional[str],
        title: str,
        description: str,
        tags: list,
        privacy_status: str = "unlisted",
        made_for_kids: bool = False,
        approval_mode: str = "MANUAL_APPROVAL"
    ) -> Dict[str, Any]:
        """
        Publishes or stages video for YouTube upload according to approval settings.
        """
        if not os.path.exists(video_file_path):
            raise FileNotFoundError(f"Video file not found at: {video_file_path}")

        # Check OAuth token existence
        token_path = settings.YOUTUBE_OAUTH_TOKEN_FILE
        has_oauth = token_path and os.path.exists(token_path)

        if approval_mode == "MANUAL_APPROVAL":
            return {
                "status": "READY_FOR_APPROVAL",
                "message": "Video rendered and staged. Waiting for creator approval before YouTube upload.",
                "video_path": video_file_path,
                "thumbnail_path": thumbnail_path,
                "metadata": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "privacy_status": privacy_status,
                    "made_for_kids": made_for_kids
                },
                "has_oauth_configured": has_oauth
            }

        if not has_oauth:
            # Staged offline mode
            return {
                "status": "STAGED_OFFLINE",
                "message": "YouTube OAuth token not detected. Video staged locally.",
                "youtube_url": None,
                "simulated_id": f"yt_local_{abs(hash(video_file_path))}"
            }

        # Real Google API upload logic
        try:
            from googleapiclient.discovery import build
            from google.oauth2.credentials import Credentials
            from googleapiclient.http import MediaFileUpload

            with open(token_path, "r", encoding="utf-8") as f:
                token_data = json.load(f)
            creds = Credentials.from_authorized_user_info(token_data)
            youtube = build("youtube", "v3", credentials=creds)

            body = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": "1"
                },
                "status": {
                    "privacyStatus": privacy_status,
                    "selfDeclaredMadeForKids": made_for_kids
                }
            }

            media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
            request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
            response = request.execute()
            video_id = response.get("id")

            # Upload thumbnail if available
            if thumbnail_path and os.path.exists(thumbnail_path) and video_id:
                thumb_media = MediaFileUpload(thumbnail_path)
                youtube.thumbnails().set(videoId=video_id, media_body=thumb_media).execute()

            return {
                "status": "PUBLISHED",
                "video_id": video_id,
                "youtube_url": f"https://youtu.be/{video_id}",
                "uploaded_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "UPLOAD_FAILED",
                "error": str(e)
            }

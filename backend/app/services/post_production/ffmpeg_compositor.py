import os
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any
import imageio_ffmpeg
from backend.app.config import settings

class FFmpegCompositor:
    """Headless video compositor handling video encoding, audio mixing, and subtitles."""

    @staticmethod
    def get_ffmpeg_path() -> str:
        return imageio_ffmpeg.get_ffmpeg_exe()

    @classmethod
    def assemble_video_with_audio(
        cls,
        frames_pattern: str,  # e.g., "E:/YT/output/renders/frame_%04d.png"
        audio_file_path: str,
        output_video_path: str,
        fps: int = 30,
        subtitles_file: Optional[str] = None
    ) -> str:
        """
        Combines rendered frame sequence with dialogue audio into a YouTube-ready MP4.
        """
        ffmpeg_exe = cls.get_ffmpeg_path()
        os.makedirs(Path(output_video_path).parent, exist_ok=True)

        # Base ffmpeg command
        cmd = [
            ffmpeg_exe,
            "-y",
            "-framerate", str(fps),
            "-i", frames_pattern,
            "-i", audio_file_path,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",  # Sync to shorter stream
            "-movflags", "+faststart",  # Web/YouTube optimized
            output_video_path
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg assembly failed: {result.stderr}")

        return output_video_path

import os
import subprocess
import json
from pathlib import Path
from typing import Optional
import imageio_ffmpeg
from backend.app.services.voice_engine.rhubarb_lipsync import LipSyncEngine

class AudioProcessor:
    """Manages audio file metadata, normalization, and lip-sync synchronization."""

    @staticmethod
    def get_ffmpeg_path() -> str:
        """Returns the absolute path to the functional FFmpeg executable."""
        return imageio_ffmpeg.get_ffmpeg_exe()

    @classmethod
    def get_audio_duration(cls, audio_file_path: str) -> float:
        """Calculates audio duration in seconds via FFmpeg."""
        ffmpeg_exe = cls.get_ffmpeg_path()
        cmd = [
            ffmpeg_exe,
            "-i", audio_file_path,
            "-f", "null",
            "-"
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Parse stderr for Duration: 00:00:03.45
        import re
        match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", result.stderr)
        if match:
            hours, minutes, seconds = match.groups()
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
        return 3.0  # safe fallback

    @classmethod
    def process_dialogue_audio(
        cls,
        text: str,
        audio_file_path: str,
        viseme_output_dir: Optional[str] = None
    ) -> dict:
        """
        Takes raw synthesized audio, measures exact duration,
        and generates synchronized 3D viseme keyframes.
        """
        duration = cls.get_audio_duration(audio_file_path)
        
        if not viseme_output_dir:
            viseme_output_dir = Path(audio_file_path).parent

        stem = Path(audio_file_path).stem
        viseme_json_path = str(Path(viseme_output_dir) / f"{stem}_visemes.json")

        visemes = LipSyncEngine.generate_visemes_from_text_and_duration(
            text=text,
            total_duration_seconds=duration,
            output_json_path=viseme_json_path
        )

        return {
            "audio_file_path": audio_file_path,
            "duration_seconds": duration,
            "viseme_json_path": viseme_json_path,
            "viseme_count": len(visemes)
        }

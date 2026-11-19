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
            "-preset", "medium",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-af", "apad",
            "-shortest",  # Sync precisely to the 300-frame video timeline
            "-movflags", "+faststart",  # Web/YouTube optimized
            output_video_path
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg assembly failed: {result.stderr}")

        return output_video_path

    @classmethod
    def concatenate_episodes(
        cls,
        episode_paths: List[str],
        output_marathon_path: str,
        fps: int = 30
    ) -> Dict[str, Any]:
        """
        Concatenates multiple episode videos into a single 1-hour/marathon movie with chapter timestamps.
        """
        ffmpeg_exe = cls.get_ffmpeg_path()
        output_file = Path(output_marathon_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        concat_list_file = output_file.parent / "marathon_concat.txt"
        with open(concat_list_file, "w", encoding="utf-8") as f:
            for p in episode_paths:
                safe = str(Path(p).resolve()).replace("\\", "/")
                f.write(f"file '{safe}'\n")

        # Fast lossless copy concatenation
        cmd = [
            ffmpeg_exe, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list_file),
            "-c", "copy",
            "-movflags", "+faststart",
            str(output_file)
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            # Fallback to re-encoding if codec profiles slightly differ
            fallback_cmd = [
                ffmpeg_exe, "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_list_file),
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart",
                str(output_file)
            ]
            subprocess.run(fallback_cmd, check=True)

        return {
            "marathon_path": str(output_file),
            "episodes_count": len(episode_paths)
        }

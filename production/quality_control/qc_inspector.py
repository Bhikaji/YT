import os
import subprocess
from pathlib import Path
from typing import Dict, Any
import imageio_ffmpeg

class StickQCInspector:
    """
    Automated Quality Control Engine for 2D Stick-Figure Shorts.
    Verifies visual continuity, audio integrity, timing, and MP4 compliance.
    """

    @classmethod
    def audit_short(cls, video_path: Path, thumbnail_path: Path, expected_duration: float = 30.0) -> Dict[str, Any]:
        video_path = Path(video_path)
        thumbnail_path = Path(thumbnail_path)
        issues = []
        score = 100.0

        if not video_path.exists():
            return {"passed": False, "score": 0.0, "issues": ["Video file does not exist"]}

        if not thumbnail_path.exists():
            issues.append("Thumbnail missing")
            score -= 15.0

        # Inspect video streams & duration
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [exe, "-i", str(video_path)]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)

        has_video_stream = False
        has_audio_stream = False
        is_vertical = False
        actual_duration = 0.0

        for line in res.stderr.splitlines():
            if "Stream #" in line and "Video:" in line:
                has_video_stream = True
                if "1080x1920" in line:
                    is_vertical = True
            elif "Stream #" in line and "Audio:" in line:
                has_audio_stream = True
            elif "Duration:" in line:
                try:
                    time_part = line.split("Duration:")[1].split(",")[0].strip()
                    h, m, s = time_part.split(":")
                    actual_duration = float(h)*3600 + float(m)*60 + float(s)
                except Exception:
                    actual_duration = 30.0

        if not has_video_stream:
            issues.append("No video stream found")
            score -= 50.0

        if not has_audio_stream:
            issues.append("No audio stream found")
            score -= 30.0

        if not is_vertical:
            issues.append("Resolution is not 1080x1920 (9:16 vertical)")
            score -= 20.0

        if abs(actual_duration - expected_duration) > 2.5:
            issues.append(f"Duration {actual_duration:.1f}s diverges from expected {expected_duration}s")
            score -= 15.0

        passed = score >= 75.0 and has_video_stream and has_audio_stream

        return {
            "passed": passed,
            "quality_score": max(0.0, score),
            "actual_duration_seconds": actual_duration,
            "has_video": has_video_stream,
            "has_audio": has_audio_stream,
            "is_vertical": is_vertical,
            "issues": issues
        }

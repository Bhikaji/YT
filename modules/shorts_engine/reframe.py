"""
YouTube Shorts Dynamic Re-framing Engine
Converts 16:9 master scenes to 9:16 vertical shorts with smart character tracking.
"""

import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from backend.app.services.voice_engine.audio_processor import AudioProcessor

class ShortsReframeEngine:
    """Reframes horizontal video to vertical 1080x1920 with high retention pacing."""

    @classmethod
    def reframe_to_vertical_short(
        cls,
        input_video_path: str,
        output_short_path: str,
        crop_x_offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Crops input horizontal video to 9:16 center-cut or targeted character focus.
        Crop filter: crop=ih*(9/16):ih:(iw-ow)/2:0,scale=1080:1920
        """
        ffmpeg_bin = AudioProcessor.get_ffmpeg_path()
        if not ffmpeg_bin:
            return {"error": "FFmpeg not available", "success": False}

        out_path = Path(output_short_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if crop_x_offset is not None:
            crop_filter = f"crop=ih*(9/16):ih:{crop_x_offset}:0,scale=1080:1920"
        else:
            crop_filter = "crop=ih*(9/16):ih:(iw-ow)/2:0,scale=1080:1920"

        cmd = [
            ffmpeg_bin, "-y",
            "-i", input_video_path,
            "-vf", crop_filter,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "copy",
            str(out_path)
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        return {
            "success": res.returncode == 0,
            "output_short_path": str(out_path),
            "filter": crop_filter,
            "error": res.stderr if res.returncode != 0 else None
        }

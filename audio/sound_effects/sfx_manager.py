import os
import subprocess
from pathlib import Path
import imageio_ffmpeg

class CartoonSFXManager:
    """
    Manages and synthesizes cartoon sound effects using FFmpeg's native audio filters.
    Zero external dependencies, 100% royalty-free.
    """

    @classmethod
    def generate_sfx(cls, sfx_name: str, output_file: Path) -> str:
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        if output_file.exists():
            return str(output_file)

        exe = imageio_ffmpeg.get_ffmpeg_exe()
        name = sfx_name.lower()

        if "ding" in name or "chime" in name or "lightbulb" in name:
            # High-pitched chime
            filter_str = "sine=frequency=880:duration=0.6,afade=t=out:st=0.3:d=0.3"
        elif "whoosh" in name:
            # Noise sweep
            filter_str = "anoisesrc=d=0.3:c=pink:r=44100:a=0.5,afade=t=in:st=0:d=0.1,afade=t=out:st=0.15:d=0.15"
        elif "impact" in name or "thud" in name:
            # Bass thud
            filter_str = "sine=frequency=110:duration=0.4,afade=t=out:st=0.1:d=0.3"
        elif "alarm" in name:
            # Alarm tone
            filter_str = "sine=frequency=620:duration=1.0,afade=t=out:st=0.8:d=0.2"
        elif "boing" in name or "spring" in name:
            # Boing sweep
            filter_str = "sine=frequency=300:duration=0.5,afade=t=out:st=0.2:d=0.3"
        elif "pop" in name:
            # Pop click
            filter_str = "sine=frequency=1200:duration=0.15,afade=t=out:st=0.05:d=0.1"
        else:
            # Default soft blip
            filter_str = "sine=frequency=520:duration=0.2,afade=t=out:st=0.1:d=0.1"

        cmd = [exe, "-y", "-f", "lavfi", "-i", filter_str, "-c:a", "libmp3lame", str(output_file)]
        subprocess.run(cmd, capture_output=True)
        return str(output_file)

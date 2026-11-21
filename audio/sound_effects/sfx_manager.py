import os
import subprocess
from pathlib import Path
import imageio_ffmpeg

class CartoonSFXManager:
    """
    Manages and synthesizes cartoon sound effects using real demo SFX assets or FFmpeg native filters.
    Zero external dependencies, 100% royalty-free.
    """

    KNOWN_ASSET_MAP = {
        "lightbulb_ding": "assets/audio/sfx/lightbulb_ding.wav",
        "ding_lightbulb": "assets/audio/sfx/lightbulb_ding.wav",
        "ding": "assets/audio/sfx/lightbulb_ding.wav",
        "cannonball_splash": "assets/audio/sfx/cannonball_splash.wav",
        "splash": "assets/audio/sfx/cannonball_splash.wav",
        "crocodile_panic_splash": "assets/audio/sfx/crocodile_panic_splash.wav",
        "panic_splash": "assets/audio/sfx/crocodile_panic_splash.wav",
        "marker_pen_edit": "assets/audio/sfx/marker_pen_edit.wav",
        "marker": "assets/audio/sfx/marker_pen_edit.wav",
        "cartoon_shock_sting": "assets/audio/sfx/cartoon_shock_sting.wav",
        "shock_sting": "assets/audio/sfx/cartoon_shock_sting.wav",
        "shock": "assets/audio/sfx/cartoon_shock_sting.wav"
    }

    @classmethod
    def get_sfx_path(cls, sfx_name: str) -> str:
        """
        Returns high-quality authentic SFX asset if available, or generates dynamic audio via FFmpeg.
        """
        name_lower = sfx_name.lower().strip()
        for key, rel_path in cls.KNOWN_ASSET_MAP.items():
            if key in name_lower:
                p = Path(rel_path)
                if p.exists():
                    return str(p.resolve())

        # Check default generated cache
        cache_file = Path("assets/audio/sfx/cache") / f"{name_lower}.mp3"
        return cls.generate_sfx(name_lower, cache_file)

    @classmethod
    def generate_sfx(cls, sfx_name: str, output_file: Path) -> str:
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        if output_file.exists():
            return str(output_file)

        exe = imageio_ffmpeg.get_ffmpeg_exe()
        name = sfx_name.lower()

        if "ding" in name or "chime" in name or "lightbulb" in name:
            filter_str = "sine=frequency=880:duration=0.6,afade=t=out:st=0.3:d=0.3"
        elif "whoosh" in name:
            filter_str = "anoisesrc=d=0.3:c=pink:r=44100:a=0.5,afade=t=in:st=0:d=0.1,afade=t=out:st=0.15:d=0.15"
        elif "impact" in name or "thud" in name:
            filter_str = "sine=frequency=110:duration=0.4,afade=t=out:st=0.1:d=0.3"
        elif "alarm" in name:
            filter_str = "sine=frequency=620:duration=1.0,afade=t=out:st=0.8:d=0.2"
        elif "boing" in name or "spring" in name:
            filter_str = "sine=frequency=300:duration=0.5,afade=t=out:st=0.2:d=0.3"
        elif "pop" in name:
            filter_str = "sine=frequency=1200:duration=0.15,afade=t=out:st=0.05:d=0.1"
        else:
            filter_str = "sine=frequency=520:duration=0.2,afade=t=out:st=0.1:d=0.1"

        cmd = [exe, "-y", "-f", "lavfi", "-i", filter_str, "-c:a", "libmp3lame", str(output_file)]
        subprocess.run(cmd, capture_output=True)
        return str(output_file)

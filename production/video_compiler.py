import os
import subprocess
from pathlib import Path
import imageio_ffmpeg

class StickVideoCompiler:
    """
    Assembles rendered 2D frame sequences and master soundtracks into high-quality vertical MP4 shorts.
    """

    @classmethod
    def compile_short(
        cls,
        frames_pattern: str,
        audio_path: str,
        output_mp4_path: Path,
        fps: int = 30
    ) -> Path:
        output_mp4_path = Path(output_mp4_path)
        output_mp4_path.parent.mkdir(parents=True, exist_ok=True)
        exe = imageio_ffmpeg.get_ffmpeg_exe()

        cmd = [
            exe, "-y",
            "-framerate", str(fps),
            "-i", str(frames_pattern),
            "-i", str(audio_path),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-af", "apad",
            "-shortest",
            "-movflags", "+faststart",
            str(output_mp4_path)
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Video compilation failed: {res.stderr}")

        print(f"[VideoCompiler] Successfully assembled short: {output_mp4_path}")
        return output_mp4_path

import asyncio
import os
from pathlib import Path
from typing import Dict, Any, List

class StickVoiceService:
    """
    Multi-character voice synthesis engine for 2D stick-figure shorts.
    Uses Edge-TTS with customizable rate, pitch, and emotion inflection per character.
    """

    VOICE_DEFAULTS = {
        "en-US-GuyNeural": {"pitch": "+4Hz", "rate": "+10%"},
        "en-US-ChristopherNeural": {"pitch": "-2Hz", "rate": "+4%"},
        "en-US-JennyNeural": {"pitch": "+6Hz", "rate": "+8%"},
        "en-US-EricNeural": {"pitch": "+2Hz", "rate": "+12%"}
    }

    @classmethod
    async def synthesize_dialogue_clips(
        cls,
        dialogues: List[Dict[str, Any]],
        output_dir: Path
    ) -> List[Dict[str, Any]]:
        """Synthesizes individual audio files for each line in the script."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        results = []

        import edge_tts

        for idx, d in enumerate(dialogues):
            spk_id = d.get("speaker_id", "char")
            voice_id = d.get("voice_id", "en-US-GuyNeural")
            text = d.get("text", "")
            out_file = output_dir / f"diag_{idx+1}_{spk_id}.mp3"

            # Apply personality pitch/rate
            tune = cls.VOICE_DEFAULTS.get(voice_id, {"pitch": "+0Hz", "rate": "+0%"})

            try:
                communicate = edge_tts.Communicate(
                    text=text,
                    voice=voice_id,
                    rate=tune["rate"],
                    pitch=tune["pitch"]
                )
                await communicate.save(str(out_file))
            except Exception as e:
                print(f"[VoiceService] Edge-TTS notice ({e}), creating speech tone...")
                # Fallback: create short silent/beep tone using imageio-ffmpeg
                import imageio_ffmpeg, subprocess
                dur = max(1.0, d.get("end_second", 2.0) - d.get("start_second", 0.0))
                cmd = [
                    imageio_ffmpeg.get_ffmpeg_exe(), "-y",
                    "-f", "lavfi", "-i", f"sine=frequency=440:duration={dur}",
                    "-c:a", "libmp3lame", str(out_file)
                ]
                subprocess.run(cmd, capture_output=True)

            results.append({
                "index": idx,
                "speaker_id": spk_id,
                "text": text,
                "audio_path": str(out_file),
                "start": d.get("start_second", 0.0),
                "end": d.get("end_second", 3.0)
            })

        return results

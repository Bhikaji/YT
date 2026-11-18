import os
import asyncio
from pathlib import Path
from typing import Optional, Dict
import edge_tts
from backend.app.config import settings

class VoiceEngine:
    """Neural Voice Generation Engine supporting Edge-TTS and ElevenLabs."""
    
    DEFAULT_VOICE_MAP = {
        "hero_male": "en-US-ChristopherNeural",
        "hero_female": "en-US-AnaNeural",
        "villain_male": "en-US-GuyNeural",
        "comic_relief": "en-US-EricNeural",
        "child_boy": "en-US-ChristopherNeural",
        "narrator": "en-US-BrianNeural"
    }

    EMOTION_SSML_MAP = {
        "whisper": {"pitch": "-4Hz", "rate": "-15%", "volume": "-20%"},
        "excited": {"pitch": "+8Hz", "rate": "+15%", "volume": "+10%"},
        "terrified": {"pitch": "+12Hz", "rate": "+25%", "volume": "+5%"},
        "angry": {"pitch": "+4Hz", "rate": "+10%", "volume": "+15%"},
        "sad": {"pitch": "-6Hz", "rate": "-20%", "volume": "-15%"},
        "sarcastic": {"pitch": "-2Hz", "rate": "-5%", "volume": "+0%"},
        "neutral": {"pitch": "+0Hz", "rate": "+0%", "volume": "+0%"}
    }

    @classmethod
    async def generate_speech(
        cls,
        text: str,
        voice_id: str = "en-US-ChristopherNeural",
        emotion: str = "neutral",
        output_path: Optional[str] = None
    ) -> str:
        """
        Synthesizes speech with pitch/rate/volume emotion modulation.
        Returns the absolute path to the generated audio file.
        """
        if not output_path:
            filename = f"voice_{abs(hash(text))}_{emotion}.mp3"
            output_dir = settings.ASSETS_DIR / "audio" / "voices"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(output_dir / filename)

        emotion_cfg = cls.EMOTION_SSML_MAP.get(emotion.lower(), cls.EMOTION_SSML_MAP["neutral"])
        pitch = emotion_cfg["pitch"]
        rate = emotion_cfg["rate"]
        volume = emotion_cfg["volume"]

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice_id,
            pitch=pitch,
            rate=rate,
            volume=volume
        )
        
        await communicate.save(output_path)
        return output_path

    @classmethod
    async def list_available_voices(cls, language_prefix: str = "en"):
        """Lists available high-quality neural voices filtered by language."""
        all_voices = await edge_tts.list_voices()
        return [
            {
                "name": v["ShortName"],
                "gender": v["Gender"],
                "locale": v["Locale"],
                "friendly_name": v["FriendlyName"]
            }
            for v in all_voices
            if v["Locale"].startswith(language_prefix)
        ]

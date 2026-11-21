"""
Realistic Human Voice Generation Engine.
Generates natural, expressive, human-like character speech with emotion-aware modulation,
realistic speech rhythm, dynamic pitch variations, and authentic pronunciation.
Supports Rangdi Marathi, Hindi, English, and International neural models.
"""

import os
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
import edge_tts

class RealisticHumanVoiceEngine:
    """
    Multilingual Neural Voice Generator with Emotion-Aware Modulation.
    """

    CHARACTER_VOICE_MAP = {
        # Priority 1: Rangdi Marathi
        "mr_rangdi": {
            "stick_bob": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "+8%", "base_pitch": "+3Hz"},
            "stick_prof": {"voice": "mr-IN-AarohiNeural", "gender": "female", "base_rate": "0%", "base_pitch": "0Hz"},
            "stick_sam": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "+12%", "base_pitch": "+5Hz"},
            "stick_alex": {"voice": "mr-IN-AarohiNeural", "gender": "female", "base_rate": "+4%", "base_pitch": "+2Hz"}
        },
        # Priority 2: Hindi
        "hi": {
            "stick_bob": {"voice": "hi-IN-MadhurNeural", "gender": "male", "base_rate": "+6%", "base_pitch": "+2Hz"},
            "stick_prof": {"voice": "hi-IN-SwaraNeural", "gender": "female", "base_rate": "0%", "base_pitch": "0Hz"},
            "stick_sam": {"voice": "hi-IN-MadhurNeural", "gender": "male", "base_rate": "+10%", "base_pitch": "+4Hz"},
            "stick_alex": {"voice": "hi-IN-SwaraNeural", "gender": "female", "base_rate": "+4%", "base_pitch": "+2Hz"}
        },
        # Priority 3: English
        "en": {
            "stick_bob": {"voice": "en-US-GuyNeural", "gender": "male", "base_rate": "+8%", "base_pitch": "+2Hz"},
            "stick_prof": {"voice": "en-US-ChristopherNeural", "gender": "male", "base_rate": "0%", "base_pitch": "0Hz"},
            "stick_sam": {"voice": "en-US-EricNeural", "gender": "male", "base_rate": "+12%", "base_pitch": "+4Hz"},
            "stick_alex": {"voice": "en-US-JennyNeural", "gender": "female", "base_rate": "+5%", "base_pitch": "+2Hz"}
        }
    }

    EMOTION_MODULATION = {
        "shocked": {"rate": "+15%", "pitch": "+8Hz"},
        "excited": {"rate": "+12%", "pitch": "+6Hz"},
        "laughing": {"rate": "+10%", "pitch": "+4Hz"},
        "angry": {"rate": "+15%", "pitch": "-4Hz"},
        "fearful": {"rate": "+14%", "pitch": "+10Hz"},
        "suspicious": {"rate": "-6%", "pitch": "-3Hz"},
        "curious": {"rate": "+2%", "pitch": "+5Hz"},
        "confident": {"rate": "+4%", "pitch": "+0Hz"},
        "surprised": {"rate": "+16%", "pitch": "+7Hz"},
        "sad": {"rate": "-10%", "pitch": "-5Hz"}
    }

    @classmethod
    def get_voice_config_for_character(
        cls,
        character_id: str,
        language_code: str = "mr_rangdi"
    ) -> Dict[str, Any]:
        lang_map = cls.CHARACTER_VOICE_MAP.get(language_code, cls.CHARACTER_VOICE_MAP["mr_rangdi"])
        return lang_map.get(character_id, list(lang_map.values())[0])

    @classmethod
    async def synthesize_dialogue_line(
        cls,
        text: str,
        character_id: str,
        language_code: str,
        emotion: str,
        output_path: Path
    ) -> Path:
        """
        Synthesizes a realistic human dialogue audio clip with emotion-aware pitch and speed modulation.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        config = cls.get_voice_config_for_character(character_id, language_code)
        voice_id = config["voice"]

        # Calculate emotion modulation
        em_mod = cls.EMOTION_MODULATION.get(emotion.lower(), {"rate": "0%", "pitch": "0Hz"})
        rate_str = em_mod["rate"]
        pitch_str = em_mod["pitch"]

        # Call Edge-TTS
        try:
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice_id,
                rate=rate_str,
                pitch=pitch_str
            )
            await communicate.save(str(output_path))
        except Exception as e:
            # Fallback without modulation if pitch string rejected
            communicate = edge_tts.Communicate(text=text, voice=voice_id)
            await communicate.save(str(output_path))

        return output_path

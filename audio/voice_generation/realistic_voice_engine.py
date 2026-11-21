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

from audio.voice_generation.speech_intelligence import (
    RegionalDialectIntelligenceEngine,
    SpeechGenerationIntegrityEngine,
    DialogueRepairEngine
)
from audio.dialogue_coordination.speech_validator import SpeechRecognitionValidator

class RealisticHumanVoiceEngine:
    """
    Multilingual Neural Voice Generator with Emotion-Aware Modulation and Phonetic Integrity.
    """

    CHARACTER_VOICE_MAP = {
        # Priority 1: Varhadi & Rangdi Marathi - Matching demo.mp4 Character Personalities
        "mr_rangdi": {
            # Ganya (गण्या - Energetic comedy hero boy, crisp natural Maharashtrian enunciation)
            "ganya": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "+0%", "base_pitch": "+3Hz"},
            "stick_ganya": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "+0%", "base_pitch": "+3Hz"},
            "stick_bob": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "+0%", "base_pitch": "+3Hz"},

            # Sonya (सोन्या - Playful brother/friend, slightly higher pitch)
            "sonya": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "+1%", "base_pitch": "+1Hz"},
            "stick_sonya": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "+1%", "base_pitch": "+1Hz"},

            # Shanti (शांती / शांताबाई - Authoritative, crisp Maharashtrian mother in saree)
            "shanti": {"voice": "mr-IN-AarohiNeural", "gender": "female", "base_rate": "-2%", "base_pitch": "+4Hz"},
            "varhadi_shanti": {"voice": "mr-IN-AarohiNeural", "gender": "female", "base_rate": "-2%", "base_pitch": "+4Hz"},
            "varhadi_mother": {"voice": "mr-IN-AarohiNeural", "gender": "female", "base_rate": "-2%", "base_pitch": "+4Hz"},

            # Rohya (रोह्या - Sarcastic, mischievous teen friend in bus doorway)
            "rohya": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "+1%", "base_pitch": "+7Hz"},
            "stick_rohya": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "+1%", "base_pitch": "+7Hz"},
            "stick_prof": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "+1%", "base_pitch": "+7Hz"},

            # Yogya (योग्या - Village katta buddy)
            "yogya": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "+0%", "base_pitch": "+5Hz"},
            "stick_yogya": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "+0%", "base_pitch": "+5Hz"},

            # Aakya (आक्या - Dry elder village friend)
            "aakya": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "-2%", "base_pitch": "-3Hz"},
            "stick_aakya": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "-2%", "base_pitch": "-3Hz"},
            "varhadi_uncle": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "-2%", "base_pitch": "-3Hz"},

            "stick_sam": {"voice": "mr-IN-ManoharNeural", "gender": "male", "base_rate": "+0%", "base_pitch": "+0Hz"},
            "stick_alex": {"voice": "mr-IN-AarohiNeural", "gender": "female", "base_rate": "+0%", "base_pitch": "+0Hz"}
        },
        # Priority 2: Hindi
        "hi": {
            "ganya": {"voice": "hi-IN-MadhurNeural", "gender": "male", "base_rate": "+2%", "base_pitch": "+2Hz"},
            "sonya": {"voice": "hi-IN-MadhurNeural", "gender": "male", "base_rate": "+1%", "base_pitch": "+1Hz"},
            "shanti": {"voice": "hi-IN-SwaraNeural", "gender": "female", "base_rate": "+0%", "base_pitch": "+1Hz"},
            "rohya": {"voice": "hi-IN-MadhurNeural", "gender": "male", "base_rate": "+1%", "base_pitch": "-1Hz"},
            "yogya": {"voice": "hi-IN-MadhurNeural", "gender": "male", "base_rate": "+1%", "base_pitch": "+0Hz"},
            "aakya": {"voice": "hi-IN-MadhurNeural", "gender": "male", "base_rate": "-1%", "base_pitch": "-2Hz"},
            "stick_bob": {"voice": "hi-IN-MadhurNeural", "gender": "male", "base_rate": "+3%", "base_pitch": "+1Hz"},
            "stick_prof": {"voice": "hi-IN-MadhurNeural", "gender": "male", "base_rate": "+1%", "base_pitch": "-2Hz"},
            "stick_sam": {"voice": "hi-IN-MadhurNeural", "gender": "male", "base_rate": "+2%", "base_pitch": "+0Hz"},
            "stick_alex": {"voice": "hi-IN-SwaraNeural", "gender": "female", "base_rate": "+1%", "base_pitch": "+0Hz"}
        },
        # Priority 3: English
        "en": {
            "ganya": {"voice": "en-US-GuyNeural", "gender": "male", "base_rate": "+4%", "base_pitch": "+1Hz"},
            "sonya": {"voice": "en-US-GuyNeural", "gender": "male", "base_rate": "+2%", "base_pitch": "+2Hz"},
            "shanti": {"voice": "en-US-JennyNeural", "gender": "female", "base_rate": "+1%", "base_pitch": "+0Hz"},
            "rohya": {"voice": "en-US-ChristopherNeural", "gender": "male", "base_rate": "+0%", "base_pitch": "+0Hz"},
            "yogya": {"voice": "en-US-GuyNeural", "gender": "male", "base_rate": "+1%", "base_pitch": "+0Hz"},
            "aakya": {"voice": "en-US-EricNeural", "gender": "male", "base_rate": "-1%", "base_pitch": "-1Hz"},
            "stick_bob": {"voice": "en-US-GuyNeural", "gender": "male", "base_rate": "+4%", "base_pitch": "+1Hz"},
            "stick_prof": {"voice": "en-US-ChristopherNeural", "gender": "male", "base_rate": "+0%", "base_pitch": "+0Hz"},
            "stick_sam": {"voice": "en-US-EricNeural", "gender": "male", "base_rate": "+5%", "base_pitch": "+1Hz"},
            "stick_alex": {"voice": "en-US-JennyNeural", "gender": "female", "base_rate": "+2%", "base_pitch": "+0Hz"}
        }
    }

    EMOTION_MODULATION = {
        "shocked": {"rate": "+2%", "pitch": "+1Hz"},
        "excited": {"rate": "+2%", "pitch": "+1Hz"},
        "laughing": {"rate": "+2%", "pitch": "+0Hz"},
        "angry": {"rate": "+1%", "pitch": "-1Hz"},
        "fearful": {"rate": "+2%", "pitch": "+1Hz"},
        "cry": {"rate": "-1%", "pitch": "+2Hz"},
        "crying": {"rate": "-1%", "pitch": "+2Hz"},
        "suspicious": {"rate": "-2%", "pitch": "-1Hz"},
        "curious": {"rate": "+1%", "pitch": "+0Hz"},
        "confident": {"rate": "+1%", "pitch": "+0Hz"},
        "surprised": {"rate": "+2%", "pitch": "+1Hz"},
        "sad": {"rate": "-2%", "pitch": "-1Hz"}
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
        Guarantees strictly valid Edge-TTS rate and pitch parameters with explicit sign prefixes (+/-).
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        config = cls.get_voice_config_for_character(character_id, language_code)
        voice_id = config["voice"]

        # Prepare high-intelligibility spoken text (Two-Tier Architecture)
        spoken_text = SpeechGenerationIntegrityEngine.prepare_tts_prompt(text, dialect="varhadi")

        # Base character parameters
        base_rate_val = int(config.get("base_rate", "+0%").replace("%", ""))
        base_pitch_val = int(config.get("base_pitch", "+0Hz").replace("Hz", ""))

        # Emotion modulation deltas (subtle modulation preserving consonant articulation)
        em_mod = cls.EMOTION_MODULATION.get(emotion.lower(), {"rate": "+0%", "pitch": "+0Hz"})
        em_rate_val = int(em_mod.get("rate", "+0%").replace("%", ""))
        em_pitch_val = int(em_mod.get("pitch", "+0Hz").replace("Hz", ""))

        # Combined modulation values - rate clamped to prevent phoneme swallowing
        final_rate_val = base_rate_val + em_rate_val
        final_pitch_val = base_pitch_val + em_pitch_val

        raw_rate_str = f"{final_rate_val:+d}%"
        rate_str = SpeechGenerationIntegrityEngine.enforce_rate_integrity(raw_rate_str)
        pitch_str = f"{final_pitch_val:+d}Hz"

        # Call Edge-TTS with phonetic spoken text
        try:
            communicate = edge_tts.Communicate(
                text=spoken_text,
                voice=voice_id,
                rate=rate_str,
                pitch=pitch_str
            )
            await communicate.save(str(output_path))
        except Exception:
            # Fallback without modulation if any error
            communicate = edge_tts.Communicate(text=spoken_text, voice=voice_id)
            await communicate.save(str(output_path))

        # Audio Quality & Intelligibility Check
        try:
            val_report = SpeechRecognitionValidator.validate_dialogue_audio(output_path, spoken_text)
            if not val_report.get("passed", True):
                print(f"[VoiceEngine] Warning: Speech clarity check below threshold for: '{text[:30]}...'")
        except Exception:
            pass

        return output_path

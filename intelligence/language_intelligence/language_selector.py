"""
Audience-Based Autonomous Language Selection Engine.
Selects target language based on geographic audience distribution, viewer demographics,
channel performance history, and user-configured language priorities.

Priorities:
1. Rangdi Marathi (Maharashtra / Regional Indian Focus)
2. Hindi (India-Wide / North-Western Urban)
3. English & International (US, UK, Europe, Latin America, East Asia)
"""

from typing import Dict, Any, Optional

class LanguageSelectionEngine:
    """
    Intelligent language selection and audience geo-matching engine.
    """

    GEO_TO_LANGUAGE = {
        "MH": "mr_rangdi",       # Maharashtra
        "MAHARASHTRA": "mr_rangdi",
        "IN_MH": "mr_rangdi",
        "PUNE": "mr_rangdi",
        "MUMBAI": "mr_rangdi",
        "IN": "mr_rangdi",       # Default India strategy defaults to Rangdi Marathi as Priority 1
        "IN_HINDI": "hi",        # North India Hindi belt
        "US": "en",              # United States
        "GB": "en",              # United Kingdom
        "UK": "en",
        "CA": "en",              # Canada
        "AU": "en",              # Australia
        "ES": "es",              # Spain
        "BR": "pt",              # Brazil
        "FR": "fr",              # France
        "DE": "de",              # Germany
        "JP": "ja",              # Japan
        "KR": "ko",              # South Korea
        "WORLDWIDE": "mr_rangdi" # Priority 1 default
    }

    LANGUAGE_METADATA = {
        "mr_rangdi": {
            "name": "Rangdi Marathi",
            "native_name": "रांगडी मराठी",
            "priority": 1,
            "default_male_voice": "mr-IN-ManoharNeural",
            "default_female_voice": "mr-IN-AarohiNeural",
            "script_direction": "ltr",
            "tone": "conversational_humorous_witty"
        },
        "hi": {
            "name": "Conversational Hindi",
            "native_name": "हिन्दी",
            "priority": 2,
            "default_male_voice": "hi-IN-MadhurNeural",
            "default_female_voice": "hi-IN-SwaraNeural",
            "script_direction": "ltr",
            "tone": "energetic_engaging_relatable"
        },
        "en": {
            "name": "English",
            "native_name": "English",
            "priority": 3,
            "default_male_voice": "en-US-GuyNeural",
            "default_female_voice": "en-US-JennyNeural",
            "script_direction": "ltr",
            "tone": "sharp_punchy_witty"
        },
        "es": {"name": "Spanish", "native_name": "Español", "priority": 4, "default_male_voice": "es-ES-AlvaroNeural"},
        "pt": {"name": "Portuguese", "native_name": "Português", "priority": 4, "default_male_voice": "pt-BR-AntonioNeural"},
        "fr": {"name": "French", "native_name": "Français", "priority": 4, "default_male_voice": "fr-FR-HenriNeural"},
        "de": {"name": "German", "native_name": "Deutsch", "priority": 4, "default_male_voice": "de-DE-ConradNeural"},
        "ja": {"name": "Japanese", "native_name": "日本語", "priority": 4, "default_male_voice": "ja-JP-KeitaNeural"},
        "ko": {"name": "Korean", "native_name": "한국어", "priority": 4, "default_male_voice": "ko-KR-InJoonNeural"}
    }

    @classmethod
    def select_language_for_target(
        cls,
        target_geo: str = "IN",
        explicit_language: Optional[str] = None,
        channel_priority_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Determines the optimal language code, regional metadata, and neural voice models.
        """
        if explicit_language and explicit_language in cls.LANGUAGE_METADATA:
            lang_code = explicit_language
        elif channel_priority_override and channel_priority_override in cls.LANGUAGE_METADATA:
            lang_code = channel_priority_override
        else:
            geo_upper = (target_geo or "IN").upper().strip()
            lang_code = cls.GEO_TO_LANGUAGE.get(geo_upper, "mr_rangdi")

        meta = cls.LANGUAGE_METADATA.get(lang_code, cls.LANGUAGE_METADATA["mr_rangdi"])
        return {
            "language_code": lang_code,
            "language_name": meta["name"],
            "native_name": meta["native_name"],
            "priority": meta["priority"],
            "default_male_voice": meta.get("default_male_voice"),
            "default_female_voice": meta.get("default_female_voice"),
            "tone": meta.get("tone", "conversational")
        }

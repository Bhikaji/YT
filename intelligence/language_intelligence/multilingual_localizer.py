"""
Multilingual Video Localization Engine.
Produces localized scripts across Rangdi Marathi, Hindi, and English with matching voice profiles,
culturally adapted jokes, and native subtitles.
"""

from typing import Dict, Any, List
from intelligence.language_intelligence.rangdi_marathi_engine import RangdiMarathiEngine
from intelligence.language_intelligence.hindi_dialogue_engine import HindiDialogueEngine
from intelligence.script_generation.story_engine import StickStoryEngine
from intelligence.script_generation.script_schema import StickFigureScript

class MultilingualLocalizer:
    """
    Coordinates multi-language localization for a single topic or video asset.
    """

    @classmethod
    def generate_script_for_language(
        cls,
        topic: str,
        category: str = "technology",
        language_code: str = "mr_rangdi"
    ) -> StickFigureScript:
        """Generates a culturally adapted screenplay in the requested language."""
        if language_code == "mr_rangdi":
            return RangdiMarathiEngine.generate_rangdi_marathi_script(topic=topic, category=category)
        elif language_code == "hi":
            return HindiDialogueEngine.generate_hindi_script(topic=topic, category=category)
        else:
            return StickStoryEngine.generate_30s_script(topic=topic, category=category)

    @classmethod
    def generate_all_language_variants(
        cls,
        topic: str,
        category: str = "technology"
    ) -> Dict[str, StickFigureScript]:
        """
        Creates all 3 localized production versions (Rangdi Marathi, Hindi, English).
        """
        return {
            "mr_rangdi": RangdiMarathiEngine.generate_rangdi_marathi_script(topic, category),
            "hi": HindiDialogueEngine.generate_hindi_script(topic, category),
            "en": StickStoryEngine.generate_30s_script(topic, category)
        }

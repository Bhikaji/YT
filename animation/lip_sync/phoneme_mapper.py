from typing import Dict, Any, Tuple

class PhonemeMapper:
    """
    Phoneme-to-Mouth Shape Mapping for 2D Stick-Figure Characters.
    Provides precise (width, height, curve) vector parameters for mouth drawing.
    """

    MOUTH_SHAPES: Dict[str, Dict[str, Any]] = {
        "A_I": {"width": 24, "height": 20, "open": True, "shape": "oval_vertical"},
        "E": {"width": 26, "height": 12, "open": True, "shape": "wide_slit"},
        "O_U": {"width": 18, "height": 20, "open": True, "shape": "circle_pucker"},
        "M_B_P": {"width": 18, "height": 2, "open": False, "shape": "closed_line"},
        "F_V": {"width": 20, "height": 8, "open": True, "shape": "wide_slit"},
        "L_TH": {"width": 22, "height": 14, "open": True, "shape": "oval_vertical"},
        "REST": {"width": 18, "height": 2, "open": False, "shape": "neutral_line"},
        "SCREAM": {"width": 30, "height": 28, "open": True, "shape": "oval_vertical"},
        "LAUGH": {"width": 34, "height": 24, "open": True, "shape": "oval_vertical"}
    }

    @classmethod
    def get_mouth_for_phoneme(cls, phoneme_key: str) -> Dict[str, Any]:
        return cls.MOUTH_SHAPES.get(phoneme_key, cls.MOUTH_SHAPES["REST"])

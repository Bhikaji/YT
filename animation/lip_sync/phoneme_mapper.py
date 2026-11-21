from typing import Dict, Any, Tuple

class PhonemeMapper:
    """
    Phoneme-to-Mouth Shape Mapping for 2D Stick-Figure Characters.
    Provides precise (width, height, curve) vector parameters for mouth drawing.
    """

    MOUTH_SHAPES: Dict[str, Dict[str, Any]] = {
        "A_I": {"width": 16, "height": 16, "open": True, "shape": "oval_vertical"},
        "E": {"width": 22, "height": 8, "open": True, "shape": "wide_slit"},
        "O_U": {"width": 14, "height": 18, "open": True, "shape": "circle_pucker"},
        "M_B_P": {"width": 18, "height": 2, "open": False, "shape": "closed_line"},
        "F_V": {"width": 16, "height": 6, "open": True, "shape": "teeth_press"},
        "L_TH": {"width": 18, "height": 12, "open": True, "shape": "tongue_visible"},
        "REST": {"width": 14, "height": 2, "open": False, "shape": "neutral_line"},
        "SCREAM": {"width": 26, "height": 28, "open": True, "shape": "huge_circle"}
    }

    @classmethod
    def get_mouth_for_phoneme(cls, phoneme_key: str) -> Dict[str, Any]:
        return cls.MOUTH_SHAPES.get(phoneme_key, cls.MOUTH_SHAPES["REST"])

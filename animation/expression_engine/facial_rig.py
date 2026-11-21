from typing import Dict, Any, Tuple

class FacialRig:
    """
    Dedicated 2D Stick-Figure Facial Expression Engine.
    Coordinates eyes, eyebrows, pupils, mouth shapes, and emotive marks (sweat, tears, anger veins).
    Supports all 15 required expressions.
    """

    EXPRESSION_PRESETS: Dict[str, Dict[str, Any]] = {
        "happy": {
            "eye_type": "arc_up",  # ^ ^ cheerful eyes
            "pupil_offset": (0, 0),
            "eyebrow_angle": 0,
            "eyebrow_offset_y": -4,
            "mouth_type": "wide_smile",
            "extras": ["blush"]
        },
        "sad": {
            "eye_type": "droop",
            "pupil_offset": (0, 2),
            "eyebrow_angle": -20,  # angled up in center
            "eyebrow_offset_y": -2,
            "mouth_type": "frown",
            "extras": []
        },
        "angry": {
            "eye_type": "squint",
            "pupil_offset": (0, 0),
            "eyebrow_angle": 25,  # furrowed sharply downward in center
            "eyebrow_offset_y": 2,
            "mouth_type": "grimace",
            "extras": ["anger_mark"]
        },
        "surprise": {
            "eye_type": "wide_circle",
            "pupil_offset": (0, -2),
            "eyebrow_angle": -5,
            "eyebrow_offset_y": -12,
            "mouth_type": "small_o",
            "extras": []
        },
        "shock": {
            "eye_type": "huge_circle",
            "pupil_offset": (0, 0),
            "eyebrow_angle": -10,
            "eyebrow_offset_y": -16,
            "mouth_type": "huge_gasp",
            "extras": ["sweat_drop", "speed_lines"]
        },
        "shocked": {
            "eye_type": "huge_circle",
            "pupil_offset": (0, 0),
            "eyebrow_angle": -10,
            "eyebrow_offset_y": -16,
            "mouth_type": "huge_gasp",
            "extras": ["sweat_drop", "speed_lines"]
        },
        "confused": {
            "eye_type": "one_big_one_small",
            "pupil_offset": (2, -1),
            "eyebrow_angle": 20,  # one raised, one furrowed
            "eyebrow_offset_y": -4,
            "mouth_type": "wavy_line",
            "extras": ["question_mark"]
        },
        "fear": {
            "eye_type": "wide_circle",
            "pupil_offset": (0, 2),
            "eyebrow_angle": -18,
            "eyebrow_offset_y": -10,
            "mouth_type": "tremble_open",
            "extras": ["sweat_drop"]
        },
        "fearful": {
            "eye_type": "wide_circle",
            "pupil_offset": (0, 2),
            "eyebrow_angle": -18,
            "eyebrow_offset_y": -10,
            "mouth_type": "tremble_open",
            "extras": ["sweat_drop"]
        },
        "excited": {
            "eye_type": "star_eyes",
            "pupil_offset": (0, 0),
            "eyebrow_angle": -8,
            "eyebrow_offset_y": -8,
            "mouth_type": "open_smile",
            "extras": ["sparkles"]
        },
        "curious": {
            "eye_type": "circle",
            "pupil_offset": (3, -1),
            "eyebrow_angle": -8,
            "eyebrow_offset_y": -6,
            "mouth_type": "small_smile",
            "extras": []
        },
        "suspicious": {
            "eye_type": "narrow_squint",
            "pupil_offset": (4, 0),
            "eyebrow_angle": 15,
            "eyebrow_offset_y": 0,
            "mouth_type": "smirk_left",
            "extras": []
        },
        "laughing": {
            "eye_type": "arc_down",  # closed laughing eyes ><
            "pupil_offset": (0, 0),
            "eyebrow_angle": 0,
            "eyebrow_offset_y": -6,
            "mouth_type": "open_laugh",
            "extras": ["happy_tears"]
        },
        "crying": {
            "eye_type": "closed_stream",
            "pupil_offset": (0, 0),
            "eyebrow_angle": -20,
            "eyebrow_offset_y": -4,
            "mouth_type": "wailing",
            "extras": ["waterfall_tears"]
        },
        "thinking": {
            "eye_type": "circle",
            "pupil_offset": (-3, -4),  # looking up and left
            "eyebrow_angle": -12,
            "eyebrow_offset_y": -4,
            "mouth_type": "pucker_side",
            "extras": ["thought_bubbles"]
        },
        "disappointed": {
            "eye_type": "flat_top",
            "pupil_offset": (0, 3),
            "eyebrow_angle": 8,
            "eyebrow_offset_y": 2,
            "mouth_type": "flat_line",
            "extras": ["dark_cloud"]
        },
        "confident": {
            "eye_type": "half_closed",
            "pupil_offset": (0, 0),
            "eyebrow_angle": 5,
            "eyebrow_offset_y": -5,
            "mouth_type": "smirk",
            "extras": ["gleam"]
        }
    }

    @classmethod
    def get_expression(cls, name: str) -> Dict[str, Any]:
        return cls.EXPRESSION_PRESETS.get(name.lower(), cls.EXPRESSION_PRESETS["curious"])

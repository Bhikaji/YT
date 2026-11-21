from typing import Dict, Any, List

class CharacterPersonalityLibrary:
    """
    Library of 20 Predefined Stick-Figure Personalities.
    Controls movement energy, gesture frequency, voice pitch, and default expressions.
    """

    PERSONALITIES: Dict[str, Dict[str, Any]] = {
        "funny": {
            "name": "Funny Character",
            "energy": 0.9,
            "default_expression": "laughing",
            "gesture_frequency": 0.85,
            "preferred_actions": ["slapstick_react", "dance", "wave"],
            "speech_rate": "+10%",
            "pitch": "+5Hz"
        },
        "intelligent": {
            "name": "Intelligent Character",
            "energy": 0.5,
            "default_expression": "thinking",
            "gesture_frequency": 0.4,
            "preferred_actions": ["point", "think", "inspect"],
            "speech_rate": "0%",
            "pitch": "0Hz"
        },
        "innocent": {
            "name": "Innocent Character",
            "energy": 0.7,
            "default_expression": "curious",
            "gesture_frequency": 0.6,
            "preferred_actions": ["wave", "stand", "jump"],
            "speech_rate": "+5%",
            "pitch": "+10Hz"
        },
        "angry": {
            "name": "Angry Character",
            "energy": 0.85,
            "default_expression": "angry",
            "gesture_frequency": 0.75,
            "preferred_actions": ["point", "stamp_foot", "cross_arms"],
            "speech_rate": "+15%",
            "pitch": "-5Hz"
        },
        "confused": {
            "name": "Confused Character",
            "energy": 0.4,
            "default_expression": "confused",
            "gesture_frequency": 0.5,
            "preferred_actions": ["scratch_head", "shrug", "look_around"],
            "speech_rate": "-5%",
            "pitch": "+3Hz"
        },
        "curious": {
            "name": "Curious Character",
            "energy": 0.75,
            "default_expression": "curious",
            "gesture_frequency": 0.7,
            "preferred_actions": ["inspect", "lean_forward", "point"],
            "speech_rate": "+5%",
            "pitch": "+5Hz"
        },
        "emotional": {
            "name": "Emotional Character",
            "energy": 0.8,
            "default_expression": "crying",
            "gesture_frequency": 0.8,
            "preferred_actions": ["facepalm", "hands_on_cheeks", "droop"],
            "speech_rate": "0%",
            "pitch": "+8Hz"
        },
        "serious": {
            "name": "Serious Character",
            "energy": 0.4,
            "default_expression": "serious",
            "gesture_frequency": 0.3,
            "preferred_actions": ["cross_arms", "straight_stand", "nod"],
            "speech_rate": "-10%",
            "pitch": "-8Hz"
        },
        "overconfident": {
            "name": "Overconfident Character",
            "energy": 0.85,
            "default_expression": "confident",
            "gesture_frequency": 0.8,
            "preferred_actions": ["hands_on_hips", "smirk", "point_self"],
            "speech_rate": "+10%",
            "pitch": "+2Hz"
        },
        "lazy": {
            "name": "Lazy Character",
            "energy": 0.2,
            "default_expression": "disappointed",
            "gesture_frequency": 0.15,
            "preferred_actions": ["slouch", "sit", "yawn"],
            "speech_rate": "-15%",
            "pitch": "-10Hz"
        },
        "businessman": {
            "name": "Smart Businessman",
            "energy": 0.65,
            "default_expression": "confident",
            "gesture_frequency": 0.6,
            "preferred_actions": ["hold_briefcase", "check_watch", "point_chart"],
            "speech_rate": "+5%",
            "pitch": "-3Hz"
        },
        "scientist": {
            "name": "Scientist",
            "energy": 0.7,
            "default_expression": "curious",
            "gesture_frequency": 0.7,
            "preferred_actions": ["hold_test_tube", "inspect", "lightbulb_idea"],
            "speech_rate": "+8%",
            "pitch": "+4Hz"
        },
        "teacher": {
            "name": "Teacher",
            "energy": 0.6,
            "default_expression": "happy",
            "gesture_frequency": 0.65,
            "preferred_actions": ["point_board", "explain_hands", "nod"],
            "speech_rate": "-5%",
            "pitch": "-2Hz"
        },
        "student": {
            "name": "Student",
            "energy": 0.65,
            "default_expression": "curious",
            "gesture_frequency": 0.55,
            "preferred_actions": ["raise_hand", "write_notes", "scratch_head"],
            "speech_rate": "+5%",
            "pitch": "+6Hz"
        },
        "techie": {
            "name": "Technology Enthusiast",
            "energy": 0.8,
            "default_expression": "excited",
            "gesture_frequency": 0.8,
            "preferred_actions": ["type_rapidly", "hold_phone", "point_screen"],
            "speech_rate": "+12%",
            "pitch": "+3Hz"
        },
        "customer": {
            "name": "Customer",
            "energy": 0.6,
            "default_expression": "suspicious",
            "gesture_frequency": 0.6,
            "preferred_actions": ["examine_item", "shrug", "reach_wallet"],
            "speech_rate": "0%",
            "pitch": "+2Hz"
        },
        "shopkeeper": {
            "name": "Shopkeeper",
            "energy": 0.75,
            "default_expression": "happy",
            "gesture_frequency": 0.75,
            "preferred_actions": ["present_item", "bow_welcome", "ring_register"],
            "speech_rate": "+5%",
            "pitch": "+3Hz"
        },
        "influencer": {
            "name": "Influencer",
            "energy": 0.95,
            "default_expression": "excited",
            "gesture_frequency": 0.9,
            "preferred_actions": ["selfie_pose", "wave_both_hands", "blow_kiss"],
            "speech_rate": "+15%",
            "pitch": "+12Hz"
        },
        "employee": {
            "name": "Office Employee",
            "energy": 0.45,
            "default_expression": "thinking",
            "gesture_frequency": 0.4,
            "preferred_actions": ["drink_coffee", "slouch_desk", "check_clock"],
            "speech_rate": "-5%",
            "pitch": "-4Hz"
        },
        "narrator": {
            "name": "Narrator",
            "energy": 0.5,
            "default_expression": "confident",
            "gesture_frequency": 0.3,
            "preferred_actions": ["open_arms", "point_scene", "stand"],
            "speech_rate": "0%",
            "pitch": "-5Hz"
        }
    }

    @classmethod
    def get_personality(cls, key: str) -> Dict[str, Any]:
        return cls.PERSONALITIES.get(key, cls.PERSONALITIES["funny"])

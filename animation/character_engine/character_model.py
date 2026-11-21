from typing import Dict, Any, Optional

class StickFigureCharacter:
    """
    Data model & visual specification for a unique 2D stick-figure character.
    Maintains visual continuity and recognizable identities across all episodes.
    """

    def __init__(
        self,
        character_id: str,
        name: str,
        personality_key: str = "funny",
        voice_id: str = "en-US-GuyNeural",
        line_color: str = "#0f172a",
        line_thickness: int = 8,
        head_radius: int = 40,
        torso_length: int = 140,
        upper_arm_length: int = 70,
        forearm_length: int = 65,
        thigh_length: int = 80,
        calf_length: int = 75,
        accessory: Optional[str] = None,  # "red_tie", "blue_tie", "glasses", "sunglasses", "lab_coat", "cap"
        hair_style: Optional[str] = None  # "spiky", "tuft", "curly", "none"
    ):
        self.id = character_id
        self.name = name
        self.personality_key = personality_key
        self.voice_id = voice_id
        self.line_color = line_color
        self.line_thickness = line_thickness
        self.head_radius = head_radius
        self.torso_length = torso_length
        self.upper_arm_length = upper_arm_length
        self.forearm_length = forearm_length
        self.thigh_length = thigh_length
        self.calf_length = calf_length
        self.accessory = accessory
        self.hair_style = hair_style

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "personality_key": self.personality_key,
            "voice_id": self.voice_id,
            "line_color": self.line_color,
            "line_thickness": self.line_thickness,
            "head_radius": self.head_radius,
            "torso_length": self.torso_length,
            "upper_arm_length": self.upper_arm_length,
            "forearm_length": self.forearm_length,
            "thigh_length": self.thigh_length,
            "calf_length": self.calf_length,
            "accessory": self.accessory,
            "hair_style": self.hair_style
        }

    @classmethod
    def get_canonical_library(cls) -> Dict[str, "StickFigureCharacter"]:
        """Canonical cast of iconic, visually distinct stick-figure characters."""
        return {
            "stick_bob": cls(
                character_id="stick_bob",
                name="Bob",
                personality_key="funny",
                voice_id="en-US-GuyNeural",
                line_color="#0f172a",
                line_thickness=9,
                accessory="red_tie",
                hair_style="tuft"
            ),
            "stick_prof": cls(
                character_id="stick_prof",
                name="Prof. Pixel",
                personality_key="scientist",
                voice_id="en-US-ChristopherNeural",
                line_color="#1e293b",
                line_thickness=8,
                accessory="glasses",
                hair_style="spiky"
            ),
            "stick_sam": cls(
                character_id="stick_sam",
                name="Sam",
                personality_key="techie",
                voice_id="en-US-EricNeural",
                line_color="#0f172a",
                line_thickness=8,
                accessory="sunglasses",
                hair_style="spiky"
            ),
            "stick_alex": cls(
                character_id="stick_alex",
                name="Alex",
                personality_key="intelligent",
                voice_id="en-US-JennyNeural",
                line_color="#334155",
                line_thickness=8,
                accessory="blue_tie",
                hair_style="curly"
            )
        }

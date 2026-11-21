from typing import Dict, Any, Optional

class StickFigureCharacter:
    """
    Data model & visual specification for a unique 2D stick-figure character.
    Maintains visual continuity, iconic costumes, and high-contrast recognizable identities across all episodes.
    """

    def __init__(
        self,
        character_id: str,
        name: str,
        personality_key: str = "funny",
        voice_id: str = "en-US-GuyNeural",
        line_color: str = "#0f172a",
        line_thickness: int = 11,
        head_radius: int = 42,
        torso_length: int = 140,
        upper_arm_length: int = 70,
        forearm_length: int = 65,
        thigh_length: int = 80,
        calf_length: int = 75,
        accessory: Optional[str] = None,  # "red_tie", "blue_tie", "glasses", "sunglasses", "lab_coat", "cap"
        hair_style: Optional[str] = None,  # "spiky", "tuft", "curly", "none"
        shirt_color: Optional[str] = "#ffffff",
        shoe_color: str = "#ffffff",
        glove_color: str = "#ffffff"
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
        self.shirt_color = shirt_color
        self.shoe_color = shoe_color
        self.glove_color = glove_color

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
            "hair_style": self.hair_style,
            "shirt_color": self.shirt_color,
            "shoe_color": self.shoe_color,
            "glove_color": self.glove_color
        }

    @classmethod
    def get_canonical_library(cls) -> Dict[str, "StickFigureCharacter"]:
        """Canonical cast of iconic, visually distinct cartoon characters matching demo.mp4."""
        return {
            # 1. Main Boy ("बब्या") - Orange Spiky Hair, Red & White Striped Pill Torso
            "stick_bob": cls(
                character_id="stick_bob",
                name="बब्या",
                personality_key="varhadi_boy",
                voice_id="mr-IN-ManoharNeural",
                line_color="#0f172a",
                line_thickness=8,
                head_radius=40,
                accessory=None,
                hair_style="spiky_orange",
                shirt_color="#dc2626",
                shoe_color="#0f172a",
                glove_color="#ffffff"
            ),
            # 2. Sidekick Friend ("गंप्या") - Purple Swept Hair, Pure White Pill Torso
            "stick_prof": cls(
                character_id="stick_prof",
                name="गंप्या",
                personality_key="varhadi_friend",
                voice_id="mr-IN-ManoharNeural",
                line_color="#0f172a",
                line_thickness=8,
                head_radius=40,
                accessory=None,
                hair_style="purple_swept",
                shirt_color="#ffffff",
                shoe_color="#0f172a",
                glove_color="#ffffff"
            ),
            # 3. Mother ("आई / काकू") - Traditional Brown Bun, Red Bindi, Royal Blue Saree & Violet Blouse
            "varhadi_mother": cls(
                character_id="varhadi_mother",
                name="आई",
                personality_key="varhadi_mother",
                voice_id="mr-IN-AarohiNeural",
                line_color="#0f172a",
                line_thickness=8,
                head_radius=38,
                accessory="red_bindi",
                hair_style="brown_bun",
                shirt_color="#1d4ed8",
                shoe_color="#0f172a",
                glove_color="#ffffff"
            ),
            # 4. Uncle / Father ("काका") - Half Bald, Dark Sunglasses, Vest Jacket
            "varhadi_uncle": cls(
                character_id="varhadi_uncle",
                name="काका",
                personality_key="varhadi_uncle",
                voice_id="mr-IN-ManoharNeural",
                line_color="#0f172a",
                line_thickness=8,
                head_radius=40,
                accessory="sunglasses",
                hair_style="half_bald",
                shirt_color="#1e293b",
                shoe_color="#ffffff",
                glove_color="#ffffff"
            )
        }

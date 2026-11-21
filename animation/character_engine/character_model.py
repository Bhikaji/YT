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
        """
        Canonical cast of iconic, visually distinct cartoon characters matching demo.mp4:
        - ganya (गण्या): Fiery orange spiky hair, bold red-and-white horizontal striped pill torso
        - sonya (सोन्या): Spiky golden hair, yellow-and-white striped pill torso
        - shanti (शांती / शांताबाई): Traditional brown bun, red bindi, royal blue saree, violet blouse, gold border
        - rohya (रोह्या): Sleek purple side-swept hair, crisp pure white pill torso
        - yogya (योग्या): Black tuft hair, cyan pill torso
        - aakya (आक्या): Half bald with dark sunglasses, charcoal vest/jacket
        """
        lib = {
            # 1. Main Hero Boy ("गण्या" / Ganya) - Orange Spiky Hair, Red & White Striped Pill Torso
            "ganya": cls(
                character_id="ganya",
                name="गण्या",
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
            # 2. Mischievous Brother/Friend ("सोन्या" / Sonya) - Golden Striped Torso
            "sonya": cls(
                character_id="sonya",
                name="सोन्या",
                personality_key="varhadi_boy",
                voice_id="mr-IN-ManoharNeural",
                line_color="#0f172a",
                line_thickness=8,
                head_radius=40,
                accessory=None,
                hair_style="spiky_orange",
                shirt_color="#eab308",
                shoe_color="#0f172a",
                glove_color="#ffffff"
            ),
            # 3. Mother ("शांती" / Shanti - शांताबाई) - Royal Blue Saree, Violet Blouse, Red Bindi
            "shanti": cls(
                character_id="shanti",
                name="शांती",
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
            # 4. Sarcastic Best Friend ("रोह्या" / Rohya) - Purple Swept Hair, Solid White Pill Torso
            "rohya": cls(
                character_id="rohya",
                name="रोह्या",
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
            # 5. Village Pal ("योग्या" / Yogya) - Cyan Pill Torso, Black Tuft Hair
            "yogya": cls(
                character_id="yogya",
                name="योग्या",
                personality_key="varhadi_friend",
                voice_id="mr-IN-ManoharNeural",
                line_color="#0f172a",
                line_thickness=8,
                head_radius=40,
                accessory=None,
                hair_style="black_tuft",
                shirt_color="#0284c7",
                shoe_color="#0f172a",
                glove_color="#ffffff"
            ),
            # 6. Village Elder/Katta Bro ("आक्या" / Aakya) - Half Bald, Dark Sunglasses, Vest
            "aakya": cls(
                character_id="aakya",
                name="आक्या",
                personality_key="varhadi_uncle",
                voice_id="mr-IN-ManoharNeural",
                line_color="#0f172a",
                line_thickness=8,
                head_radius=40,
                accessory="sunglasses",
                hair_style="half_bald",
                shirt_color="#1e293b",
                shoe_color="#0f172a",
                glove_color="#ffffff"
            )
        }

        # Backwards-compatible aliases for existing scripts
        lib["stick_bob"] = lib["ganya"]
        lib["stick_ganya"] = lib["ganya"]
        lib["stick_prof"] = lib["rohya"]
        lib["stick_rohya"] = lib["rohya"]
        lib["varhadi_mother"] = lib["shanti"]
        lib["varhadi_shanti"] = lib["shanti"]
        lib["varhadi_uncle"] = lib["aakya"]
        lib["stick_aakya"] = lib["aakya"]
        lib["stick_sonya"] = lib["sonya"]
        lib["stick_yogya"] = lib["yogya"]

        return lib

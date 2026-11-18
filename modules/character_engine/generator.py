"""
Character Engine - Procedural 3D Character Generation & Shader Setup
Compliant with Pixar / DreamWorks / Illumination aesthetic specifications.
"""

from typing import Dict, Any, List, Optional
import json
from pathlib import Path

class CharacterSpecification:
    """Defines the complete anatomical, stylistic, and material parameters of a 3D character."""

    @classmethod
    def get_pixar_style_presets(cls) -> Dict[str, Dict[str, Any]]:
        """
        Returns official production archetypes based on reference artwork:
        - Leo: The curious young adventurer boy
        - Lumi: The magical pink-cyan glowing fox companion
        - Aria: The courageous explorer girl
        - Milo: The brainy young inventor with round glasses
        """
        return {
            "char_leo_001": {
                "character_id": "char_leo_001",
                "name": "Leo",
                "archetype": "adventurer_boy",
                "age_category": "child_10_12",
                "voice_id": "en-US-ChristopherNeural",
                "proportions": {
                    "head_scale": 1.35,  # Stylized larger head
                    "eye_scale": 1.45,   # Large expressive eyes
                    "body_height": 1.30, # meters
                    "limb_proportions": "stylized_slender",
                    "finger_count": 5
                },
                "facial_features": {
                    "eye_color": [0.25, 0.45, 0.65, 1.0],  # Sparkling blue-gray
                    "hair_style": "tousled_sculpted_locks",
                    "hair_color": [0.28, 0.16, 0.08, 1.0],  # Warm chestnut brown
                    "skin_tone": [0.92, 0.74, 0.62, 1.0],
                    "freckles": True,
                    "freckle_density": 0.35,
                    "brow_thickness": 1.2
                },
                "wardrobe": {
                    "primary_outfit": "adventure_hoodie",
                    "top_color": [0.85, 0.22, 0.15, 1.0],  # Warm crimson red
                    "bottom_color": [0.15, 0.25, 0.40, 1.0], # Explorer denim
                    "backpack": {
                        "enabled": True,
                        "color": [0.15, 0.45, 0.55, 1.0],
                        "straps": "leather_brown"
                    },
                    "footwear": "high_top_hikers"
                },
                "shader_properties": {
                    "skin_subsurface_weight": 0.28,
                    "skin_subsurface_radius": [0.35, 0.15, 0.08],
                    "eye_cornea_ior": 1.376,
                    "eye_specular_wetness": 0.95,
                    "hair_anisotropic_sheen": 0.82
                }
            },
            "char_lumi_003": {
                "character_id": "char_lumi_003",
                "name": "Lumi",
                "archetype": "magical_fox_companion",
                "age_category": "companion_creature",
                "voice_id": "en-US-AnaNeural",
                "proportions": {
                    "head_scale": 1.25,
                    "eye_scale": 1.60,   # Oversized anime/pixar emotive eyes
                    "body_height": 0.45, # meters
                    "ear_scale": 1.40,   # Large pointed expressive ears
                    "tail_scale": 1.70   # Enormous fluffy bioluminescent tail
                },
                "facial_features": {
                    "eye_color": [0.10, 0.85, 0.95, 1.0],  # Luminescent cyan
                    "fur_pattern": "gradient_fox",
                    "primary_fur_color": [0.95, 0.20, 0.65, 1.0], # Vibrant magenta pink
                    "secondary_fur_color": [0.20, 0.85, 0.95, 1.0], # Cyan gradient tail & chest
                    "whiskers": True,
                    "snout_style": "soft_curved"
                },
                "wardrobe": {
                    "accessory": "golden_saddle_pouch",
                    "accessory_color": [0.90, 0.75, 0.20, 1.0],
                    "neck_gem": "floating_crystal"
                },
                "shader_properties": {
                    "fur_sheen": 0.90,
                    "bioluminescent_emission": 0.45,
                    "tail_glow_color": [0.30, 0.90, 1.0, 1.0],
                    "eye_glow": 0.25
                }
            },
            "char_aria_002": {
                "character_id": "char_aria_002",
                "name": "Aria",
                "archetype": "explorer_girl",
                "age_category": "child_10_12",
                "voice_id": "en-US-JennyNeural",
                "proportions": {
                    "head_scale": 1.30,
                    "eye_scale": 1.45,
                    "body_height": 1.32,
                    "finger_count": 5
                },
                "facial_features": {
                    "eye_color": [0.20, 0.60, 0.35, 1.0],  # Emerald green
                    "hair_style": "braided_adventurer",
                    "hair_color": [0.12, 0.08, 0.06, 1.0],  # Rich dark espresso
                    "skin_tone": [0.88, 0.70, 0.58, 1.0]
                },
                "wardrobe": {
                    "primary_outfit": "tunic_and_boots",
                    "top_color": [0.75, 0.25, 0.25, 1.0],  # Terracotta red
                    "scarf": "wrapped_wool_scarf",
                    "scarf_color": [0.25, 0.30, 0.35, 1.0],
                    "footwear": "shearling_boots"
                },
                "shader_properties": {
                    "skin_subsurface_weight": 0.26,
                    "skin_subsurface_radius": [0.32, 0.14, 0.07],
                    "eye_specular_wetness": 0.92,
                    "hair_anisotropic_sheen": 0.78
                }
            },
            "char_milo_004": {
                "character_id": "char_milo_004",
                "name": "Milo",
                "archetype": "young_inventor",
                "age_category": "child_9_11",
                "voice_id": "en-US-GuyNeural",
                "proportions": {
                    "head_scale": 1.45,  # Bulbous head for quirky genius look
                    "eye_scale": 1.50,
                    "body_height": 1.15,
                    "glasses": "oversized_round_frames"
                },
                "facial_features": {
                    "eye_color": [0.20, 0.50, 0.75, 1.0],
                    "hair_style": "short_parted_smart",
                    "hair_color": [0.85, 0.65, 0.35, 1.0], # Blond
                    "skin_tone": [0.94, 0.78, 0.66, 1.0]
                },
                "wardrobe": {
                    "primary_outfit": "yellow_tee_and_jeans",
                    "top_color": [0.95, 0.85, 0.15, 1.0],
                    "glasses_color": [0.85, 0.35, 0.15, 1.0],
                    "backpack": {
                        "enabled": True,
                        "color": [0.20, 0.60, 0.30, 1.0]
                    }
                },
                "shader_properties": {
                    "skin_subsurface_weight": 0.25,
                    "glasses_glass_transmission": 0.98,
                    "glasses_glass_ior": 1.52
                }
            }
        }

    @classmethod
    def export_character_spec(cls, character_id: str, output_path: str) -> str:
        """Serializes character spec to JSON."""
        presets = cls.get_pixar_style_presets()
        spec = presets.get(character_id)
        if not spec:
            raise ValueError(f"Unknown character preset: {character_id}")
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(spec, f, indent=2)
        return str(path)

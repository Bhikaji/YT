"""
Character Identity Validator & Topology Hash Engine
Guarantees zero character drift across episodes and seasons.
"""

import hashlib
import json
from typing import Dict, Any, List, Optional, Tuple

class CharacterIdentityValidator:
    """Verifies that 3D character assets conform to strict biometric and topological standards."""

    # Standard ARKit 52 & Rhubarb Viseme Blendshapes required on all head meshes
    REQUIRED_SHAPEKEYS = [
        # Visemes
        "viseme_sil", "viseme_PP", "viseme_FF", "viseme_TH", "viseme_DD",
        "viseme_kk", "viseme_CH", "viseme_SS", "viseme_nn", "viseme_RR",
        "viseme_aa", "viseme_E", "viseme_I", "viseme_O", "viseme_U",
        # Facial Expressions
        "eyeBlinkLeft", "eyeBlinkRight", "eyeWideLeft", "eyeWideRight",
        "browDownLeft", "browDownRight", "browInnerUp", "browOuterUpLeft", "browOuterUpRight",
        "jawOpen", "mouthSmileLeft", "mouthSmileRight", "mouthFrownLeft", "mouthFrownRight"
    ]

    @classmethod
    def compute_mesh_fingerprint(cls, vertex_positions: List[Tuple[float, float, float]], uv_coordinates: Optional[List[Tuple[float, float]]] = None) -> str:
        """
        Calculates SHA-256 fingerprint from vertex topology.
        Any vertex displacement > 0.001 changes the hash, detecting unauthorized mesh alteration.
        """
        hasher = hashlib.sha256()
        for v in vertex_positions:
            hasher.update(f"{v[0]:.3f},{v[1]:.3f},{v[2]:.3f};".encode("utf-8"))
        if uv_coordinates:
            for uv in uv_coordinates:
                hasher.update(f"{uv[0]:.3f},{uv[1]:.3f};".encode("utf-8"))
        return hasher.hexdigest()

    @classmethod
    def validate_blendshapes(cls, available_shapekeys: List[str]) -> Dict[str, Any]:
        """Checks if all required ARKit/Rhubarb shapekeys exist on the character mesh."""
        available_set = set(available_shapekeys)
        missing = [sk for sk in cls.REQUIRED_SHAPEKEYS if sk not in available_set]
        return {
            "is_valid": len(missing) == 0,
            "total_required": len(cls.REQUIRED_SHAPEKEYS),
            "present_count": len(cls.REQUIRED_SHAPEKEYS) - len(missing),
            "missing_shapekeys": missing
        }

    @classmethod
    def audit_character_consistency(cls, canonical_spec: Dict[str, Any], current_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Audits character specs for accidental attribute mutation."""
        mismatches = []
        critical_fields = ["voice_id", "proportions", "facial_features", "archetype"]
        
        for field in critical_fields:
            if canonical_spec.get(field) != current_spec.get(field):
                mismatches.append({
                    "field": field,
                    "expected": canonical_spec.get(field),
                    "found": current_spec.get(field)
                })

        return {
            "consistent": len(mismatches) == 0,
            "character_id": canonical_spec.get("character_id"),
            "mismatches": mismatches
        }

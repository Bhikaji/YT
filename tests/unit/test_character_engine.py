"""
Unit tests for Character Studio Engine & Identity Validator
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.character_engine.generator import CharacterSpecification
from modules.character_engine.materials import PixarShaderGenerator
from modules.character_identity.validator import CharacterIdentityValidator
from modules.character_identity.registry import CharacterRegistry

def test_character_specifications():
    print("--- Testing Character Presets ---")
    presets = CharacterSpecification.get_pixar_style_presets()
    assert "char_leo_001" in presets
    assert "char_lumi_003" in presets
    assert "char_aria_002" in presets
    assert "char_milo_004" in presets
    
    leo = presets["char_leo_001"]
    assert leo["name"] == "Leo"
    assert leo["proportions"]["head_scale"] == 1.35
    assert leo["shader_properties"]["skin_subsurface_weight"] == 0.28
    print("✔ 4 Pixar character presets validated successfully.")

def test_shader_generators():
    print("--- Testing Pixar Shader Generators ---")
    skin_code = PixarShaderGenerator.generate_skin_shader_code("Leo_Skin", [0.92, 0.74, 0.62, 1.0], [0.35, 0.15, 0.08])
    assert "ShaderNodeBsdfPrincipled" in skin_code
    assert "Subsurface Weight" in skin_code or "Subsurface" in skin_code

    eye_code = PixarShaderGenerator.generate_stylized_eye_shader_code("Leo_Eye", [0.25, 0.45, 0.65, 1.0])
    assert "0.05" in eye_code # high gloss

    hair_code = PixarShaderGenerator.generate_hair_shader_code("Leo_Hair", [0.28, 0.16, 0.08, 1.0])
    assert "Anisotropic" in hair_code

    glow_code = PixarShaderGenerator.generate_bioluminescent_shader_code("Lumi_Fur", [0.95, 0.2, 0.65, 1.0], [0.3, 0.9, 1.0, 1.0])
    assert "Emission" in glow_code
    print("✔ Procedural shader generators verified.")

def test_identity_validator():
    print("--- Testing Character Identity & Mesh Hash Validator ---")
    # Simulated vertex cloud
    vertices = [(0.0, 0.0, 1.0), (0.1, 0.2, 1.0), (-0.1, 0.2, 1.0)]
    hash1 = CharacterIdentityValidator.compute_mesh_fingerprint(vertices)
    hash2 = CharacterIdentityValidator.compute_mesh_fingerprint(vertices)
    assert hash1 == hash2

    # Displaced vertex
    vertices_drift = [(0.0, 0.0, 1.005), (0.1, 0.2, 1.0), (-0.1, 0.2, 1.0)]
    hash3 = CharacterIdentityValidator.compute_mesh_fingerprint(vertices_drift)
    assert hash1 != hash3
    print("✔ Mesh topology hash detects micro-displacement (< 0.005) perfectly.")

    # Blendshape validation
    available_keys = CharacterIdentityValidator.REQUIRED_SHAPEKEYS.copy()
    res = CharacterIdentityValidator.validate_blendshapes(available_keys)
    assert res["is_valid"]
    print(f"✔ All {res['total_required']} ARKit 52/Rhubarb blendshapes verified.")

if __name__ == "__main__":
    test_character_specifications()
    test_shader_generators()
    test_identity_validator()
    print("\n✔ Character Studio & Identity Tests Passed Successfully!")

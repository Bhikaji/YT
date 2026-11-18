"""
Unit tests for Scene Director, Environment Biomes, and Episode Engine
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.scene_director.camera_director import CinematicCameraDirector
from modules.environment_engine.procedural_biomes import ProceduralBiomes
from modules.episode_engine.builder import EpisodeEngine

def test_camera_presets():
    print("--- Testing Cinematic Camera Director ---")
    for preset_name in ["ESTABLISHING_WIDE", "MEDIUM_TWO_SHOT", "CLOSE_UP_EMOTION", "HERO_LOW_ANGLE", "ACTION_TRACKING"]:
        script = CinematicCameraDirector.generate_camera_setup_script(f"Cam_{preset_name}", preset_name)
        assert "bpy.data.cameras.new" in script
        assert "TRACK_TO" in script
    print("✔ 5 Hollywood & Pixar camera presets generated successfully.")

def test_biomes():
    print("--- Testing Procedural Biomes ---")
    for biome in ["BIOLUMINESCENT_FOREST", "CRYSTAL_CAVERN", "WATERFALL_LOG_CROSSING", "NIGHT_LANTERN_VALLEY", "ALPINE_MEADOW"]:
        script = ProceduralBiomes.generate_environment_script(biome)
        assert "ShaderNodeVolumeScatter" in script
        assert "SunLight" in script
    print("✔ All 5 stylized fantasy biomes generated with volumetric atmospheres.")

def test_episode_beat_sheet():
    print("--- Testing Episode Beat Sheets ---")
    short_beats = EpisodeEngine.generate_beat_sheet(format_type="SHORT")
    assert len(short_beats) == 3
    assert "Viral Hook" in short_beats[0]["beat_name"]

    long_beats = EpisodeEngine.generate_beat_sheet(format_type="LONG_FORM")
    assert len(long_beats) == 4
    print("✔ Short and long-form narrative beat sheets verified.")

if __name__ == "__main__":
    test_camera_presets()
    test_biomes()
    test_episode_beat_sheet()
    print("\n✔ Scene & Camera Tests Passed Successfully!")

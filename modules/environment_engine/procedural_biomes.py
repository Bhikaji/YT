"""
Procedural 3D Environment & Biome Generator
Constructs volumetric atmospheric lighting, skyboxes, and prop arrangements for fantasy worlds.
"""

from typing import Dict, Any, List

class ProceduralBiomes:
    """Environment presets based on reference artwork."""

    BIOMES = {
        "BIOLUMINESCENT_FOREST": {
            "name": "Bioluminescent Forest",
            "world_color": [0.02, 0.04, 0.08, 1.0],  # Deep twilight indigo
            "fog_density": 0.025,
            "fog_color": [0.15, 0.35, 0.55, 1.0],
            "sun_energy": 0.5,
            "sun_color": [0.85, 0.45, 0.65],  # Soft pink dawn
            "ambient_particles": "bioluminescent_spores",
            "key_props": ["giant_mushrooms", "glowing_flora", "mossy_rocks"]
        },
        "CRYSTAL_CAVERN": {
            "name": "Crystal Cavern & Bridge",
            "world_color": [0.01, 0.02, 0.05, 1.0],
            "fog_density": 0.035,
            "fog_color": [0.05, 0.65, 0.85, 1.0],  # Cyan glow
            "sun_energy": 0.0,
            "sun_color": [0.10, 0.65, 0.85],
            "ambient_particles": "sparkling_crystals",
            "key_props": ["crystal_bridge", "cavern_stalactites", "glowing_minerals"]
        },
        "WATERFALL_LOG_CROSSING": {
            "name": "Sunlit Waterfall Log Crossing",
            "world_color": [0.45, 0.65, 0.85, 1.0],  # Vibrant morning sky
            "fog_density": 0.015,
            "fog_color": [0.95, 0.95, 0.85, 1.0],  # Volumetric god-rays
            "sun_energy": 4.5,
            "sun_color": [1.0, 0.92, 0.75],  # Warm golden sunlight
            "ambient_particles": "water_mist",
            "key_props": ["waterfall_cascade", "mossy_log_bridge", "ancient_pines"]
        },
        "NIGHT_LANTERN_VALLEY": {
            "name": "Night Mountain Lantern Valley",
            "world_color": [0.01, 0.02, 0.06, 1.0],  # Deep starry blue
            "fog_density": 0.018,
            "fog_color": [0.10, 0.15, 0.30, 1.0],
            "sun_energy": 0.2,
            "sun_color": [0.65, 0.75, 1.0],  # Moonlight
            "ambient_particles": "floating_paper_lanterns",
            "key_props": ["volcanic_peaks", "floating_lanterns", "glowing_embers"]
        },
        "ALPINE_MEADOW": {
            "name": "Sunny Alpine Meadow",
            "world_color": [0.40, 0.70, 0.95, 1.0],  # Bright crisp blue
            "fog_density": 0.005,
            "sun_energy": 5.0,
            "sun_color": [1.0, 0.98, 0.90],
            "ambient_particles": "wildflower_petals",
            "key_props": ["snowy_peaks", "wildflowers", "rolling_grass"]
        }
    }

    @classmethod
    def generate_environment_script(cls, biome_key: str) -> str:
        """
        Generates Blender bpy code to configure World background shader, Sun lamp, and volumetric scattering.
        """
        b = cls.BIOMES.get(biome_key, cls.BIOMES["BIOLUMINESCENT_FOREST"])
        return f'''
def setup_environment_{biome_key.lower()}():
    import bpy
    world = bpy.context.scene.world or bpy.data.worlds.new("EnvironmentWorld")
    bpy.context.scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()

    # Background
    bg = nodes.new(type='ShaderNodeBackground')
    bg.inputs['Color'].default_value = {b["world_color"]}
    bg.inputs['Strength'].default_value = 0.8

    # World Output
    out = nodes.new(type='ShaderNodeOutputWorld')
    links.new(bg.outputs['Background'], out.inputs['Surface'])

    # Volumetric Atmosphere
    volume = nodes.new(type='ShaderNodeVolumeScatter')
    volume.inputs['Density'].default_value = {b["fog_density"]}
    if 'Color' in volume.inputs:
        volume.inputs['Color'].default_value = {b.get("fog_color", [1.0, 1.0, 1.0, 1.0])}
    links.new(volume.outputs['Volume'], out.inputs['Volume'])

    # Key Directional Sun Light
    sun_data = bpy.data.lights.new(name="SunLight", type='SUN')
    sun_data.energy = {b["sun_energy"]}
    sun_data.color = {b.get("sun_color", [1.0, 1.0, 1.0])[:3]}
    sun_obj = bpy.data.objects.new(name="SunLight", object_data=sun_data)
    bpy.context.collection.objects.link(sun_obj)
    sun_obj.rotation_euler = (0.785, 0.35, 0.5)

    return world
'''

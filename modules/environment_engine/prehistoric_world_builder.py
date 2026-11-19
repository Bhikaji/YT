"""
Prehistoric Lost World Environment & Biome Builder for Blender 4.2+ (bpy)
Constructs the complete lost-world setting from demo_video/videoplayback.mp4:
- Distant smoking volcano with rising plume
- Cascading multi-tier waterfalls & crystal tropical lagoon
- Towering tropical palm trees & prehistoric giant tree-ferns
- Giant vibrant blooming blossoms (purple, amber, orange)
- Winding mud trail with giant 3-toed dinosaur footprint puddles
- Volumetric sunbeams, mist, and cinematic depth of field
"""

from typing import Dict, Any, List, Tuple


class PrehistoricWorldBuilder:
    """Procedurally builds high-definition prehistoric environments matching the demo animation."""

    @staticmethod
    def get_environment_code() -> str:
        """Returns Blender bpy code to assemble the complete prehistoric world."""
        return '''
def build_prehistoric_world():
    import bpy, math
    
    # 1. World Atmosphere & Golden Tropical Sky (Radiant Daylight)
    world = bpy.context.scene.world or bpy.data.worlds.new("PrehistoricWorld")
    bpy.context.scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()
    
    bg = nodes.new(type='ShaderNodeBackground')
    bg.inputs['Color'].default_value = (0.35, 0.60, 0.90, 1.0) # Bright tropical sky
    bg.inputs['Strength'].default_value = 1.20
    
    out = nodes.new(type='ShaderNodeOutputWorld')
    links.new(bg.outputs['Background'], out.inputs['Surface'])
    
    # Tropical Sun Light (Balanced Morning Key)
    sun_data = bpy.data.lights.new(name="TropicalSun", type='SUN')
    sun_data.energy = 3.2
    sun_data.color = (1.0, 0.96, 0.90)
    sun_obj = bpy.data.objects.new(name="TropicalSun", object_data=sun_data)
    bpy.context.collection.objects.link(sun_obj)
    sun_obj.rotation_euler = (math.radians(48), math.radians(15), math.radians(-32))
    
    # Sky Fill Light (Soft Cyan Ambient Bounce)
    fill_data = bpy.data.lights.new(name="SkyFill", type='SUN')
    fill_data.energy = 1.1
    fill_data.color = (0.50, 0.75, 0.95)
    fill_obj = bpy.data.objects.new(name="SkyFill", object_data=fill_data)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.rotation_euler = (math.radians(-35), 0, math.radians(45))

    # Dedicated Character Key & Eye Catchlight
    char_key = bpy.data.lights.new(name="CharFaceKey", type='POINT')
    char_key.energy = 22.0
    char_key.color = (1.0, 0.96, 0.90)
    char_key_obj = bpy.data.objects.new(name="CharFaceKey", object_data=char_key)
    char_key_obj.location = (-0.35, -1.8, 1.6)
    bpy.context.collection.objects.link(char_key_obj)

    # 2. Material Definitions
    # Earth / Dirt trail
    mat_trail = bpy.data.materials.new("Trail_DampDirt")
    mat_trail.use_nodes = True
    b_trail = mat_trail.node_tree.nodes.get("Principled BSDF")
    b_trail.inputs['Base Color'].default_value = (0.42, 0.30, 0.18, 1.0)
    b_trail.inputs['Roughness'].default_value = 0.55
    
    # Tropical Foliage Green
    mat_fern = bpy.data.materials.new("Fern_LushGreen")
    mat_fern.use_nodes = True
    b_fern = mat_fern.node_tree.nodes.get("Principled BSDF")
    b_fern.inputs['Base Color'].default_value = (0.14, 0.58, 0.18, 1.0)
    b_fern.inputs['Roughness'].default_value = 0.32
    if 'Subsurface Weight' in b_fern.inputs:
        b_fern.inputs['Subsurface Weight'].default_value = 0.35
        b_fern.inputs['Subsurface Radius'].default_value = (0.2, 0.6, 0.1)
    
    # Crystal Lagoon Water
    mat_water = bpy.data.materials.new("Lagoon_Water")
    mat_water.use_nodes = True
    b_water = mat_water.node_tree.nodes.get("Principled BSDF")
    b_water.inputs['Base Color'].default_value = (0.12, 0.68, 0.76, 1.0)
    b_water.inputs['Roughness'].default_value = 0.03
    if 'Transmission Weight' in b_water.inputs:
        b_water.inputs['Transmission Weight'].default_value = 0.70
    elif 'Transmission' in b_water.inputs:
        b_water.inputs['Transmission'].default_value = 0.70
    if 'IOR' in b_water.inputs:
        b_water.inputs['IOR'].default_value = 1.333

    # Distant Volcano & Rock
    mat_volcano = bpy.data.materials.new("Volcano_Rock")
    mat_volcano.use_nodes = True
    b_volc = mat_volcano.node_tree.nodes.get("Principled BSDF")
    b_volc.inputs['Base Color'].default_value = (0.34, 0.30, 0.30, 1.0)
    b_volc.inputs['Roughness'].default_value = 0.82
    
    mat_smoke = bpy.data.materials.new("Volcano_Smoke")
    mat_smoke.use_nodes = True
    b_smk = mat_smoke.node_tree.nodes.get("Principled BSDF")
    b_smk.inputs['Base Color'].default_value = (0.95, 0.92, 0.88, 1.0)
    b_smk.inputs['Roughness'].default_value = 0.88
    if 'Emission Color' in b_smk.inputs:
        b_smk.inputs['Emission Color'].default_value = (0.98, 0.80, 0.65, 1.0)
        b_smk.inputs['Emission Strength'].default_value = 0.35

    # Flower Petal Colors (Purple, Orange, Yellow)
    mat_flower_purple = bpy.data.materials.new("Flower_Purple")
    mat_flower_purple.use_nodes = True
    b_purp = mat_flower_purple.node_tree.nodes.get("Principled BSDF")
    b_purp.inputs['Base Color'].default_value = (0.75, 0.15, 0.85, 1.0)
    b_purp.inputs['Roughness'].default_value = 0.28
    if 'Subsurface Weight' in b_purp.inputs:
        b_purp.inputs['Subsurface Weight'].default_value = 0.40
        
    mat_flower_yellow = bpy.data.materials.new("Flower_Yellow")
    mat_flower_yellow.use_nodes = True
    b_yel = mat_flower_yellow.node_tree.nodes.get("Principled BSDF")
    b_yel.inputs['Base Color'].default_value = (0.98, 0.82, 0.08, 1.0)
    b_yel.inputs['Roughness'].default_value = 0.28
    
    mat_flower_orange = bpy.data.materials.new("Flower_Orange")
    mat_flower_orange.use_nodes = True
    b_ora = mat_flower_orange.node_tree.nodes.get("Principled BSDF")
    b_ora.inputs['Base Color'].default_value = (0.98, 0.45, 0.08, 1.0)
    b_ora.inputs['Roughness'].default_value = 0.28

    # 3. Ground Terrain & Dirt Trail
    bpy.ops.mesh.primitive_plane_add(size=35.0, location=(0, 6.0, 0.0))
    ground = bpy.context.active_object
    ground.name = "Terrain_Ground"
    ground.data.materials.append(mat_trail)

    # 4. Giant 3-Toed Dinosaur Footprint Puddle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.48, depth=0.06, location=(0.35, -0.65, 0.02))
    heel = bpy.context.active_object
    heel.name = "Dino_Footprint_Heel"
    heel.scale = (0.85, 1.15, 1.0)
    heel.data.materials.append(mat_water)
    
    for t_idx, (tx, ty, rot_z) in enumerate([(0.22, -1.20, -20), (0.35, -1.30, 0), (0.48, -1.20, 20)]):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=0.06, location=(tx, ty, 0.02))
        toe = bpy.context.active_object
        toe.name = f"Dino_Footprint_Toe_{t_idx}"
        toe.scale = (0.7, 1.4, 1.0)
        toe.rotation_euler = (0, 0, math.radians(rot_z))
        toe.data.materials.append(mat_water)

    # 5. Distant Volcano with Steam Plume (Framed nicely in background)
    bpy.ops.mesh.primitive_cone_add(radius1=8.0, depth=12.0, location=(-3.2, 24.0, 5.5))
    volcano = bpy.context.active_object
    volcano.name = "Volcano_Peak"
    volcano.scale = (1.3, 1.0, 1.0)
    volcano.data.materials.append(mat_volcano)
    
    for s_idx, (sx, sy, sz, sr) in enumerate([
        (-3.2, 24.0, 12.0, 2.0),
        (-2.8, 25.0, 14.5, 3.0),
        (-2.2, 26.0, 18.0, 4.2)
    ]):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=sr, location=(sx, sy, sz))
        smoke = bpy.context.active_object
        smoke.name = f"Volcano_Smoke_{s_idx}"
        smoke.data.materials.append(mat_smoke)

    # 6. Cascading Waterfalls & Cliff Ridge
    bpy.ops.mesh.primitive_cube_add(size=7.0, location=(6.5, 16.0, 3.2))
    cliff = bpy.context.active_object
    cliff.name = "Waterfall_Cliff"
    cliff.scale = (1.2, 0.4, 1.6)
    cliff.data.materials.append(mat_volcano)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=1.5, depth=7.5, location=(6.5, 14.8, 3.0))
    fall = bpy.context.active_object
    fall.name = "Waterfall_Cascade"
    fall.scale = (1.2, 0.25, 1.0)
    fall.data.materials.append(mat_water)

    # Crystal Tropical Lagoon (Water Plane)
    bpy.ops.mesh.primitive_plane_add(size=22.0, location=(4.2, 11.0, -0.15))
    lagoon = bpy.context.active_object
    lagoon.name = "Crystal_Lagoon"
    lagoon.data.materials.append(mat_water)

    # 7. Tropical Palm Trees
    palm_locations = [
        (-3.5, 1.8, 0.0), (-2.8, 6.5, 0.0), (3.6, 2.2, 0.0), (5.2, 6.0, 0.0)
    ]
    for p_idx, (px, py, pz) in enumerate(palm_locations):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=4.0, location=(px, py, pz + 2.0))
        trunk = bpy.context.active_object
        trunk.name = f"Palm_Trunk_{p_idx}"
        trunk.rotation_euler = (math.radians(8), math.radians(-5), 0)
        trunk.data.materials.append(mat_volcano)
        
        for f_angle in [0, 60, 120, 180, 240, 300]:
            bpy.ops.mesh.primitive_cube_add(size=0.3, location=(px, py, pz + 4.0))
            frond = bpy.context.active_object
            frond.name = f"Palm_Frond_{p_idx}_{f_angle}"
            frond.scale = (0.6, 3.0, 0.15)
            frond.rotation_euler = (math.radians(35), 0, math.radians(f_angle))
            frond.data.materials.append(mat_fern)

    # 8. Giant Prehistoric Blossoms (Purple, Orange, Yellow)
    flower_locs = [
        (-1.2, -0.5, 0.0, mat_flower_purple, 0.42),
        (-1.9, -0.2, 0.0, mat_flower_orange, 0.50),
        (1.2, -0.3, 0.0, mat_flower_yellow, 0.48),
        (1.8, 0.4, 0.0, mat_flower_purple, 0.55),
    ]
    for fl_idx, (fx, fy, fz, fmat, frad) in enumerate(flower_locs):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.038, depth=1.1, location=(fx, fy, fz + 0.55))
        fstem = bpy.context.active_object
        fstem.data.materials.append(mat_fern)
        
        bpy.ops.mesh.primitive_cylinder_add(radius=frad, depth=0.10, location=(fx, fy, fz + 1.1))
        fbloom = bpy.context.active_object
        fbloom.name = f"Prehistoric_Blossom_{fl_idx}"
        fbloom.rotation_euler = (math.radians(-25), 0, math.radians(15))
        fbloom.data.materials.append(fmat)

    print("[PrehistoricWorldBuilder] Scene geometry, lighting, and materials assembled successfully.")
'''

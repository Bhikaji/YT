# Master 3D Production Render Script (Blender 4.5+ EEVEE-Next)
import bpy
import math
import os

# 1. Clear Scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# 2. Render Settings (EEVEE-Next, High Definition 1080x1920 @ 30fps)
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderEngine") else 'BLENDER_EEVEE'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 300

if hasattr(scene, "eevee"):
    scene.eevee.taa_render_samples = 4

# AgX Color Management
if 'AgX' in [c.name for c in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items]:
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'Medium High Contrast'
else:
    scene.view_settings.view_transform = 'Filmic'

scene.render.filepath = os.path.join(r"D:\YT\output\renders\demo_pixar_dino_short", "frame_")
scene.render.image_settings.file_format = 'JPEG'
scene.render.image_settings.quality = 95

# 3. Materials Palette

def make_principled_mat(name, base_color, roughness=0.35, sss=0.0, sss_color=None, emission=None, metallic=0.0, specular=0.5):
    import bpy
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
        if 'Specular IOR Level' in bsdf.inputs:
            bsdf.inputs['Specular IOR Level'].default_value = specular
        elif 'Specular' in bsdf.inputs:
            bsdf.inputs['Specular'].default_value = specular
            
        if 'Subsurface Weight' in bsdf.inputs and sss > 0.0:
            bsdf.inputs['Subsurface Weight'].default_value = sss
            bsdf.inputs['Subsurface Radius'].default_value = (0.35, 0.16, 0.08)
            if sss_color and 'Subsurface Color' in bsdf.inputs:
                bsdf.inputs['Subsurface Color'].default_value = sss_color
        elif 'Subsurface' in bsdf.inputs and sss > 0.0:
            bsdf.inputs['Subsurface'].default_value = sss
            bsdf.inputs['Subsurface Radius'].default_value = (0.35, 0.16, 0.08)
            
        if emission:
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = emission[0]
                bsdf.inputs['Emission Strength'].default_value = emission[1]
            elif 'Emission' in bsdf.inputs:
                bsdf.inputs['Emission'].default_value = emission[0]
    return mat

# Character Material Palette matching Demo Video
mat_leo_skin = make_principled_mat("Leo_Skin", (0.94, 0.74, 0.62, 1.0), roughness=0.32, sss=0.30, sss_color=(0.98, 0.58, 0.48, 1.0))
mat_leo_lips = make_principled_mat("Leo_Lips", (0.88, 0.52, 0.50, 1.0), roughness=0.35, sss=0.25)
mat_leo_hair = make_principled_mat("Leo_Hair", (0.24, 0.13, 0.06, 1.0), roughness=0.38, specular=0.88)
mat_leo_shirt = make_principled_mat("Leo_OrangeShirt", (0.96, 0.44, 0.08, 1.0), roughness=0.70)
mat_leo_shorts = make_principled_mat("Leo_DenimShorts", (0.16, 0.32, 0.62, 1.0), roughness=0.75)
mat_leo_sneakers = make_principled_mat("Leo_RedSneakers", (0.85, 0.14, 0.14, 1.0), roughness=0.50)
mat_rubber_white = make_principled_mat("SneakerRubberWhite", (0.95, 0.95, 0.95, 1.0), roughness=0.20)
mat_backpack_blue = make_principled_mat("Leo_BackpackBlue", (0.12, 0.38, 0.72, 1.0), roughness=0.60)
mat_backpack_yellow = make_principled_mat("Leo_BackpackYellow", (0.96, 0.76, 0.12, 1.0), roughness=0.55)
mat_eye_white = make_principled_mat("EyeWhite", (0.98, 0.98, 0.99, 1.0), roughness=0.04, specular=0.98)
mat_eye_iris = make_principled_mat("EyeIrisHazel", (0.18, 0.50, 0.45, 1.0), roughness=0.06, specular=0.95)
mat_eye_pupil = make_principled_mat("EyePupil", (0.01, 0.01, 0.01, 1.0), roughness=0.02, specular=0.99)
mat_mouth_interior = make_principled_mat("MouthInterior", (0.42, 0.08, 0.10, 1.0), roughness=0.40)
mat_teeth = make_principled_mat("TeethWhite", (0.96, 0.95, 0.93, 1.0), roughness=0.12)

# Puppy Materials
mat_puppy_fur = make_principled_mat("Puppy_Fur", (0.89, 0.68, 0.38, 1.0), roughness=0.62, sss=0.18, specular=0.65)
mat_puppy_nose = make_principled_mat("Puppy_Nose", (0.07, 0.05, 0.05, 1.0), roughness=0.20, specular=0.92)
mat_puppy_collar = make_principled_mat("Puppy_Collar", (0.88, 0.12, 0.14, 1.0), roughness=0.35)
mat_gold_tag = make_principled_mat("GoldTag", (0.95, 0.75, 0.15, 1.0), roughness=0.18, metallic=0.92)

# Dinosaur Materials
mat_stego_skin = make_principled_mat("Stego_Skin", (0.46, 0.40, 0.32, 1.0), roughness=0.68)
mat_stego_plates = make_principled_mat("Stego_Plates", (0.82, 0.30, 0.15, 1.0), roughness=0.50, sss=0.22)
mat_sauropod = make_principled_mat("Sauropod_Skin", (0.26, 0.56, 0.60, 1.0), roughness=0.55, sss=0.18)
mat_baby_trex = make_principled_mat("BabyTrex_Skin", (0.36, 0.60, 0.30, 1.0), roughness=0.60, sss=0.20)


# 4. Environment & Prehistoric World

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
    bg.inputs['Color'].default_value = (0.38, 0.62, 0.92, 1.0) # Bright tropical sky
    bg.inputs['Strength'].default_value = 1.35
    
    out = nodes.new(type='ShaderNodeOutputWorld')
    links.new(bg.outputs['Background'], out.inputs['Surface'])
    
    # Tropical Sun Light (Warm Morning Key at 45 degree angle)
    sun_data = bpy.data.lights.new(name="TropicalSun", type='SUN')
    sun_data.energy = 6.5
    sun_data.color = (1.0, 0.95, 0.86)
    sun_obj = bpy.data.objects.new(name="TropicalSun", object_data=sun_data)
    bpy.context.collection.objects.link(sun_obj)
    sun_obj.rotation_euler = (math.radians(48), math.radians(15), math.radians(-32))
    
    # Sky Fill Light (Soft Cyan Ambient Bounce)
    fill_data = bpy.data.lights.new(name="SkyFill", type='SUN')
    fill_data.energy = 2.2
    fill_data.color = (0.55, 0.78, 0.98)
    fill_obj = bpy.data.objects.new(name="SkyFill", object_data=fill_data)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.rotation_euler = (math.radians(-35), 0, math.radians(45))

    # Dedicated Character Key & Eye Catchlight
    char_key = bpy.data.lights.new(name="CharFaceKey", type='POINT')
    char_key.energy = 85.0
    char_key.color = (1.0, 0.96, 0.90)
    char_key_obj = bpy.data.objects.new(name="CharFaceKey", object_data=char_key)
    char_key_obj.location = (-0.2, -2.2, 1.8)
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
    b_water.inputs['Base Color'].default_value = (0.18, 0.72, 0.80, 1.0)
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
    b_purp.inputs['Base Color'].default_value = (0.70, 0.20, 0.85, 1.0)
    b_purp.inputs['Roughness'].default_value = 0.30
    if 'Subsurface Weight' in b_purp.inputs:
        b_purp.inputs['Subsurface Weight'].default_value = 0.40
        
    mat_flower_yellow = bpy.data.materials.new("Flower_Yellow")
    mat_flower_yellow.use_nodes = True
    b_yel = mat_flower_yellow.node_tree.nodes.get("Principled BSDF")
    b_yel.inputs['Base Color'].default_value = (0.98, 0.80, 0.14, 1.0)
    b_yel.inputs['Roughness'].default_value = 0.30
    
    mat_flower_orange = bpy.data.materials.new("Flower_Orange")
    mat_flower_orange.use_nodes = True
    b_ora = mat_flower_orange.node_tree.nodes.get("Principled BSDF")
    b_ora.inputs['Base Color'].default_value = (0.96, 0.45, 0.12, 1.0)
    b_ora.inputs['Roughness'].default_value = 0.30

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

    # 5. Distant Volcano with Steam Plume
    bpy.ops.mesh.primitive_cone_add(radius1=9.5, depth=15.0, location=(-5.0, 32.0, 6.5))
    volcano = bpy.context.active_object
    volcano.name = "Volcano_Peak"
    volcano.scale = (1.4, 1.0, 1.0)
    volcano.data.materials.append(mat_volcano)
    
    for s_idx, (sx, sy, sz, sr) in enumerate([
        (-5.0, 32.0, 14.5, 2.4),
        (-4.5, 33.0, 17.5, 3.6),
        (-3.8, 34.0, 21.5, 5.2)
    ]):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=sr, location=(sx, sy, sz))
        smoke = bpy.context.active_object
        smoke.name = f"Volcano_Smoke_{s_idx}"
        smoke.data.materials.append(mat_smoke)

    # 6. Cascading Waterfalls & Cliff Ridge
    bpy.ops.mesh.primitive_cube_add(size=8.0, location=(10.0, 20.0, 4.0))
    cliff = bpy.context.active_object
    cliff.name = "Waterfall_Cliff"
    cliff.scale = (1.2, 0.4, 1.8)
    cliff.data.materials.append(mat_volcano)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=1.8, depth=9.0, location=(10.0, 18.5, 3.8))
    fall = bpy.context.active_object
    fall.name = "Waterfall_Cascade"
    fall.scale = (1.2, 0.25, 1.0)
    fall.data.materials.append(mat_water)

    # Crystal Tropical Lagoon (Water Plane)
    bpy.ops.mesh.primitive_plane_add(size=24.0, location=(5.0, 13.0, -0.15))
    lagoon = bpy.context.active_object
    lagoon.name = "Crystal_Lagoon"
    lagoon.data.materials.append(mat_water)

    # 7. Tropical Palm Trees
    palm_locations = [
        (-4.0, 2.0, 0.0), (-3.2, 7.5, 0.0), (4.2, 2.5, 0.0), (6.2, 7.0, 0.0)
    ]
    for p_idx, (px, py, pz) in enumerate(palm_locations):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=4.2, location=(px, py, pz + 2.1))
        trunk = bpy.context.active_object
        trunk.name = f"Palm_Trunk_{p_idx}"
        trunk.rotation_euler = (math.radians(8), math.radians(-5), 0)
        trunk.data.materials.append(mat_volcano)
        
        for f_angle in [0, 60, 120, 180, 240, 300]:
            bpy.ops.mesh.primitive_cube_add(size=0.3, location=(px, py, pz + 4.2))
            frond = bpy.context.active_object
            frond.name = f"Palm_Frond_{p_idx}_{f_angle}"
            frond.scale = (0.6, 3.2, 0.15)
            frond.rotation_euler = (math.radians(35), 0, math.radians(f_angle))
            frond.data.materials.append(mat_fern)

    # 8. Giant Prehistoric Blossoms (Purple, Orange, Yellow)
    flower_locs = [
        (-1.4, -0.6, 0.0, mat_flower_purple, 0.45),
        (-2.2, -0.2, 0.0, mat_flower_orange, 0.55),
        (1.4, -0.4, 0.0, mat_flower_yellow, 0.50),
        (2.1, 0.4, 0.0, mat_flower_purple, 0.60),
    ]
    for fl_idx, (fx, fy, fz, fmat, frad) in enumerate(flower_locs):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=1.2, location=(fx, fy, fz + 0.6))
        fstem = bpy.context.active_object
        fstem.data.materials.append(mat_fern)
        
        bpy.ops.mesh.primitive_cylinder_add(radius=frad, depth=0.12, location=(fx, fy, fz + 1.2))
        fbloom = bpy.context.active_object
        fbloom.name = f"Prehistoric_Blossom_{fl_idx}"
        fbloom.rotation_euler = (math.radians(-25), 0, math.radians(15))
        fbloom.data.materials.append(fmat)

    print("[PrehistoricWorldBuilder] Scene geometry, lighting, and materials assembled successfully.")

build_prehistoric_world()

# 5. Characters & Creatures

def build_pixar_leo():
    import bpy, math
    leo_objects = []
    
    # 1. Smooth Head
    bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=32, radius=0.38, location=(-0.35, 0.0, 0.0 + 1.48))
    head = bpy.context.active_object
    head.name = "Leo_Head"
    head.scale = (1.04, 0.96, 1.12)
    bpy.ops.object.transform_apply(scale=True)
    head.data.materials.append(mat_leo_skin)
    leo_objects.append(head)
    
    # Cute Button Nose
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=16, radius=0.065, location=(-0.35, 0.0 - 0.37, 0.0 + 1.45))
    nose = bpy.context.active_object
    nose.name = "Leo_Nose"
    nose.scale = (1.1, 0.9, 0.85)
    nose.data.materials.append(mat_leo_skin)
    leo_objects.append(nose)
    
    # Smiling Mouth & Lips
    bpy.ops.mesh.primitive_torus_add(major_radius=0.09, minor_radius=0.022, location=(-0.35, 0.0 - 0.34, 0.0 + 1.34))
    mouth = bpy.context.active_object
    mouth.name = "Leo_MouthLips"
    mouth.rotation_euler = (math.radians(75), 0, 0)
    mouth.scale = (1.4, 0.6, 1.0)
    mouth.data.materials.append(mat_leo_lips)
    leo_objects.append(mouth)
    
    # Upper Teeth
    bpy.ops.mesh.primitive_cube_add(size=0.05, location=(-0.35, 0.0 - 0.33, 0.0 + 1.35))
    teeth = bpy.context.active_object
    teeth.name = "Leo_Teeth"
    teeth.scale = (1.6, 0.3, 0.4)
    teeth.data.materials.append(mat_teeth)
    leo_objects.append(teeth)

    # Add ShapeKeys for Speech Visemes and Emotions to Head and Mouth
    head.shape_key_add(name="Basis")
    sk_jaw = head.shape_key_add(name="jawOpen")
    sk_smile = head.shape_key_add(name="mouthSmile")
    sk_pucker = head.shape_key_add(name="mouthPucker")
    sk_wonder = head.shape_key_add(name="wonderEmotion")
    
    for i, v in enumerate(head.data.vertices):
        if v.co.z < (0.0 + 1.36) and v.co.y < (0.0 - 0.05):
            sk_jaw.data[i].co.z -= 0.12
            sk_jaw.data[i].co.y += 0.03
        if v.co.z > (0.0 + 1.28) and v.co.z < (0.0 + 1.38) and abs(v.co.x - -0.35) > 0.08 and v.co.y < (0.0 - 0.15):
            sk_smile.data[i].co.z += 0.05
        if v.co.z > (0.0 + 1.45) and v.co.y < (0.0 - 0.20):
            sk_wonder.data[i].co.z += 0.03
            
    # Eyes (Left & Right) with Eyelids & Specular Cornea
    for side, sign in [("L", 1), ("R", -1)]:
        eye_center = (-0.35 + 0.13 * sign, 0.0 - 0.28, 0.0 + 1.52)
        # Sclera (White)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=28, ring_count=20, radius=0.105, location=eye_center)
        sclera = bpy.context.active_object
        sclera.name = f"Leo_EyeWhite_{side}"
        sclera.scale = (1.0, 0.75, 1.1)
        sclera.data.materials.append(mat_eye_white)
        leo_objects.append(sclera)
        
        # Iris (Hazel)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=0.068, location=(-0.35 + 0.13 * sign, 0.0 - 0.35, 0.0 + 1.52))
        iris = bpy.context.active_object
        iris.name = f"Leo_Iris_{side}"
        iris.scale = (1.0, 0.25, 1.0)
        iris.data.materials.append(mat_eye_iris)
        leo_objects.append(iris)
        
        # Pupil (Glossy Black)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14, radius=0.034, location=(-0.35 + 0.13 * sign, 0.0 - 0.365, 0.0 + 1.52))
        pupil = bpy.context.active_object
        pupil.name = f"Leo_Pupil_{side}"
        pupil.scale = (1.0, 0.15, 1.0)
        pupil.data.materials.append(mat_eye_pupil)
        leo_objects.append(pupil)
        
        # Specular Cornea Highlight
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.012, location=(-0.35 + 0.115 * sign, 0.0 - 0.38, 0.0 + 1.535))
        glint = bpy.context.active_object
        glint.data.materials.append(mat_rubber_white)
        leo_objects.append(glint)

        # Upper Eyelid
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14, radius=0.112, location=eye_center)
        lid = bpy.context.active_object
        lid.name = f"Leo_UpperLid_{side}"
        lid.scale = (1.02, 0.78, 0.55)
        lid.location.z += 0.05
        lid.data.materials.append(mat_leo_skin)
        leo_objects.append(lid)
        
        # Eyebrows (Curved Expressive)
        bpy.ops.mesh.primitive_cube_add(size=0.08, location=(-0.35 + 0.13 * sign, 0.0 - 0.32, 0.0 + 1.66))
        brow = bpy.context.active_object
        brow.name = f"Leo_Brow_{side}"
        brow.scale = (1.6, 0.25, 0.22)
        brow.rotation_euler = (0, 0.14 * sign, 0)
        brow.data.materials.append(mat_leo_hair)
        leo_objects.append(brow)

    # 2. Wavy Tousled Hair Mesh (Layered Sculpted Clusters)
    hair_clusters = [
        (-0.35 + 0.0, 0.0 - 0.08, 0.0 + 1.90, 0.38, 1.02, 0.88, 0.96),
        (-0.35 + 0.18, 0.0 - 0.04, 0.0 + 1.84, 0.26, 0.92, 0.82, 0.85),
        (-0.35 - 0.18, 0.0 - 0.04, 0.0 + 1.84, 0.26, 0.92, 0.82, 0.85),
        (-0.35 + 0.10, 0.0 - 0.26, 0.0 + 1.80, 0.18, 1.25, 0.65, 0.55),
        (-0.35 - 0.10, 0.0 - 0.26, 0.0 + 1.80, 0.18, 1.25, 0.65, 0.55),
        (-0.35 + 0.0, 0.0 - 0.30, 0.0 + 1.82, 0.16, 1.15, 0.55, 0.65),
        (-0.35 + 0.32, 0.0 + 0.02, 0.0 + 1.54, 0.20, 0.75, 0.92, 1.05),
        (-0.35 - 0.32, 0.0 + 0.02, 0.0 + 1.54, 0.20, 0.75, 0.92, 1.05),
        (-0.35 + 0.22, 0.0 + 0.22, 0.0 + 1.62, 0.24, 0.92, 0.92, 0.98),
        (-0.35 - 0.22, 0.0 + 0.22, 0.0 + 1.62, 0.24, 0.92, 0.92, 0.98),
        (-0.35 + 0.0, 0.0 + 0.26, 0.0 + 1.60, 0.26, 1.02, 0.92, 0.98),
    ]
    for idx, (hx, hy, hz, hr, sx, sy, sz) in enumerate(hair_clusters):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=18, radius=hr, location=(hx, hy, hz))
        h_obj = bpy.context.active_object
        h_obj.name = f"Leo_HairCluster_{idx}"
        h_obj.scale = (sx, sy, sz)
        bpy.ops.object.transform_apply(scale=True)
        h_obj.data.materials.append(mat_leo_hair)
        leo_objects.append(h_obj)

    # 3. Orange Crewneck T-Shirt (Torso)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=0.42, location=(-0.35, 0.0 + 0.02, 0.0 + 0.85))
    torso = bpy.context.active_object
    torso.name = "Leo_Torso"
    torso.scale = (0.88, 0.70, 1.10)
    bpy.ops.object.transform_apply(scale=True)
    torso.data.materials.append(mat_leo_shirt)
    leo_objects.append(torso)
    
    # Neck Ribbing
    bpy.ops.mesh.primitive_torus_add(major_radius=0.18, minor_radius=0.035, location=(-0.35, 0.0 - 0.02, 0.0 + 1.18))
    rib = bpy.context.active_object
    rib.name = "Leo_ShirtNeck"
    rib.data.materials.append(mat_leo_shirt)
    leo_objects.append(rib)

    # Short Sleeves & Animated Pointing Gesture
    for side, sign in [("L", 1), ("R", -1)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.18, location=(-0.35 + 0.38 * sign, 0.0, 0.0 + 0.95))
        sleeve = bpy.context.active_object
        sleeve.name = f"Leo_Sleeve_{side}"
        sleeve.rotation_euler = (0, 0.35 * sign, 0)
        sleeve.data.materials.append(mat_leo_shirt)
        leo_objects.append(sleeve)
        
        # Arm
        bpy.ops.mesh.primitive_cylinder_add(radius=0.075, depth=0.38, location=(-0.35 + 0.46 * sign, 0.0 - 0.05, 0.0 + 0.72))
        arm = bpy.context.active_object
        arm.name = f"Leo_Arm_{side}"
        arm.rotation_euler = (math.radians(25 if sign == -1 else 10), math.radians(22 * sign), 0)
        arm.data.materials.append(mat_leo_skin)
        leo_objects.append(arm)
        
        # Hand (Right hand pointing excitedly toward dinosaur)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=18, ring_count=14, radius=0.078, location=(-0.35 + 0.52 * sign, 0.0 - (0.24 if sign == -1 else 0.12), 0.0 + 0.54))
        hand = bpy.context.active_object
        hand.name = f"Leo_Hand_{side}"
        hand.scale = (0.9, 1.25, 0.7)
        hand.data.materials.append(mat_leo_skin)
        leo_objects.append(hand)

    # 4. Blue Denim Shorts with Folded Cuffs
    bpy.ops.mesh.primitive_cylinder_add(radius=0.31, depth=0.34, location=(-0.35, 0.0 + 0.02, 0.0 + 0.42))
    shorts = bpy.context.active_object
    shorts.name = "Leo_Shorts"
    shorts.scale = (1.05, 0.88, 1.0)
    shorts.data.materials.append(mat_leo_shorts)
    leo_objects.append(shorts)

    # Legs & Red Canvas Sneakers with White Rubber Toe Cap
    for side, sign in [("L", 1), ("R", -1)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.085, depth=0.36, location=(-0.35 + 0.16 * sign, 0.0, 0.0 + 0.22))
        leg = bpy.context.active_object
        leg.name = f"Leo_Leg_{side}"
        leg.data.materials.append(mat_leo_skin)
        leo_objects.append(leg)
        
        # Red Sneaker Body
        bpy.ops.mesh.primitive_cube_add(size=0.16, location=(-0.35 + 0.16 * sign, 0.0 - 0.06, 0.0 + 0.08))
        shoe = bpy.context.active_object
        shoe.name = f"Leo_Sneaker_{side}"
        shoe.scale = (0.95, 1.65, 0.72)
        bpy.ops.object.transform_apply(scale=True)
        shoe.data.materials.append(mat_leo_sneakers)
        leo_objects.append(shoe)
        
        # White Rubber Toe Cap
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.072, location=(-0.35 + 0.16 * sign, 0.0 - 0.17, 0.0 + 0.06))
        toecap = bpy.context.active_object
        toecap.name = f"Leo_Toecap_{side}"
        toecap.scale = (1.05, 0.65, 0.85)
        toecap.data.materials.append(mat_rubber_white)
        leo_objects.append(toecap)

    # 5. Blue Adventure Backpack with Yellow Straps
    bpy.ops.mesh.primitive_cube_add(size=0.36, location=(-0.35, 0.0 + 0.28, 0.0 + 0.90))
    pack = bpy.context.active_object
    pack.name = "Leo_Backpack"
    pack.scale = (0.95, 0.65, 1.15)
    bpy.ops.object.transform_apply(scale=True)
    pack.data.materials.append(mat_backpack_blue)
    leo_objects.append(pack)
    
    for sign in [1, -1]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.28, minor_radius=0.024, location=(-0.35 + 0.17 * sign, 0.0 + 0.10, 0.0 + 0.90))
        strap = bpy.context.active_object
        strap.name = f"Leo_Strap_{sign}"
        strap.rotation_euler = (math.radians(90), 0, math.radians(18 * sign))
        strap.data.materials.append(mat_backpack_yellow)
        leo_objects.append(strap)

    return head, mouth, leo_objects

head_leo, mouth_leo, leo_objs = build_pixar_leo()


def build_puppy_lumi():
    import bpy, math
    puppy_objects = []
    
    # 1. Puppy Head
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=0.20, location=(0.42, -0.25, 0.0 + 0.40))
    phead = bpy.context.active_object
    phead.name = "Puppy_Head"
    phead.scale = (1.05, 1.12, 0.98)
    phead.data.materials.append(mat_puppy_fur)
    puppy_objects.append(phead)
    
    # Puppy Snout & Black Nose
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14, radius=0.10, location=(0.42, -0.25 - 0.16, 0.0 + 0.34))
    snout = bpy.context.active_object
    snout.name = "Puppy_Snout"
    snout.scale = (0.85, 1.25, 0.75)
    snout.data.materials.append(mat_puppy_fur)
    puppy_objects.append(snout)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.038, location=(0.42, -0.25 - 0.27, 0.0 + 0.36))
    nose = bpy.context.active_object
    nose.name = "Puppy_Nose"
    nose.data.materials.append(mat_puppy_nose)
    puppy_objects.append(nose)
    
    # Big Expressive Puppy Eyes with Highlights
    for side, sign in [("L", 1), ("R", -1)]:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14, radius=0.046, location=(0.42 + 0.08 * sign, -0.25 - 0.14, 0.0 + 0.44))
        peye = bpy.context.active_object
        peye.name = f"Puppy_Eye_{side}"
        peye.data.materials.append(mat_eye_pupil)
        puppy_objects.append(peye)
        
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.012, location=(0.42 + 0.072 * sign, -0.25 - 0.18, 0.0 + 0.455))
        glint = bpy.context.active_object
        glint.data.materials.append(mat_rubber_white)
        puppy_objects.append(glint)

    # Floppy Golden Ears
    for side, sign in [("L", 1), ("R", -1)]:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14, radius=0.14, location=(0.42 + 0.18 * sign, -0.25 - 0.02, 0.0 + 0.36))
        ear = bpy.context.active_object
        ear.name = f"Puppy_Ear_{side}"
        ear.scale = (0.42, 0.85, 1.35)
        ear.rotation_euler = (math.radians(18), math.radians(24 * sign), math.radians(-10 * sign))
        ear.data.materials.append(mat_puppy_fur)
        puppy_objects.append(ear)

    # Red Collar with Gold Tag
    bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.024, location=(0.42, -0.25 + 0.04, 0.0 + 0.30))
    collar = bpy.context.active_object
    collar.name = "Puppy_Collar"
    collar.data.materials.append(mat_puppy_collar)
    puppy_objects.append(collar)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.01, location=(0.42, -0.25 - 0.08, 0.0 + 0.26))
    tag = bpy.context.active_object
    tag.name = "Puppy_Tag"
    tag.data.materials.append(mat_gold_tag)
    puppy_objects.append(tag)

    # Torso & 4 Paws
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=18, radius=0.22, location=(0.42, -0.25 + 0.18, 0.0 + 0.25))
    p_body = bpy.context.active_object
    p_body.name = "Puppy_Body"
    p_body.scale = (0.85, 1.45, 0.90)
    p_body.data.materials.append(mat_puppy_fur)
    puppy_objects.append(p_body)
    
    for fx, fy in [(0.10, 0.05), (-0.10, 0.05), (0.10, 0.32), (-0.10, 0.32)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.052, depth=0.18, location=(0.42 + fx, -0.25 + fy, 0.0 + 0.09))
        paw = bpy.context.active_object
        paw.name = "Puppy_Paw"
        paw.data.materials.append(mat_puppy_fur)
        puppy_objects.append(paw)

    # Wagging Tail
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.22, location=(0.42, -0.25 + 0.44, 0.0 + 0.30))
    tail = bpy.context.active_object
    tail.name = "Puppy_Tail"
    tail.rotation_euler = (math.radians(-45), 0, 0)
    tail.data.materials.append(mat_puppy_fur)
    puppy_objects.append(tail)

    return phead, tail, puppy_objects

phead, ptail, puppy_objs = build_puppy_lumi()


def build_stegosaurus(location=(-2.6, 4.2, 0.0)):
    import bpy, math
    sx, sy, sz = location
    stego_objs = []
    
    # 1. Massive Arched Body
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=1.35, location=(sx, sy, sz + 1.35))
    body = bpy.context.active_object
    body.name = "Stego_Body"
    body.scale = (0.92, 2.15, 1.12)
    body.data.materials.append(mat_stego_skin)
    stego_objs.append(body)
    
    # Neck & Head
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=18, radius=0.45, location=(sx, sy - 2.6, sz + 0.75))
    neck = bpy.context.active_object
    neck.name = "Stego_Neck"
    neck.scale = (0.7, 1.4, 0.7)
    neck.data.materials.append(mat_stego_skin)
    stego_objs.append(neck)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14, radius=0.32, location=(sx, sy - 3.6, sz + 0.60))
    shead = bpy.context.active_object
    shead.name = "Stego_Head"
    shead.scale = (0.65, 1.3, 0.75)
    shead.data.materials.append(mat_stego_skin)
    stego_objs.append(shead)

    # Double Row of Terracotta Dorsal Plates
    plate_positions = [
        (-1.8, 0.35), (-1.2, 0.55), (-0.6, 0.80), (0.0, 0.95),
        (0.6, 0.90), (1.2, 0.75), (1.8, 0.50), (2.4, 0.35)
    ]
    for idx, (py, pz_off) in enumerate(plate_positions):
        for side, sign in [("L", 1), ("R", -1)]:
            alt_shift = 0.12 * sign
            bpy.ops.mesh.primitive_cone_add(radius1=0.28 + pz_off * 0.25, depth=0.65 + pz_off * 0.5, 
                                           location=(sx + 0.22 * sign, sy + py + alt_shift, sz + 2.1 + pz_off * 0.6))
            plate = bpy.context.active_object
            plate.name = f"Stego_Plate_{side}_{idx}"
            plate.scale = (0.15, 1.0, 1.3)
            plate.rotation_euler = (0, math.radians(10 * sign), math.radians(5 * sign))
            plate.data.materials.append(mat_stego_plates)
            stego_objs.append(plate)

    # Long Tail with 4 Defensive Spikes (Thagomizer)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=2.8, location=(sx, sy + 3.4, sz + 1.25))
    tail = bpy.context.active_object
    tail.name = "Stego_Tail"
    tail.rotation_euler = (math.radians(-65), 0, 0)
    tail.scale = (0.6, 0.6, 1.0)
    tail.data.materials.append(mat_stego_skin)
    stego_objs.append(tail)
    
    for s_idx, (spk_x, spk_y, spk_z, rot_y) in enumerate([
        (0.28, 4.4, 1.4, 45), (-0.28, 4.4, 1.4, -45),
        (0.32, 4.8, 1.6, 55), (-0.32, 4.8, 1.6, -55)
    ]):
        bpy.ops.mesh.primitive_cone_add(radius1=0.08, depth=0.65, location=(sx + spk_x, sy + spk_y, sz + spk_z))
        spk = bpy.context.active_object
        spk.name = f"Stego_Spike_{s_idx}"
        spk.rotation_euler = (math.radians(20), math.radians(rot_y), 0)
        spk.data.materials.append(mat_stego_plates)
        stego_objs.append(spk)

    # 4 Legs
    for lx, ly in [(0.75, -1.2), (-0.75, -1.2), (0.75, 1.2), (-0.75, 1.2)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.30, depth=1.3, location=(sx + lx, sy + ly, sz + 0.65))
        leg = bpy.context.active_object
        leg.name = "Stego_Leg"
        leg.data.materials.append(mat_stego_skin)
        stego_objs.append(leg)

    return stego_objs


def build_lagoon_sauropod(location=(3.2, 11.5, -0.4)):
    import bpy, math
    lx, ly, lz = location
    sauro_objs = []
    
    # Graceful Long Arched Neck emerging from turquoise water
    bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=4.5, location=(lx, ly, lz + 2.8))
    neck = bpy.context.active_object
    neck.name = "Sauropod_Neck"
    neck.rotation_euler = (math.radians(22), 0, 0)
    neck.scale = (0.75, 0.85, 1.0)
    neck.data.materials.append(mat_sauropod)
    sauro_objs.append(neck)
    
    # Friendly Head
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=18, radius=0.40, location=(lx, ly - 0.9, lz + 4.9))
    shead = bpy.context.active_object
    shead.name = "Sauropod_Head"
    shead.scale = (0.75, 1.45, 0.85)
    shead.data.materials.append(mat_sauropod)
    sauro_objs.append(shead)
    
    for sign in [1, -1]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(lx + 0.24 * sign, ly - 1.1, lz + 5.05))
        seye = bpy.context.active_object
        seye.data.materials.append(mat_eye_pupil)
        sauro_objs.append(seye)

    return sauro_objs


def build_baby_trex(location=(-1.5, 5.8, 0.1)):
    import bpy, math
    tx, ty, tz = location
    trex_objs = []
    
    # Inquisitive Baby Dinosaur Head
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=18, radius=0.38, location=(tx, ty, tz + 0.9))
    head = bpy.context.active_object
    head.name = "BabyTrex_Head"
    head.scale = (0.85, 1.35, 1.1)
    head.rotation_euler = (math.radians(10), 0, math.radians(25))
    head.data.materials.append(mat_baby_trex)
    trex_objs.append(head)
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.09, location=(tx + 0.22, ty - 0.20, tz + 1.05))
    eye = bpy.context.active_object
    eye.data.materials.append(mat_eye_pupil)
    trex_objs.append(eye)

    return trex_objs

stego_objs = build_stegosaurus(location=(-2.6, 4.2, 0.0))
sauro_objs = build_lagoon_sauropod(location=(3.2, 11.5, -0.4))
trex_objs = build_baby_trex(location=(-1.5, 5.8, 0.1))

# Apply Shade Smooth & Subdivision Surface to all character meshes
for obj in scene.objects:
    if obj.type == 'MESH':
        for poly in obj.data.polygons:
            poly.use_smooth = True
        # Add Subdivision Surface for silky smooth Pixar geometry
        if any(tag in obj.name for tag in ["Leo_Head", "Leo_Nose", "Leo_Mouth", "Leo_Torso", "Puppy_Head", "Puppy_Body", "Puppy_Ear", "HairCluster"]):
            sub = obj.modifiers.new(name="Subsurf", type='SUBSURF')
            sub.levels = 1
            sub.render_levels = 2

# 6. Camera Director & Multi-Act Cinematography
cam_data = bpy.data.cameras.new("DirectorCamera")
cam_data.lens = 38
cam_data.dof.use_dof = True
cam_data.dof.aperture_fstop = 3.2

cam_obj = bpy.data.objects.new("DirectorCamera", cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

# 7. Animation Keyframing (4 Acts matching Demo Video)
for f in range(1, 300 + 1):
    # Leo Lip-Sync & Emotion Blendshapes
    if head_leo and head_leo.data.shape_keys:
        kb = head_leo.data.shape_keys.key_blocks
        if "jawOpen" in kb:
            if (65 <= f <= 135) or (165 <= f <= 275):
                jaw_val = abs(math.sin(f * 0.48)) * 0.70 + 0.12
                smile_val = 0.60 + 0.20 * math.sin(f * 0.22)
            else:
                jaw_val = 0.04
                smile_val = 0.45
                
            kb["jawOpen"].value = jaw_val
            kb["jawOpen"].keyframe_insert(data_path="value", frame=f)
            kb["mouthSmile"].value = smile_val
            kb["mouthSmile"].keyframe_insert(data_path="value", frame=f)
            if "wonderEmotion" in kb:
                kb["wonderEmotion"].value = 0.75
                kb["wonderEmotion"].keyframe_insert(data_path="value", frame=f)

    # Puppy Tail Wagging Animation
    if ptail:
        wag = math.sin(f * 0.75) * math.radians(30)
        ptail.rotation_euler = (math.radians(-45), 0, wag)
        ptail.keyframe_insert(data_path="rotation_euler", frame=f)

    # Puppy Sniffing & Looking Up
    if phead:
        if f <= 140:
            sniff = math.radians(16 + math.sin(f * 0.35) * 6)
            phead.rotation_euler = (sniff, 0, math.radians(-12))
        else:
            look_up = math.radians(-16 + math.sin(f * 0.18) * 5)
            phead.rotation_euler = (look_up, 0, math.radians(14))
        phead.keyframe_insert(data_path="rotation_euler", frame=f)

    # Camera Multi-Act Sequence (Cinematic Framing)
    if f <= 75:
        # ACT 1 (Frames 1-75): Majestic Establishing Landscape
        # Level angle showing Leo, Puppy, Volcano, and Waterfalls
        t1 = f / 75.0
        cam_obj.location = (0.05 + t1 * 0.1, -3.2 + t1 * 0.3, 1.25 + t1 * 0.05)
        cam_obj.rotation_euler = (math.radians(88), 0, math.radians(2))
        cam_data.lens = 35
        cam_data.dof.focus_distance = 3.0
    elif f <= 150:
        # ACT 2 (Frames 76-150): Medium Tracking Shot - Footprint Discovery
        t2 = (f - 75) / 75.0
        cam_obj.location = (0.15 + t2 * 0.1, -2.4 - t2 * 0.15, 0.95 - t2 * 0.1)
        cam_obj.rotation_euler = (math.radians(82 + t2 * 2), 0, math.radians(4))
        cam_data.lens = 42
        cam_data.dof.focus_distance = 2.0
    elif f <= 225:
        # ACT 3 (Frames 151-225): Macro Low-Angle Shot on Footprint
        t3 = (f - 150) / 75.0
        cam_obj.location = (0.28 - t3 * 0.12, -1.8 - t3 * 0.15, 0.65 + t3 * 0.15)
        cam_obj.rotation_euler = (math.radians(82), 0, math.radians(-3 + t3 * 4))
        cam_data.lens = 48
        cam_data.dof.focus_distance = 1.6
    else:
        # ACT 4 (Frames 226-300): Hero Close-Up & Grand Dinosaur Reveal
        t4 = (f - 225) / 75.0
        cam_obj.location = (-0.25 + t4 * 0.20, -1.85 - t4 * 0.35, 1.48 + t4 * 0.10)
        cam_obj.rotation_euler = (math.radians(88 - t4 * 3), 0, math.radians(-4 + t4 * 8))
        cam_data.lens = 50
        cam_data.dof.focus_distance = 1.85

    cam_obj.keyframe_insert(data_path="location", frame=f)
    cam_obj.keyframe_insert(data_path="rotation_euler", frame=f)
    cam_data.keyframe_insert(data_path="lens", frame=f)
    cam_data.dof.keyframe_insert(data_path="focus_distance", frame=f)

print("[MasterRenderer] Scene setup complete. Beginning high-definition animation render...")
bpy.ops.render.render(animation=True)
print("[MasterRenderer] 3D Animation render finished successfully.")

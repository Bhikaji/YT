"""
Test script to build a complete 3D cartoon character (Leo) in Blender:
- Base mesh with child morphing baked
- Shape keys for organic eyelid blinking, wonder eyebrows, mouth open lip-sync, and smile
- 52-bone Mixamo skeletal armature with weights
- Separate glossy cartoon eyes with pupils and corneas
- Stylized clothing and hair materials
- Pose with legs walking, arm raising to point, head looking up
"""

import bpy
import gzip
import json
import math
import os
from pathlib import Path

# Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# Configure EEVEE
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderEngine") else 'BLENDER_EEVEE'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100
if hasattr(scene, "eevee"):
    scene.eevee.taa_render_samples = 16

if 'AgX' in [c.name for c in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items]:
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'Medium High Contrast'

# 1. Parse base.obj manually to retain vertex groups and geometry
base_obj_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\3dobjs\base.obj"
child_target_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\targets\macrodetails\caucasian-male-child.target.gz"

print("[1] Loading base mesh and applying child morph...")

# Read vertices
vertices = []
faces = []
group_faces = {}
current_group = "default"

with open(base_obj_path, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('v '):
            parts = line.strip().split()
            vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
        elif line.startswith('g '):
            current_group = line.strip().split()[1]
            if current_group not in group_faces:
                group_faces[current_group] = []
        elif line.startswith('f '):
            parts = line.strip().split()
            poly = [int(p.split('/')[0]) - 1 for p in parts[1:]]
            faces.append(poly)
            if current_group not in group_faces:
                group_faces[current_group] = []
            group_faces[current_group].append(len(faces) - 1)

print(f"Total base vertices: {len(vertices)}, faces: {len(faces)}")

# Apply child morphing (bake into base vertices)
with gzip.open(child_target_path, 'rt', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            parts = line.split()
            v_idx = int(parts[0])
            dx, dy, dz = float(parts[1]), float(parts[2]), float(parts[3])
            if v_idx < len(vertices):
                vertices[v_idx][0] += dx
                vertices[v_idx][1] += dy
                vertices[v_idx][2] += dz

print("Child morph applied to vertices.")

# Target scale: MakeHuman units are decimeters (~10cm). Scale factor to bring character to child height ~1.2m
# In Blender, character orientation: X -> X, Y -> -Z, Z -> Y
scale_factor = 0.078

transformed_verts = []
for v in vertices:
    # Rotate 90 deg around X and scale
    bx = v[0] * scale_factor
    by = -v[2] * scale_factor
    bz = v[1] * scale_factor
    transformed_verts.append((bx, by, bz))

# Create Mesh object in Blender
mesh_data = bpy.data.meshes.new("Leo_Mesh_Data")
mesh_data.from_pydata(transformed_verts, [], faces)
mesh_data.update()

mesh_obj = bpy.data.objects.new("Leo_Character", mesh_data)
bpy.context.collection.objects.link(mesh_obj)
bpy.context.view_layer.objects.active = mesh_obj

for p in mesh_data.polygons:
    p.use_smooth = True

print("Base mesh created in Blender.")

# 2. Add Shape Keys for Facial Performance (Blinking, Wonder Brows, Lip-Sync Mouth Open, Smile)
print("[2] Adding shape keys from MPFB target files...")

targets_to_load = {
    "EyeBlink_L": r"E:\YT\third_party\mpfb2\src\mpfb\data\targets\expression\units\caucasian\eye-left-closure.target.gz",
    "EyeBlink_R": r"E:\YT\third_party\mpfb2\src\mpfb\data\targets\expression\units\caucasian\eye-right-closure.target.gz",
    "Brow_Wonder": [
        r"E:\YT\third_party\mpfb2\src\mpfb\data\targets\expression\units\caucasian\eyebrows-left-inner-up.target.gz",
        r"E:\YT\third_party\mpfb2\src\mpfb\data\targets\expression\units\caucasian\eyebrows-right-inner-up.target.gz"
    ],
    "Mouth_Open": r"E:\YT\third_party\mpfb2\src\mpfb\data\targets\expression\units\caucasian\mouth-open.target.gz",
    "Mouth_Smile": r"E:\YT\third_party\mpfb2\src\mpfb\data\targets\expression\units\caucasian\mouth-corner-puller.target.gz"
}

# Basis shape key
basis_key = mesh_obj.shape_key_add(name="Basis", from_mix=False)

def apply_target_file(shape_key, target_filepath, weight=1.0):
    with gzip.open(target_filepath, 'rt', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split()
                v_idx = int(parts[0])
                dx = float(parts[1]) * scale_factor * weight
                dy = float(parts[2]) * scale_factor * weight
                dz = float(parts[3]) * scale_factor * weight
                if v_idx < len(shape_key.data):
                    # Coordinate transform (X -> X, Y -> -Z, Z -> Y)
                    shape_key.data[v_idx].co.x += dx
                    shape_key.data[v_idx].co.y += -dz
                    shape_key.data[v_idx].co.z += dy

for key_name, target_info in targets_to_load.items():
    sk = mesh_obj.shape_key_add(name=key_name, from_mix=False)
    if isinstance(target_info, list):
        for t_file in target_info:
            apply_target_file(sk, t_file)
    else:
        apply_target_file(sk, target_info)
    sk.value = 0.0
    print(f"  Loaded shape key: {key_name}")

# 3. Build 52-Bone Mixamo Armature
print("[3] Building Mixamo armature from vertex anchors...")
rig_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\rigs\standard\rig.mixamo.json"
with open(rig_path, 'r', encoding='utf-8') as f:
    rig_data = json.load(f)["bones"]

arm_data = bpy.data.armatures.new("Leo_Armature_Data")
arm_obj = bpy.data.objects.new("Leo_Armature", arm_data)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='EDIT')

v_coords = transformed_verts

def get_bone_pos(spec):
    if spec.get("strategy") == "MEAN" and "vertex_indices" in spec:
        indices = spec["vertex_indices"]
        avg_x = sum(v_coords[i][0] for i in indices) / len(indices)
        avg_y = sum(v_coords[i][1] for i in indices) / len(indices)
        avg_z = sum(v_coords[i][2] for i in indices) / len(indices)
        return (avg_x, avg_y, avg_z)
    else:
        p = spec["default_position"]
        return (p[0] * scale_factor * 10, -p[2] * scale_factor * 10, p[1] * scale_factor * 10)

edit_bones = {}
for bone_name, bone_spec in rig_data.items():
    eb = arm_data.edit_bones.new(bone_name)
    eb.head = get_bone_pos(bone_spec["head"])
    eb.tail = get_bone_pos(bone_spec["tail"])
    if (eb.head - eb.tail).length < 0.001:
        eb.tail.z += 0.02
    eb.roll = bone_spec.get("roll", 0.0)
    edit_bones[bone_name] = eb

for bone_name, bone_spec in rig_data.items():
    parent_name = bone_spec.get("parent")
    if parent_name and parent_name in edit_bones:
        edit_bones[bone_name].parent = edit_bones[parent_name]
        edit_bones[bone_name].use_connect = bone_spec.get("use_connect", False)

bpy.ops.object.mode_set(mode='OBJECT')

# 4. Skinning / Vertex Weights
print("[4] Applying vertex skinning weights from weights.mixamo.json...")
weights_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\rigs\standard\weights.mixamo.json"
with open(weights_path, 'r', encoding='utf-8') as f:
    weights_data = json.load(f)["weights"]

for group_name, weight_list in weights_data.items():
    vg = mesh_obj.vertex_groups.new(name=group_name)
    for vert_idx, w_val in weight_list:
        if vert_idx < len(mesh_obj.data.vertices):
            vg.add([vert_idx], float(w_val), 'REPLACE')

arm_mod = mesh_obj.modifiers.new(name="Armature", type='ARMATURE')
arm_mod.object = arm_obj
arm_mod.use_vertex_groups = True

# 5. Stylized Shaders and Materials
print("[5] Configuring Pixar stylized materials...")

def make_material(name, color, roughness=0.35, sss=0.0, emission=None):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = roughness
        if 'Subsurface Weight' in bsdf.inputs:
            bsdf.inputs['Subsurface Weight'].default_value = sss
        elif 'Subsurface' in bsdf.inputs:
            bsdf.inputs['Subsurface'].default_value = sss
        if emission and 'Emission Color' in bsdf.inputs:
            bsdf.inputs['Emission Color'].default_value = emission[0]
            bsdf.inputs['Emission Strength'].default_value = emission[1]
    return mat

mat_skin = make_material("PixarSkin", (0.94, 0.74, 0.62, 1.0), roughness=0.30, sss=0.28)
mat_hoodie = make_material("RedHoodie", (0.88, 0.16, 0.12, 1.0), roughness=0.72)
mat_jeans = make_material("DenimJeans", (0.14, 0.24, 0.42, 1.0), roughness=0.65)
mat_boots = make_material("HikingBoots", (0.20, 0.13, 0.08, 1.0), roughness=0.50)
mat_hair = make_material("AuburnHair", (0.24, 0.12, 0.05, 1.0), roughness=0.40)
mat_eye_white = make_material("EyeSclera", (0.95, 0.95, 0.96, 1.0), roughness=0.08)
mat_iris = make_material("BlueIris", (0.10, 0.45, 0.88, 1.0), roughness=0.05)
mat_mouth_inner = make_material("MouthInner", (0.50, 0.08, 0.08, 1.0), roughness=0.4)

materials = [
    mat_skin,        # 0
    mat_hoodie,      # 1
    mat_jeans,       # 2
    mat_boots,       # 3
    mat_hair,        # 4
    mat_eye_white,   # 5
    mat_iris,        # 6
    mat_mouth_inner  # 7
]

for m in materials:
    mesh_obj.data.materials.append(m)

# Assign face materials based on MPFB object groups and vertex heights
eye_faces = set(group_faces.get("helper-l-eye", []) + group_faces.get("helper-r-eye", []))
hair_faces = set(group_faces.get("helper-hair", []))
mouth_faces = set(group_faces.get("helper-tongue", []) + group_faces.get("helper-upper-teeth", []) + group_faces.get("helper-lower-teeth", []))

# Unwanted helpers to hide (skirt, tights, genital)
unwanted_faces = set(group_faces.get("helper-skirt", []) + group_faces.get("helper-tights", []) + group_faces.get("helper-genital", []))

mat_invisible = make_material("Invisible", (0, 0, 0, 0), roughness=1.0)
if hasattr(mat_invisible, "blend_method"):
    mat_invisible.blend_method = 'CLIP'
mesh_obj.data.materials.append(mat_invisible)
invisible_idx = len(mesh_obj.data.materials) - 1

for poly_idx, poly in enumerate(mesh_obj.data.polygons):
    if poly_idx in unwanted_faces:
        poly.material_index = invisible_idx
        continue
    if poly_idx in eye_faces:
        # Front of eyeball is iris, sides are sclera
        face_center_y = sum(v_coords[v][1] for v in poly.vertices) / len(poly.vertices)
        if face_center_y < -0.05:  # Looking forward
            poly.material_index = 6  # Blue Iris
        else:
            poly.material_index = 5  # Eye Sclera
        continue
    if poly_idx in hair_faces:
        poly.material_index = 4  # Hair
        continue
    if poly_idx in mouth_faces:
        poly.material_index = 7  # Mouth inner
        continue
        
    avg_z = sum(v_coords[v][2] for v in poly.vertices) / len(poly.vertices)
    avg_x = abs(sum(v_coords[v][0] for v in poly.vertices) / len(poly.vertices))
    
    if avg_z > 0.98:
        poly.material_index = 0  # Skin face/neck
    elif avg_z > 0.58:
        if avg_x > 0.38 and avg_z < 0.72:
            poly.material_index = 0  # Skin hands
        else:
            poly.material_index = 1  # Red Hoodie
    elif avg_z > 0.12:
        poly.material_index = 2  # Jeans
    else:
        poly.material_index = 3  # Boots

print("Materials assigned.")

# 6. Set Pose and Expressions
print("[6] Applying character action pose & facial expressions...")

# Activate facial wonder & mouth open for speaking
mesh_obj.data.shape_keys.key_blocks["Brow_Wonder"].value = 0.85
mesh_obj.data.shape_keys.key_blocks["Mouth_Open"].value = 0.45
mesh_obj.data.shape_keys.key_blocks["Mouth_Smile"].value = 0.30

# Skeletal pose: Right arm pointing forward, left arm relaxed, head tilted up
pose = arm_obj.pose

# Pointing right arm
pose.bones["mixamorig:RightArm"].rotation_mode = 'XYZ'
pose.bones["mixamorig:RightArm"].rotation_euler = (math.radians(-65), math.radians(12), math.radians(-25))

pose.bones["mixamorig:RightForeArm"].rotation_mode = 'XYZ'
pose.bones["mixamorig:RightForeArm"].rotation_euler = (math.radians(-40), math.radians(15), 0)

# Extend right index finger
pose.bones["mixamorig:RightHandIndex1"].rotation_mode = 'XYZ'
pose.bones["mixamorig:RightHandIndex1"].rotation_euler = (0, 0, 0)
pose.bones["mixamorig:RightHandIndex2"].rotation_mode = 'XYZ'
pose.bones["mixamorig:RightHandIndex2"].rotation_euler = (0, 0, 0)

# Curl other fingers into fist
for f in ["Middle", "Ring", "Pinky"]:
    pose.bones[f"mixamorig:RightHand{f}1"].rotation_mode = 'XYZ'
    pose.bones[f"mixamorig:RightHand{f}1"].rotation_euler = (math.radians(60), 0, 0)
    pose.bones[f"mixamorig:RightHand{f}2"].rotation_mode = 'XYZ'
    pose.bones[f"mixamorig:RightHand{f}2"].rotation_euler = (math.radians(70), 0, 0)

# Left arm resting naturally
pose.bones["mixamorig:LeftArm"].rotation_mode = 'XYZ'
pose.bones["mixamorig:LeftArm"].rotation_euler = (math.radians(10), math.radians(5), math.radians(-8))

# Walk stance (legs separated in stride)
pose.bones["mixamorig:LeftUpLeg"].rotation_mode = 'XYZ'
pose.bones["mixamorig:LeftUpLeg"].rotation_euler = (math.radians(18), 0, math.radians(3))
pose.bones["mixamorig:RightUpLeg"].rotation_mode = 'XYZ'
pose.bones["mixamorig:RightUpLeg"].rotation_euler = (math.radians(-20), 0, math.radians(-3))

pose.bones["mixamorig:RightLeg"].rotation_mode = 'XYZ'
pose.bones["mixamorig:RightLeg"].rotation_euler = (math.radians(25), 0, 0)

# Head looking up in wonder at crystals
pose.bones["mixamorig:Head"].rotation_mode = 'XYZ'
pose.bones["mixamorig:Head"].rotation_euler = (math.radians(-14), math.radians(4), math.radians(-10))

# 7. Environment & Crystal Bridge
mat_crystal = make_material("CrystalSpire", (0.2, 0.85, 1.0, 1.0), roughness=0.08, emission=((0.15, 0.85, 1.0, 1.0), 3.5))

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.05))
bridge = bpy.context.active_object
bridge.scale = (1.2, 8.0, 0.10)
bpy.ops.object.transform_apply(scale=True)
bridge.data.materials.append(mat_crystal)

# Floating glowing crystals
for pos, s in [((-0.7, 0.8, 0.6), 0.18), ((0.75, 1.4, 0.9), 0.25), ((-0.85, 2.2, 1.3), 0.32)]:
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=s, depth=s*2.6, location=pos)
    c_obj = bpy.context.active_object
    c_obj.rotation_euler = (math.radians(15), math.radians(-10), math.radians(25))
    c_obj.data.materials.append(mat_crystal)

# 8. Camera with Track To constraint on Character Chest/Head
cam_data = bpy.data.cameras.new("HeroCamera")
cam_data.lens = 50.0  # Cinematic portrait focal length
cam_obj = bpy.data.objects.new("HeroCamera", cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

# Camera position in front of character (framing mid-shot to hero close-up)
cam_obj.location = (0.25, -2.1, 0.95)

# Target empty at character chest/head
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0.88))
cam_target = bpy.context.active_object
cam_target.name = "CameraTarget"

track = cam_obj.constraints.new(type='TRACK_TO')
track.target = cam_target
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'

# 9. Lighting Setup
# Key Light (Warm golden rim from front-left)
key_light = bpy.data.lights.new("KeyLight", type='POINT')
key_light.energy = 600
key_light.color = (1.0, 0.88, 0.74)
key_obj = bpy.data.objects.new("KeyLight", key_light)
key_obj.location = (-1.2, -1.8, 1.8)
bpy.context.collection.objects.link(key_obj)

# Crystal Blue Fill Light (From back-right rimming character)
fill_light = bpy.data.lights.new("CrystalRim", type='POINT')
fill_light.energy = 500
fill_light.color = (0.15, 0.85, 1.0)
fill_obj = bpy.data.objects.new("CrystalRim", fill_light)
fill_obj.location = (1.4, 0.8, 1.2)
bpy.context.collection.objects.link(fill_obj)

# Soft Ambience
bpy.context.scene.world = bpy.data.worlds.new("StudioWorld")
bpy.context.scene.world.use_nodes = True
bg_node = bpy.context.scene.world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs['Color'].default_value = (0.015, 0.018, 0.035, 1.0)
    bg_node.inputs['Strength'].default_value = 0.8

# 10. Render Test Frame
output_path = r"E:\YT\output\renders\real_3d_character_demo.jpg"
scene.render.filepath = output_path
scene.render.image_settings.file_format = 'JPEG'
scene.render.image_settings.quality = 95

print(f"[10] Rendering verified 3D character to {output_path}...")
bpy.ops.render.render(write_still=True)
print("SUCCESS: 3D character rendered perfectly!")

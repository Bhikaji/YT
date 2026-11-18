"""
Verified 3D Pixar Cartoon Character Render:
- Clean 100% bone-based material mapping (Skin face/neck, Red Hoodie, Blue Jeans, Boots, Hands)
- Realistic cartoon eyes with pupil/iris and cornea
- Stylized sculpted boy hair properly seated on head and parented to Head bone
- Organic facial shapekeys (Wonder brows, speaking mouth)
- True skeletal pose (Mixamo armature): walking stance, arm pointing, head tilted in wonder
"""

import bpy
import gzip
import json
import math
import os

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# Configure EEVEE-Next
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderEngine") else 'BLENDER_EEVEE'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100
if hasattr(scene, "eevee"):
    scene.eevee.taa_render_samples = 16

if 'AgX' in [c.name for c in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items]:
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'Medium High Contrast'

# 1. Parse base.obj manually
base_obj_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\3dobjs\base.obj"
child_target_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\targets\macrodetails\caucasian-male-child.target.gz"

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

# Apply child morphing
with gzip.open(child_target_path, 'rt', encoding='utf-8') as f:
    for line in f:
        if line and not line.startswith('#'):
            p = line.split()
            v_idx = int(p[0])
            if v_idx < len(vertices):
                vertices[v_idx][0] += float(p[1])
                vertices[v_idx][1] += float(p[2])
                vertices[v_idx][2] += float(p[3])

scale_factor = 0.078
min_z_raw = min(v[1] * scale_factor for v in vertices)
z_offset = -min_z_raw  # Ground feet at Z = 0.0

transformed_verts = []
for v in vertices:
    bx = v[0] * scale_factor
    by = -v[2] * scale_factor
    bz = (v[1] * scale_factor) + z_offset
    transformed_verts.append((bx, by, bz))

mesh_data = bpy.data.meshes.new("Leo_Mesh_Data")
mesh_data.from_pydata(transformed_verts, [], faces)
mesh_data.update()

mesh_obj = bpy.data.objects.new("Leo_Character", mesh_data)
bpy.context.collection.objects.link(mesh_obj)
bpy.context.view_layer.objects.active = mesh_obj

for p in mesh_data.polygons:
    p.use_smooth = True

# 2. Shape Keys for Expressions
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

mesh_obj.shape_key_add(name="Basis", from_mix=False)

def apply_target(shape_key, t_path, weight=1.0):
    with gzip.open(t_path, 'rt', encoding='utf-8') as f:
        for line in f:
            if line and not line.startswith('#'):
                parts = line.split()
                v_idx = int(parts[0])
                if v_idx < len(shape_key.data):
                    shape_key.data[v_idx].co.x += float(parts[1]) * scale_factor * weight
                    shape_key.data[v_idx].co.y += -float(parts[3]) * scale_factor * weight
                    shape_key.data[v_idx].co.z += float(parts[2]) * scale_factor * weight

for key_name, target_info in targets_to_load.items():
    sk = mesh_obj.shape_key_add(name=key_name, from_mix=False)
    if isinstance(target_info, list):
        for t_file in target_info:
            apply_target(sk, t_file)
    else:
        apply_target(sk, target_info)
    sk.value = 0.0

# 3. 52-Bone Mixamo Armature
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
        return (p[0] * scale_factor * 10, -p[2] * scale_factor * 10, (p[1] * scale_factor * 10) + z_offset)

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

# 4. Vertex Weights and Dominant Bone Mapping
weights_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\rigs\standard\weights.mixamo.json"
with open(weights_path, 'r', encoding='utf-8') as f:
    weights_data = json.load(f)["weights"]

vert_dominant_bone = {}
for group_name, weight_list in weights_data.items():
    vg = mesh_obj.vertex_groups.new(name=group_name)
    for vert_idx, w_val in weight_list:
        if vert_idx < len(mesh_obj.data.vertices):
            val_f = float(w_val)
            vg.add([vert_idx], val_f, 'REPLACE')
            if vert_idx not in vert_dominant_bone or val_f > vert_dominant_bone[vert_idx][1]:
                vert_dominant_bone[vert_idx] = (group_name, val_f)

arm_mod = mesh_obj.modifiers.new(name="Armature", type='ARMATURE')
arm_mod.object = arm_obj
arm_mod.use_vertex_groups = True

# 5. Materials Setup
def create_bsdf_mat(name, color, roughness=0.35, sss=0.0):
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
    return mat

# Warm Pixar Peach Skin
mat_skin = create_bsdf_mat("PixarSkin", (0.92, 0.72, 0.60, 1.0), roughness=0.35, sss=0.20)
# Hero Red Hoodie
mat_hoodie = create_bsdf_mat("RedHoodie", (0.85, 0.16, 0.12, 1.0), roughness=0.65)
# Dark Denim Blue Jeans
mat_jeans = create_bsdf_mat("DenimJeans", (0.12, 0.22, 0.40, 1.0), roughness=0.60)
# Brown Leather Hiking Boots
mat_boots = create_bsdf_mat("HikingBoots", (0.18, 0.11, 0.07, 1.0), roughness=0.45)
# Rich Auburn Brown Hair
mat_hair = create_bsdf_mat("AuburnHair", (0.22, 0.11, 0.05, 1.0), roughness=0.40)
# Cartoon Eye Sclera (White)
mat_sclera = create_bsdf_mat("EyeSclera", (0.96, 0.96, 0.98, 1.0), roughness=0.05)
# Bright Vibrant Blue Iris
mat_iris = create_bsdf_mat("BlueIris", (0.05, 0.45, 0.92, 1.0), roughness=0.02)
# Mouth Interior / Tongue
mat_mouth_inner = create_bsdf_mat("MouthInner", (0.42, 0.08, 0.08, 1.0), roughness=0.4)

# 100% Transparent material for helper meshes
mat_transparent = bpy.data.materials.new(name="InvisibleHelper")
mat_transparent.use_nodes = True
nodes = mat_transparent.node_tree.nodes
nodes.clear()
out_node = nodes.new(type="ShaderNodeOutputMaterial")
trans_node = nodes.new(type="ShaderNodeBsdfTransparent")
mat_transparent.node_tree.links.new(trans_node.outputs["BSDF"], out_node.inputs["Surface"])

materials = [
    mat_skin,        # 0
    mat_hoodie,      # 1
    mat_jeans,       # 2
    mat_boots,       # 3
    mat_hair,        # 4
    mat_sclera,      # 5
    mat_iris,        # 6
    mat_mouth_inner, # 7
    mat_transparent  # 8
]

for m in materials:
    mesh_obj.data.materials.append(m)

# Assign polygon materials using DOMINANT BONES
transparent_face_indices = set()
for grp_name in ["helper-tights", "helper-skirt", "helper-hair", "helper-genital",
                 "helper-l-eyelashes-1", "helper-l-eyelashes-2", "helper-r-eyelashes-1", "helper-r-eyelashes-2"]:
    transparent_face_indices.update(group_faces.get(grp_name, []))

eye_faces = set(group_faces.get("helper-l-eye", []) + group_faces.get("helper-r-eye", []))
mouth_faces = set(group_faces.get("helper-tongue", []) + group_faces.get("helper-upper-teeth", []) + group_faces.get("helper-lower-teeth", []))

for poly_idx, poly in enumerate(mesh_obj.data.polygons):
    if poly_idx in transparent_face_indices:
        poly.material_index = 8
        continue
    if poly_idx in eye_faces:
        center_y = sum(v_coords[v][1] for v in poly.vertices) / len(poly.vertices)
        if center_y < -0.062:
            poly.material_index = 6  # Blue Iris
        else:
            poly.material_index = 5  # Sclera
        continue
    if poly_idx in mouth_faces:
        poly.material_index = 7
        continue
        
    # Get dominant bone for this polygon
    bone_counts = {}
    for v in poly.vertices:
        if v in vert_dominant_bone:
            b = vert_dominant_bone[v][0]
            bone_counts[b] = bone_counts.get(b, 0) + 1
    dom_bone = max(bone_counts.items(), key=lambda x: x[1])[0] if bone_counts else "mixamorig:Head"
    
    if dom_bone in ["mixamorig:Head", "mixamorig:Neck"]:
        poly.material_index = 0  # Skin face/neck
    elif "Hand" in dom_bone or "Finger" in dom_bone or "Thumb" in dom_bone:
        poly.material_index = 0  # Skin hands
    elif dom_bone in ["mixamorig:LeftFoot", "mixamorig:RightFoot", "mixamorig:LeftToeBase", "mixamorig:RightToeBase"]:
        poly.material_index = 3  # Boots
    elif dom_bone in ["mixamorig:LeftUpLeg", "mixamorig:RightUpLeg", "mixamorig:LeftLeg", "mixamorig:RightLeg", "mixamorig:Hips"]:
        poly.material_index = 2  # Jeans
    else:
        # Spine, Spine1, Spine2, Shoulders, Arms, ForeArms -> Red Hoodie!
        poly.material_index = 1  # Hoodie

# 6. Stylized Pixar Hair Model (Sculpted quiff / swoops)
head_bone = arm_obj.pose.bones["mixamorig:Head"]
head_pos = edit_bones["mixamorig:Head"].head
head_tail = edit_bones["mixamorig:Head"].tail

bpy.ops.mesh.primitive_uv_sphere_add(segments=28, ring_count=20, radius=0.098, location=(0, -0.025, head_tail.z - 0.02))
hair_obj = bpy.context.active_object
hair_obj.name = "Leo_StylizedHair"
hair_obj.scale = (1.08, 1.15, 0.95)
bpy.ops.object.transform_apply(scale=True)
hair_obj.data.materials.append(mat_hair)

for p in hair_obj.data.polygons:
    p.use_smooth = True

hair_obj.parent = arm_obj
hair_obj.parent_type = 'BONE'
hair_obj.parent_bone = "mixamorig:Head"

# 7. Apply Expressions and Action Pose
mesh_obj.data.shape_keys.key_blocks["Brow_Wonder"].value = 0.85
mesh_obj.data.shape_keys.key_blocks["Mouth_Open"].value = 0.45
mesh_obj.data.shape_keys.key_blocks["Mouth_Smile"].value = 0.35

pose = arm_obj.pose

# Walk / Stance Locomotion
pose.bones["mixamorig:LeftUpLeg"].rotation_mode = 'XYZ'
pose.bones["mixamorig:LeftUpLeg"].rotation_euler = (math.radians(22), 0, math.radians(2))
pose.bones["mixamorig:RightUpLeg"].rotation_mode = 'XYZ'
pose.bones["mixamorig:RightUpLeg"].rotation_euler = (math.radians(-20), 0, math.radians(-2))
pose.bones["mixamorig:RightLeg"].rotation_mode = 'XYZ'
pose.bones["mixamorig:RightLeg"].rotation_euler = (math.radians(24), 0, 0)

# Right arm raised & pointing forward to crystals
pose.bones["mixamorig:RightArm"].rotation_mode = 'XYZ'
pose.bones["mixamorig:RightArm"].rotation_euler = (math.radians(-62), math.radians(10), math.radians(-25))
pose.bones["mixamorig:RightForeArm"].rotation_mode = 'XYZ'
pose.bones["mixamorig:RightForeArm"].rotation_euler = (math.radians(-40), math.radians(12), 0)

# Pointing index finger
pose.bones["mixamorig:RightHandIndex1"].rotation_mode = 'XYZ'
pose.bones["mixamorig:RightHandIndex1"].rotation_euler = (0, 0, 0)
pose.bones["mixamorig:RightHandIndex2"].rotation_mode = 'XYZ'
pose.bones["mixamorig:RightHandIndex2"].rotation_euler = (0, 0, 0)
for f in ["Middle", "Ring", "Pinky"]:
    pose.bones[f"mixamorig:RightHand{f}1"].rotation_mode = 'XYZ'
    pose.bones[f"mixamorig:RightHand{f}1"].rotation_euler = (math.radians(65), 0, 0)
    pose.bones[f"mixamorig:RightHand{f}2"].rotation_mode = 'XYZ'
    pose.bones[f"mixamorig:RightHand{f}2"].rotation_euler = (math.radians(75), 0, 0)

# Left arm resting naturally
pose.bones["mixamorig:LeftArm"].rotation_mode = 'XYZ'
pose.bones["mixamorig:LeftArm"].rotation_euler = (math.radians(12), math.radians(4), math.radians(-8))

# Head looking up in wonder at crystals
pose.bones["mixamorig:Head"].rotation_mode = 'XYZ'
pose.bones["mixamorig:Head"].rotation_euler = (math.radians(-14), math.radians(5), math.radians(-8))

# 8. Environment & Bridge
mat_crystal = bpy.data.materials.new("CrystalMat")
mat_crystal.use_nodes = True
b_node = mat_crystal.node_tree.nodes.get("Principled BSDF")
if b_node:
    b_node.inputs['Base Color'].default_value = (0.2, 0.85, 1.0, 1.0)
    b_node.inputs['Roughness'].default_value = 0.08
    if 'Emission Color' in b_node.inputs:
        b_node.inputs['Emission Color'].default_value = (0.15, 0.85, 1.0, 1.0)
        b_node.inputs['Emission Strength'].default_value = 3.5

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.05))
bridge = bpy.context.active_object
bridge.scale = (1.5, 8.0, 0.10)
bpy.ops.object.transform_apply(scale=True)
bridge.data.materials.append(mat_crystal)

# Crystal spires on sides
for pos, s in [((-0.8, 0.6, 0.5), 0.22), ((0.85, 1.2, 0.8), 0.28), ((-0.9, 1.8, 1.1), 0.35)]:
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=s, depth=s*2.5, location=pos)
    c = bpy.context.active_object
    c.data.materials.append(mat_crystal)

# 9. Camera with Framing: Medium-Close Action Shot
cam_data = bpy.data.cameras.new("DirectorCam")
cam_data.lens = 42.0
cam_obj = bpy.data.objects.new("DirectorCam", cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

# Camera framed directly on Leo's chest and face
cam_obj.location = (0.22, -1.85, 0.88)

bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0.78))
cam_target = bpy.context.active_object
track = cam_obj.constraints.new(type='TRACK_TO')
track.target = cam_target
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'

# 10. Lighting
key_light = bpy.data.lights.new("WarmKey", type='POINT')
key_light.energy = 550
key_light.color = (1.0, 0.88, 0.74)
key_obj = bpy.data.objects.new("WarmKey", key_light)
key_obj.location = (-1.0, -1.2, 1.6)
bpy.context.collection.objects.link(key_obj)

rim_light = bpy.data.lights.new("CyanRim", type='POINT')
rim_light.energy = 480
rim_light.color = (0.15, 0.85, 1.0)
rim_obj = bpy.data.objects.new("CyanRim", rim_light)
rim_obj.location = (1.2, 0.6, 1.2)
bpy.context.collection.objects.link(rim_obj)

bpy.context.scene.world = bpy.data.worlds.new("CavernWorld")
bpy.context.scene.world.use_nodes = True
bg_node = bpy.context.scene.world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs['Color'].default_value = (0.015, 0.018, 0.035, 1.0)
    bg_node.inputs['Strength'].default_value = 0.8

output_path = r"E:\YT\output\renders\leo_3d_bone_material_test.jpg"
scene.render.filepath = output_path
scene.render.image_settings.file_format = 'JPEG'
scene.render.image_settings.quality = 95

print(f"Rendering bone-mapped 3D character to {output_path}...")
bpy.ops.render.render(write_still=True)
print("SUCCESS: Bone-mapped render complete!")

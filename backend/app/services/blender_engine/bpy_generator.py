import json
import os
from pathlib import Path
from typing import Dict, Any, List
from backend.app.schemas.script import GeneratedEpisodeScript, ScriptScene

class BpyScriptGenerator:
    """Generates standalone Python scripts executed headlessly by Blender (bpy)."""

    @classmethod
    def generate_blender_render_script(
        cls,
        script: GeneratedEpisodeScript,
        output_script_path: str,
        output_frames_dir: str,
        viseme_data_map: Dict[str, str],  # dialogue line index -> viseme JSON path
        resolution: tuple = (1080, 1920),
        fps: int = 30,
        total_frames: int = 300
    ) -> str:
        """
        Creates a self-contained Python script to drive Blender headless rendering
        with MakeHuman child mesh, 52 Mixamo bones, facial shapekeys, and PBR materials.
        """
        script_content = f'''# Auto-generated Blender 3D Automation Script by Autonomous AI Cartoon Studio
import bpy
import gzip
import json
import os
import math

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderEngine") else 'BLENDER_EEVEE'
scene.render.resolution_x = {resolution[0]}
scene.render.resolution_y = {resolution[1]}
scene.render.resolution_percentage = 100
scene.render.fps = {fps}
scene.frame_start = 1
scene.frame_end = {total_frames}

if hasattr(scene, "eevee"):
    scene.eevee.taa_render_samples = 8

if 'AgX' in [c.name for c in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items]:
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'Medium High Contrast'
else:
    scene.view_settings.view_transform = 'Filmic'

os.makedirs(r"{output_frames_dir}", exist_ok=True)
scene.render.filepath = os.path.join(r"{output_frames_dir}", "frame_")
scene.render.image_settings.file_format = 'JPEG'
scene.render.image_settings.quality = 95

# 1. Load Base Mesh & Child Target
base_obj_path = r"E:\\YT\\third_party\\mpfb2\\src\\mpfb\\data\\3dobjs\\base.obj"
child_target_path = r"E:\\YT\\third_party\\mpfb2\\src\\mpfb\\data\\targets\\macrodetails\\caucasian-male-child.target.gz"

vertices = []
faces = []
group_faces = {{}}
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
z_offset = -min_z_raw

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

# 2. Shape Keys
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

targets_to_load = {{
    "EyeBlink_L": r"E:\\YT\\third_party\\mpfb2\\src\\mpfb\\data\\targets\\expression\\units\\caucasian\\eye-left-closure.target.gz",
    "EyeBlink_R": r"E:\\YT\\third_party\\mpfb2\\src\\mpfb\\data\\targets\\expression\\units\\caucasian\\eye-right-closure.target.gz",
    "Brow_Wonder": [
        r"E:\\YT\\third_party\\mpfb2\\src\\mpfb\\data\\targets\\expression\\units\\caucasian\\eyebrows-left-inner-up.target.gz",
        r"E:\\YT\\third_party\\mpfb2\\src\\mpfb\\data\\targets\\expression\\units\\caucasian\\eyebrows-right-inner-up.target.gz"
    ],
    "Mouth_Open": r"E:\\YT\\third_party\\mpfb2\\src\\mpfb\\data\\targets\\expression\\units\\caucasian\\mouth-open.target.gz",
    "Mouth_Smile": r"E:\\YT\\third_party\\mpfb2\\src\\mpfb\\data\\targets\\expression\\units\\caucasian\\mouth-corner-puller.target.gz"
}}

for key_name, target_info in targets_to_load.items():
    sk = mesh_obj.shape_key_add(name=key_name, from_mix=False)
    if isinstance(target_info, list):
        for t_file in target_info:
            apply_target(sk, t_file)
    else:
        apply_target(sk, target_info)
    sk.value = 0.0

# 3. 52-Bone Mixamo Armature
rig_path = r"E:\\YT\\third_party\\mpfb2\\src\\mpfb\\data\\rigs\\standard\\rig.mixamo.json"
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

edit_bones = {{}}
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

# 4. Weights
weights_path = r"E:\\YT\\third_party\\mpfb2\\src\\mpfb\\data\\rigs\\standard\\weights.mixamo.json"
with open(weights_path, 'r', encoding='utf-8') as f:
    weights_data = json.load(f)["weights"]

vert_dominant_bone = {{}}
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

# 5. Materials
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

mat_skin = create_bsdf_mat("PixarSkin", (0.92, 0.72, 0.60, 1.0), roughness=0.35, sss=0.20)
mat_hoodie = create_bsdf_mat("RedHoodie", (0.85, 0.16, 0.12, 1.0), roughness=0.65)
mat_jeans = create_bsdf_mat("DenimJeans", (0.12, 0.22, 0.40, 1.0), roughness=0.60)
mat_boots = create_bsdf_mat("HikingBoots", (0.18, 0.11, 0.07, 1.0), roughness=0.45)
mat_hair = create_bsdf_mat("AuburnHair", (0.22, 0.11, 0.05, 1.0), roughness=0.40)
mat_sclera = create_bsdf_mat("EyeSclera", (0.96, 0.96, 0.98, 1.0), roughness=0.05)
mat_iris = create_bsdf_mat("BlueIris", (0.05, 0.45, 0.92, 1.0), roughness=0.02)
mat_mouth_inner = create_bsdf_mat("MouthInner", (0.42, 0.08, 0.08, 1.0), roughness=0.4)

mat_transparent = bpy.data.materials.new(name="InvisibleHelper")
mat_transparent.use_nodes = True
t_nodes = mat_transparent.node_tree.nodes
t_nodes.clear()
out_node = t_nodes.new(type="ShaderNodeOutputMaterial")
trans_node = t_nodes.new(type="ShaderNodeBsdfTransparent")
mat_transparent.node_tree.links.new(trans_node.outputs["BSDF"], out_node.inputs["Surface"])

materials = [mat_skin, mat_hoodie, mat_jeans, mat_boots, mat_hair, mat_sclera, mat_iris, mat_mouth_inner, mat_transparent]
for m in materials:
    mesh_obj.data.materials.append(m)

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
        poly.material_index = 6 if center_y < -0.062 else 5
        continue
    if poly_idx in mouth_faces:
        poly.material_index = 7
        continue
    bone_counts = {{}}
    for v in poly.vertices:
        if v in vert_dominant_bone:
            b = vert_dominant_bone[v][0]
            bone_counts[b] = bone_counts.get(b, 0) + 1
    dom_bone = max(bone_counts.items(), key=lambda x: x[1])[0] if bone_counts else "mixamorig:Head"
    if dom_bone in ["mixamorig:Head", "mixamorig:Neck"]:
        poly.material_index = 0
    elif "Hand" in dom_bone or "Finger" in dom_bone or "Thumb" in dom_bone:
        poly.material_index = 0
    elif dom_bone in ["mixamorig:LeftFoot", "mixamorig:RightFoot", "mixamorig:LeftToeBase", "mixamorig:RightToeBase"]:
        poly.material_index = 3
    elif dom_bone in ["mixamorig:LeftUpLeg", "mixamorig:RightUpLeg", "mixamorig:LeftLeg", "mixamorig:RightLeg", "mixamorig:Hips"]:
        poly.material_index = 2
    else:
        poly.material_index = 1

# 6. Sculpted Hair Parented to Head Bone
head_tail_z = edit_bones["mixamorig:Head"].tail.z
bpy.ops.mesh.primitive_uv_sphere_add(segments=28, ring_count=20, radius=0.098, location=(0, -0.025, head_tail_z - 0.02))
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

# 7. Environment & Lighting
def make_emission_mat(name, color, roughness=0.2, strength=2.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = roughness
        if 'Emission Color' in bsdf.inputs:
            bsdf.inputs['Emission Color'].default_value = color
            bsdf.inputs['Emission Strength'].default_value = strength
    return mat

mat_crystal = make_emission_mat("CrystalBridgeMat", (0.22, 0.82, 1.0, 1.0), roughness=0.1, strength=1.8)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.06))
bridge = bpy.context.active_object
bridge.scale = (1.4, 14.0, 0.12)
bpy.ops.object.transform_apply(scale=True)
bridge.data.materials.append(mat_crystal)

# Key Light
key_light = bpy.data.lights.new("WarmKey", type='POINT')
key_light.energy = 750
key_light.color = (1.0, 0.88, 0.74)
key_obj = bpy.data.objects.new("WarmKey", key_light)
key_obj.location = (-1.2, -1.6, 2.2)
bpy.context.collection.objects.link(key_obj)

# Cyan Rim Light
rim_light = bpy.data.lights.new("CyanRim", type='POINT')
rim_light.energy = 550
rim_light.color = (0.2, 0.82, 1.0)
rim_obj = bpy.data.objects.new("CyanRim", rim_light)
rim_obj.location = (1.5, 0.2, 1.0)
bpy.context.collection.objects.link(rim_obj)

# Camera
cam_data = bpy.data.cameras.new("DirectorCamera")
cam_data.lens = 38.0
cam_data.dof.use_dof = True
cam_data.dof.focus_distance = 3.2
cam_data.dof.aperture_fstop = 2.8
cam_obj = bpy.data.objects.new("DirectorCamera", cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

cam_obj.location = (0.35, -4.6, 1.25)
cam_obj.rotation_euler = (math.radians(84), 0, math.radians(-4))
cam_obj.keyframe_insert(data_path="location", frame=1)
cam_obj.keyframe_insert(data_path="rotation_euler", frame=1)

cam_obj.location = (0.15, -2.8, 1.15)
cam_obj.rotation_euler = (math.radians(86), 0, math.radians(-2))
cam_obj.keyframe_insert(data_path="location", frame=150)
cam_obj.keyframe_insert(data_path="rotation_euler", frame=150)

cam_obj.location = (-0.16, -1.25, 1.18)
cam_obj.rotation_euler = (math.radians(92), 0, math.radians(7))
cam_obj.keyframe_insert(data_path="location", frame=151)
cam_obj.keyframe_insert(data_path="rotation_euler", frame=151)

cam_obj.location = (-0.12, -1.05, 1.20)
cam_obj.rotation_euler = (math.radians(93), 0, math.radians(5))
cam_obj.keyframe_insert(data_path="location", frame={total_frames})
cam_obj.keyframe_insert(data_path="rotation_euler", frame={total_frames})

# 8. Animate Timeline (Bones & ShapeKeys)
pose = arm_obj.pose
for b in pose.bones:
    b.rotation_mode = 'XYZ'

sk_blocks = mesh_obj.data.shape_keys.key_blocks
sk_brow = sk_blocks["Brow_Wonder"]
sk_mouth = sk_blocks["Mouth_Open"]
sk_smile = sk_blocks["Mouth_Smile"]
sk_blink_l = sk_blocks["EyeBlink_L"]
sk_blink_r = sk_blocks["EyeBlink_R"]

walk_cycle_frames = 28

for f in range(1, {total_frames} + 1):
    if f <= 90:
        phase = (f % walk_cycle_frames) / float(walk_cycle_frames) * (2 * math.pi)
        root_y = -2.2 + (f / 90.0) * 1.5
        pose.bones["mixamorig:Hips"].location = (0, root_y, math.sin(2 * phase) * 0.025)
        pose.bones["mixamorig:Hips"].rotation_euler = (0, math.sin(phase) * 0.035, 0)
        pose.bones["mixamorig:Hips"].keyframe_insert(data_path="location", frame=f)
        pose.bones["mixamorig:Hips"].keyframe_insert(data_path="rotation_euler", frame=f)
        
        leg_swing = math.sin(phase) * 0.44
        pose.bones["mixamorig:LeftUpLeg"].rotation_euler = (leg_swing, 0, math.radians(2))
        pose.bones["mixamorig:RightUpLeg"].rotation_euler = (-leg_swing, 0, math.radians(-2))
        pose.bones["mixamorig:LeftLeg"].rotation_euler = (max(0.0, -math.sin(phase) * 0.50), 0, 0)
        pose.bones["mixamorig:RightLeg"].rotation_euler = (max(0.0, math.sin(phase) * 0.50), 0, 0)
        pose.bones["mixamorig:LeftUpLeg"].keyframe_insert(data_path="rotation_euler", frame=f)
        pose.bones["mixamorig:RightUpLeg"].keyframe_insert(data_path="rotation_euler", frame=f)
        pose.bones["mixamorig:LeftLeg"].keyframe_insert(data_path="rotation_euler", frame=f)
        pose.bones["mixamorig:RightLeg"].keyframe_insert(data_path="rotation_euler", frame=f)
        
        pose.bones["mixamorig:LeftArm"].rotation_euler = (math.radians(15) - leg_swing * 0.7, 0, math.radians(-10))
        pose.bones["mixamorig:RightArm"].rotation_euler = (math.radians(15) + leg_swing * 0.7, 0, math.radians(10))
        pose.bones["mixamorig:LeftArm"].keyframe_insert(data_path="rotation_euler", frame=f)
        pose.bones["mixamorig:RightArm"].keyframe_insert(data_path="rotation_euler", frame=f)
        
        blink_val = math.sin((f - 36) / 6.0 * math.pi) if 36 <= f <= 42 else 0.0
        sk_blink_l.value = max(0.0, blink_val)
        sk_blink_r.value = max(0.0, blink_val)
        sk_blink_l.keyframe_insert(data_path="value", frame=f)
        sk_blink_r.keyframe_insert(data_path="value", frame=f)
        sk_mouth.value = 0.0
        sk_mouth.keyframe_insert(data_path="value", frame=f)
        sk_brow.value = 0.2
        sk_brow.keyframe_insert(data_path="value", frame=f)
    elif f <= 150:
        prog = (f - 90) / 60.0
        pose.bones["mixamorig:Hips"].location = (0, -0.7, 0)
        pose.bones["mixamorig:Hips"].rotation_euler = (0, 0, 0)
        pose.bones["mixamorig:Hips"].keyframe_insert(data_path="location", frame=f)
        pose.bones["mixamorig:Hips"].keyframe_insert(data_path="rotation_euler", frame=f)
        
        arm_up = min(1.0, prog * 1.6)
        pose.bones["mixamorig:RightArm"].rotation_euler = (math.radians(-65 * arm_up), math.radians(12 * arm_up), math.radians(-28 * arm_up))
        pose.bones["mixamorig:RightForeArm"].rotation_euler = (math.radians(-25 * arm_up), math.radians(8 * arm_up), 0)
        pose.bones["mixamorig:RightArm"].keyframe_insert(data_path="rotation_euler", frame=f)
        pose.bones["mixamorig:RightForeArm"].keyframe_insert(data_path="rotation_euler", frame=f)
        
        head_tilt = min(1.0, prog * 1.4)
        pose.bones["mixamorig:Head"].rotation_euler = (math.radians(-14 * head_tilt), 0, math.radians(-8 * head_tilt))
        pose.bones["mixamorig:Head"].keyframe_insert(data_path="rotation_euler", frame=f)
        
        sk_brow.value = min(0.85, 0.2 + prog * 1.1)
        sk_brow.keyframe_insert(data_path="value", frame=f)
        sk_smile.value = min(0.40, prog * 0.8)
        sk_smile.keyframe_insert(data_path="value", frame=f)
        
        speech_aperture = max(0.0, math.sin((f - 98) * 0.42) * 0.45 + 0.32) if 98 <= f <= 145 else 0.0
        sk_mouth.value = speech_aperture
        sk_mouth.keyframe_insert(data_path="value", frame=f)
        
        blink_val = math.sin((f - 114) / 6.0 * math.pi) if 114 <= f <= 120 else 0.0
        sk_blink_l.value = max(0.0, blink_val)
        sk_blink_r.value = max(0.0, blink_val)
        sk_blink_l.keyframe_insert(data_path="value", frame=f)
        sk_blink_r.keyframe_insert(data_path="value", frame=f)
    else:
        local_f = f - 151
        pose.bones["mixamorig:RightArm"].rotation_euler = (math.radians(-15), math.radians(8), math.radians(-14))
        pose.bones["mixamorig:RightForeArm"].rotation_euler = (math.radians(35), 0, 0)
        pose.bones["mixamorig:RightArm"].keyframe_insert(data_path="rotation_euler", frame=f)
        pose.bones["mixamorig:RightForeArm"].keyframe_insert(data_path="rotation_euler", frame=f)
        
        head_cycle = math.sin(local_f * 0.06) * 3
        pose.bones["mixamorig:Head"].rotation_euler = (math.radians(-6 + head_cycle), math.radians(-4), math.radians(6))
        pose.bones["mixamorig:Head"].keyframe_insert(data_path="rotation_euler", frame=f)
        
        sk_brow.value = 0.48 + math.sin(local_f * 0.08) * 0.12
        sk_brow.keyframe_insert(data_path="value", frame=f)
        sk_smile.value = 0.25
        sk_smile.keyframe_insert(data_path="value", frame=f)
        
        speech_aperture = max(0.0, math.sin((f - 168) * 0.38) * 0.42 + 0.28) if 168 <= f <= 285 else 0.0
        sk_mouth.value = speech_aperture
        sk_mouth.keyframe_insert(data_path="value", frame=f)
        
        blink_val = math.sin((f - 216) / 8.0 * math.pi) if 216 <= f <= 224 else 0.0
        sk_blink_l.value = max(0.0, blink_val)
        sk_blink_r.value = max(0.0, blink_val)
        sk_blink_l.keyframe_insert(data_path="value", frame=f)
        sk_blink_r.keyframe_insert(data_path="value", frame=f)

print("[Blender Engine] Executing genuine 3D render...")
bpy.ops.render.render(animation=True)
print("[Blender Engine] 3D Render complete!")
'''
        with open(output_script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)

        return output_script_path

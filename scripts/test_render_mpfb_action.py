"""
Renders a single action frame (Frame 110: Leo pointing hand, jaw open speaking, crystal bridge)
in Blender 4.2 LTS to verify mesh skinning and visual materials.
"""

import bpy
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

# Color profile
if 'AgX' in [c.name for c in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items]:
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'Medium High Contrast'

# 1. Import base.obj
scale_factor = 0.082
base_obj_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\3dobjs\base.obj"
bpy.ops.wm.obj_import(filepath=base_obj_path)
mesh = bpy.context.active_object
mesh.name = "Leo_Mesh"

mesh.rotation_euler = (math.radians(90), 0, 0)
bpy.ops.object.transform_apply(rotation=True)
mesh.scale = (scale_factor, scale_factor, scale_factor)
bpy.ops.object.transform_apply(scale=True)

for p in mesh.data.polygons:
    p.use_smooth = True

v_coords = [v.co.copy() for v in mesh.data.vertices]

# 2. Build Armature from rig.mixamo.json
rig_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\rigs\standard\rig.mixamo.json"
with open(rig_path, 'r', encoding='utf-8') as f:
    rig_data = json.load(f)["bones"]

arm_data = bpy.data.armatures.new("Leo_Armature_Data")
arm_obj = bpy.data.objects.new("Leo_Armature", arm_data)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='EDIT')

def get_pos(spec):
    if spec.get("strategy") == "MEAN" and "vertex_indices" in spec:
        indices = spec["vertex_indices"]
        avg_x = sum(v_coords[i].x for i in indices) / len(indices)
        avg_y = sum(v_coords[i].y for i in indices) / len(indices)
        avg_z = sum(v_coords[i].z for i in indices) / len(indices)
        return (avg_x, avg_y, avg_z)
    else:
        p = spec["default_position"]
        return (p[0] * scale_factor * 10, -p[2] * scale_factor * 10, p[1] * scale_factor * 10)

edit_bones = {}
for bone_name, bone_spec in rig_data.items():
    eb = arm_data.edit_bones.new(bone_name)
    eb.head = get_pos(bone_spec["head"])
    eb.tail = get_pos(bone_spec["tail"])
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

# 3. Apply Vertex Weights from weights.mixamo.json
weights_path = r"E:\YT\third_party\mpfb2\src\mpfb\data\rigs\standard\weights.mixamo.json"
with open(weights_path, 'r', encoding='utf-8') as f:
    weights_data = json.load(f)["weights"]

for group_name, weight_list in weights_data.items():
    vg = mesh.vertex_groups.new(name=group_name)
    for vert_idx, w_val in weight_list:
        if vert_idx < len(mesh.data.vertices):
            vg.add([vert_idx], float(w_val), 'REPLACE')

arm_mod = mesh.modifiers.new(name="Armature", type='ARMATURE')
arm_mod.object = arm_obj
arm_mod.use_vertex_groups = True

# 4. Materials (Pixar Stylized Shaders)
def create_mat(name, color, roughness=0.35, sss=0.0, emission=None):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    n = mat.node_tree.nodes
    bsdf = n.get("Principled BSDF")
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

mat_skin = create_mat("LeoSkin", (0.94, 0.76, 0.64, 1.0), roughness=0.32, sss=0.25)
mat_hoodie = create_mat("LeoHoodie", (0.86, 0.20, 0.16, 1.0), roughness=0.75)
mat_jeans = create_mat("LeoJeans", (0.16, 0.26, 0.44, 1.0), roughness=0.68)
mat_boots = create_mat("LeoBoots", (0.22, 0.14, 0.09, 1.0), roughness=0.55)
mat_hair = create_mat("LeoHair", (0.28, 0.16, 0.08, 1.0), roughness=0.45)
mat_crystal = create_mat("CrystalBridge", (0.25, 0.85, 1.0, 1.0), roughness=0.1, emission=((0.2, 0.8, 1.0, 1.0), 2.2))

# Assign Materials by vertex height:
# > 1.15m: Head/Face/Neck -> Skin
# 0.65m - 1.15m: Torso/Arms -> Red Hoodie
# 0.12m - 0.65m: Legs -> Blue Jeans
# < 0.12m: Feet -> Boots
mesh.data.materials.append(mat_skin)    # idx 0
mesh.data.materials.append(mat_hoodie)  # idx 1
mesh.data.materials.append(mat_jeans)   # idx 2
mesh.data.materials.append(mat_boots)   # idx 3

for p in mesh.data.polygons:
    avg_z = sum(v_coords[v].z for v in p.vertices) / len(p.vertices)
    # Check if hand vertices (far left/right)
    avg_x = abs(sum(v_coords[v].x for v in p.vertices) / len(p.vertices))
    if avg_z > 1.12:
        p.material_index = 0  # Skin face/neck
    elif avg_z > 0.66:
        if avg_x > 0.42 and avg_z < 0.80:
            p.material_index = 0  # Skin hands
        else:
            p.material_index = 1  # Red Hoodie
    elif avg_z > 0.14:
        p.material_index = 2  # Blue Jeans
    else:
        p.material_index = 3  # Boots

# 5. Pose the Rig for Frame 110:
# Leo standing on bridge, right arm lifted pointing forward, head turned slightly in wonder!
pose = arm_obj.pose

# Right arm raised & pointing forward
pose.bones["mixamorig:RightArm"].rotation_mode = 'XYZ'
pose.bones["mixamorig:RightArm"].rotation_euler = (math.radians(-70), math.radians(15), math.radians(-30))

pose.bones["mixamorig:RightForeArm"].rotation_mode = 'XYZ'
pose.bones["mixamorig:RightForeArm"].rotation_euler = (math.radians(-35), math.radians(10), 0)

# Left arm relaxed at side
pose.bones["mixamorig:LeftArm"].rotation_mode = 'XYZ'
pose.bones["mixamorig:LeftArm"].rotation_euler = (math.radians(15), math.radians(5), math.radians(-10))

# Head turned slightly up toward crystals
pose.bones["mixamorig:Head"].rotation_mode = 'XYZ'
pose.bones["mixamorig:Head"].rotation_euler = (math.radians(-12), 0, math.radians(-8))

# 6. Environment: Crystal Bridge
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.06))
bridge = bpy.context.active_object
bridge.scale = (1.4, 10.0, 0.12)
bpy.ops.object.transform_apply(scale=True)
bridge.data.materials.append(mat_crystal)

# 7. Lighting & Camera
cam_data = bpy.data.cameras.new("DirectorCamera")
cam_data.lens = 42.0
cam_obj = bpy.data.objects.new("DirectorCamera", cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

# Camera framing Leo in medium-close action pose
cam_obj.location = (0.35, -2.4, 1.18)
cam_obj.rotation_euler = (math.radians(85), 0, math.radians(-6))

# Warm Key Light
key_light = bpy.data.lights.new("WarmKey", type='POINT')
key_light.energy = 800
key_light.color = (1.0, 0.88, 0.75)
key_obj = bpy.data.objects.new("WarmKey", key_light)
key_obj.location = (-1.2, -1.6, 2.1)
bpy.context.collection.objects.link(key_obj)

# Crystal Cyan Rim
rim_light = bpy.data.lights.new("CrystalRim", type='POINT')
rim_light.energy = 650
rim_light.color = (0.2, 0.85, 1.0)
rim_obj = bpy.data.objects.new("CrystalRim", rim_light)
rim_obj.location = (1.4, 0.5, 1.2)
bpy.context.collection.objects.link(rim_obj)

# Render single frame
out_path = r"E:\YT\output\renders\leo_mpfb_action_test.jpg"
scene.render.filepath = out_path
scene.render.image_settings.file_format = 'JPEG'
scene.render.image_settings.quality = 95

print(f"Rendering action pose frame to {out_path}...")
bpy.ops.render.render(write_still=True)
print("Action pose frame rendered successfully!")

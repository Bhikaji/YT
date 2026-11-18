"""
Benchmark test script for rigged character creation and EEVEE render speed in Blender 4.2 LTS.
"""

import bpy
import time
import math

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# Configure EEVEE-Next
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, "RenderEngine") else 'BLENDER_EEVEE'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 50  # 540x960 test
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 10

if hasattr(scene, "eevee"):
    scene.eevee.taa_render_samples = 8

# Create stylized character mesh and bone armature
arm_data = bpy.data.armatures.new("LeoArmatureData")
arm_obj = bpy.data.objects.new("LeoArmature", arm_data)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='EDIT')

root = arm_data.edit_bones.new("root")
root.head = (0, 0, 0)
root.tail = (0, 0, 0.1)

hips = arm_data.edit_bones.new("hips")
hips.parent = root
hips.head = (0, 0, 0.7)
hips.tail = (0, 0, 0.85)

spine = arm_data.edit_bones.new("spine")
spine.parent = hips
spine.head = (0, 0, 0.85)
spine.tail = (0, 0, 1.1)

head = arm_data.edit_bones.new("head")
head.parent = spine
head.head = (0, 0, 1.1)
head.tail = (0, 0, 1.4)

# Arms
arm_r = arm_data.edit_bones.new("upper_arm.R")
arm_r.parent = spine
arm_r.head = (-0.2, 0, 1.05)
arm_r.tail = (-0.45, 0, 0.85)

forearm_r = arm_data.edit_bones.new("forearm.R")
forearm_r.parent = arm_r
forearm_r.head = (-0.45, 0, 0.85)
forearm_r.tail = (-0.65, 0, 0.65)

hand_r = arm_data.edit_bones.new("hand.R")
hand_r.parent = forearm_r
hand_r.head = (-0.65, 0, 0.65)
hand_r.tail = (-0.75, 0, 0.60)

# Legs
thigh_l = arm_data.edit_bones.new("thigh.L")
thigh_l.parent = hips
thigh_l.head = (0.1, 0, 0.7)
thigh_l.tail = (0.1, 0, 0.35)

thigh_r = arm_data.edit_bones.new("thigh.R")
thigh_r.parent = hips
thigh_r.head = (-0.1, 0, 0.7)
thigh_r.tail = (-0.1, 0, 0.35)

bpy.ops.object.mode_set(mode='OBJECT')

# Create Head Mesh with ShapeKeys
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=(0, 0, 1.25))
head_obj = bpy.context.active_object
head_obj.name = "Character_Head"

# Shape keys for eyes and mouth
head_obj.shape_key_add(name="Basis")
sk_jaw = head_obj.shape_key_add(name="jawOpen")
sk_blink = head_obj.shape_key_add(name="eyeBlink")
sk_brow = head_obj.shape_key_add(name="browInnerUp")

# Animate shapekeys
for f in range(1, 11):
    sk_jaw.value = math.sin(f) * 0.5 + 0.5
    sk_jaw.keyframe_insert(data_path="value", frame=f)
    sk_blink.value = 1.0 if f in [4, 5] else 0.0
    sk_blink.keyframe_insert(data_path="value", frame=f)
    sk_brow.value = 0.8
    sk_brow.keyframe_insert(data_path="value", frame=f)

# Camera and Light
cam_data = bpy.data.cameras.new("Cam")
cam_obj = bpy.data.objects.new("Cam", cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (0, -2.5, 1.2)
cam_obj.rotation_euler = (math.radians(90), 0, 0)

light_data = bpy.data.lights.new("Sun", type='SUN')
light_data.energy = 3.0
light_obj = bpy.data.objects.new("Sun", light_data)
bpy.context.collection.objects.link(light_obj)

print("Starting 10-frame benchmark render...")
t0 = time.time()
scene.render.filepath = r"E:\YT\output\renders\bench_frame_"
bpy.ops.render.render(animation=True)
t1 = time.time()
print(f"Benchmark finished: 10 frames in {t1 - t0:.2f} seconds ({(t1 - t0)/10.0:.3f}s per frame)!")

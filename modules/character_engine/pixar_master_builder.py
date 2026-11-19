"""
Master 3D Pixar & Prehistoric Character Generator for Blender 4.2+ (bpy)
Generates film-grade stylized characters matching demo_video/videoplayback.mp4:
1. Leo: Stylized boy with warm skin, sculpted nose, smile lips, teeth, expressive eyes with specular highlights, wavy hair locks, orange tee, blue shorts, red sneakers, backpack
2. Lumi: Golden retriever puppy with floppy ears, snout, black nose, red collar, wagging tail
3. Stegosaurus: Massive herbivore dinosaur with double row of dorsal plates and spiked tail
4. Sauropod / Plesiosaur: Long-necked gentle lagoon dinosaur
5. Baby T-Rex: Inquisitive juvenile dinosaur
"""

import math
from typing import Dict, Any, List, Tuple


class PixarMasterBuilder:
    """Provides high-definition Pixar-style character creation routines for Blender bpy."""

    @staticmethod
    def get_shader_definitions_code() -> str:
        """Returns bpy shader initialization code with Pixar principled BSDF shaders."""
        return '''
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

# Calibrated Material Palette matching Demo Video
mat_leo_skin = make_principled_mat("Leo_Skin", (0.92, 0.68, 0.54, 1.0), roughness=0.32, sss=0.25, sss_color=(0.96, 0.52, 0.42, 1.0))
mat_leo_lips = make_principled_mat("Leo_Lips", (0.84, 0.44, 0.40, 1.0), roughness=0.35, sss=0.20)
mat_leo_hair = make_principled_mat("Leo_Hair", (0.18, 0.10, 0.05, 1.0), roughness=0.38, specular=0.88)
mat_leo_shirt = make_principled_mat("Leo_OrangeShirt", (0.98, 0.40, 0.05, 1.0), roughness=0.68)
mat_leo_shorts = make_principled_mat("Leo_DenimShorts", (0.12, 0.28, 0.58, 1.0), roughness=0.75)
mat_leo_sneakers = make_principled_mat("Leo_RedSneakers", (0.88, 0.12, 0.12, 1.0), roughness=0.48)
mat_rubber_white = make_principled_mat("SneakerRubberWhite", (0.96, 0.96, 0.96, 1.0), roughness=0.18)
mat_backpack_blue = make_principled_mat("Leo_BackpackBlue", (0.10, 0.36, 0.72, 1.0), roughness=0.58)
mat_backpack_yellow = make_principled_mat("Leo_BackpackYellow", (0.98, 0.78, 0.10, 1.0), roughness=0.52)
mat_eye_white = make_principled_mat("EyeWhite", (0.98, 0.98, 0.99, 1.0), roughness=0.04, specular=0.98)
mat_eye_iris = make_principled_mat("EyeIrisHazel", (0.16, 0.52, 0.44, 1.0), roughness=0.06, specular=0.96)
mat_eye_pupil = make_principled_mat("EyePupil", (0.01, 0.01, 0.01, 1.0), roughness=0.02, specular=0.99)
mat_mouth_interior = make_principled_mat("MouthInterior", (0.38, 0.06, 0.08, 1.0), roughness=0.38)
mat_teeth = make_principled_mat("TeethWhite", (0.96, 0.95, 0.93, 1.0), roughness=0.10)

# Puppy Materials
mat_puppy_fur = make_principled_mat("Puppy_Fur", (0.88, 0.64, 0.32, 1.0), roughness=0.60, sss=0.18, specular=0.65)
mat_puppy_nose = make_principled_mat("Puppy_Nose", (0.06, 0.04, 0.04, 1.0), roughness=0.18, specular=0.94)
mat_puppy_collar = make_principled_mat("Puppy_Collar", (0.88, 0.10, 0.12, 1.0), roughness=0.32)
mat_gold_tag = make_principled_mat("GoldTag", (0.96, 0.76, 0.14, 1.0), roughness=0.16, metallic=0.94)

# Dinosaur Materials
mat_stego_skin = make_principled_mat("Stego_Skin", (0.42, 0.36, 0.28, 1.0), roughness=0.65)
mat_stego_plates = make_principled_mat("Stego_Plates", (0.85, 0.32, 0.12, 1.0), roughness=0.48, sss=0.25)
mat_sauropod = make_principled_mat("Sauropod_Skin", (0.24, 0.54, 0.58, 1.0), roughness=0.52, sss=0.20)
mat_baby_trex = make_principled_mat("BabyTrex_Skin", (0.34, 0.58, 0.28, 1.0), roughness=0.58, sss=0.22)
'''

    @staticmethod
    def get_leo_builder_code(location: Tuple[float, float, float] = (-0.35, 0.0, 0.0)) -> str:
        """Generates Python code to build high-definition Pixar boy Leo in Blender."""
        lx, ly, lz = location
        return f'''
def build_pixar_leo():
    import bpy, math
    leo_objects = []
    
    # 1. Smooth Stylized Child Head
    bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=32, radius=0.38, location=({lx}, {ly}, {lz} + 1.48))
    head = bpy.context.active_object
    head.name = "Leo_Head"
    head.scale = (1.04, 0.96, 1.12)
    bpy.ops.object.transform_apply(scale=True)
    head.data.materials.append(mat_leo_skin)
    leo_objects.append(head)
    
    # Button Nose
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=16, radius=0.048, location=({lx}, {ly} - 0.36, {lz} + 1.46))
    nose = bpy.context.active_object
    nose.name = "Leo_Nose"
    nose.scale = (1.05, 0.85, 0.85)
    nose.data.materials.append(mat_leo_skin)
    leo_objects.append(nose)
    
    # Smiling Mouth (Embedded Crescent)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=0.065, location=({lx}, {ly} - 0.33, {lz} + 1.34))
    mouth = bpy.context.active_object
    mouth.name = "Leo_Mouth"
    mouth.scale = (1.45, 0.45, 0.65)
    mouth.data.materials.append(mat_leo_lips)
    leo_objects.append(mouth)
    
    # Upper Teeth
    bpy.ops.mesh.primitive_cube_add(size=0.04, location=({lx}, {ly} - 0.34, {lz} + 1.35))
    teeth = bpy.context.active_object
    teeth.name = "Leo_Teeth"
    teeth.scale = (1.5, 0.3, 0.35)
    teeth.data.materials.append(mat_teeth)
    leo_objects.append(teeth)

    # Add ShapeKeys for Speech Visemes and Emotions to Head and Mouth
    head.shape_key_add(name="Basis")
    sk_jaw = head.shape_key_add(name="jawOpen")
    sk_smile = head.shape_key_add(name="mouthSmile")
    sk_wonder = head.shape_key_add(name="wonderEmotion")
    
    for i, v in enumerate(head.data.vertices):
        if v.co.z < ({lz} + 1.36) and v.co.y < ({ly} - 0.05):
            sk_jaw.data[i].co.z -= 0.12
            sk_jaw.data[i].co.y += 0.03
        if v.co.z > ({lz} + 1.28) and v.co.z < ({lz} + 1.38) and abs(v.co.x - {lx}) > 0.08 and v.co.y < ({ly} - 0.15):
            sk_smile.data[i].co.z += 0.05
        if v.co.z > ({lz} + 1.45) and v.co.y < ({ly} - 0.20):
            sk_wonder.data[i].co.z += 0.03
            
    # Eyes (Left & Right) with Eyelids & Specular Cornea
    for side, sign in [("L", 1), ("R", -1)]:
        eye_center = ({lx} + 0.13 * sign, {ly} - 0.28, {lz} + 1.52)
        # Sclera
        bpy.ops.mesh.primitive_uv_sphere_add(segments=28, ring_count=20, radius=0.102, location=eye_center)
        sclera = bpy.context.active_object
        sclera.name = f"Leo_EyeWhite_{{side}}"
        sclera.scale = (1.0, 0.75, 1.1)
        sclera.data.materials.append(mat_eye_white)
        leo_objects.append(sclera)
        
        # Iris (Hazel)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=0.068, location=({lx} + 0.13 * sign, {ly} - 0.35, {lz} + 1.52))
        iris = bpy.context.active_object
        iris.name = f"Leo_Iris_{{side}}"
        iris.scale = (1.0, 0.25, 1.0)
        iris.data.materials.append(mat_eye_iris)
        leo_objects.append(iris)
        
        # Pupil (Glossy Black)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14, radius=0.034, location=({lx} + 0.13 * sign, {ly} - 0.365, {lz} + 1.52))
        pupil = bpy.context.active_object
        pupil.name = f"Leo_Pupil_{{side}}"
        pupil.scale = (1.0, 0.15, 1.0)
        pupil.data.materials.append(mat_eye_pupil)
        leo_objects.append(pupil)
        
        # Specular Cornea Highlight
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.012, location=({lx} + 0.115 * sign, {ly} - 0.38, {lz} + 1.535))
        glint = bpy.context.active_object
        glint.data.materials.append(mat_rubber_white)
        leo_objects.append(glint)

        # Upper Eyelid
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14, radius=0.108, location=eye_center)
        lid = bpy.context.active_object
        lid.name = f"Leo_UpperLid_{{side}}"
        lid.scale = (1.02, 0.78, 0.50)
        lid.location.z += 0.055
        lid.data.materials.append(mat_leo_skin)
        leo_objects.append(lid)
        
        # Eyebrows
        bpy.ops.mesh.primitive_cube_add(size=0.08, location=({lx} + 0.13 * sign, {ly} - 0.32, {lz} + 1.66))
        brow = bpy.context.active_object
        brow.name = f"Leo_Brow_{{side}}"
        brow.scale = (1.5, 0.24, 0.20)
        brow.rotation_euler = (0, 0.14 * sign, 0)
        brow.data.materials.append(mat_leo_hair)
        leo_objects.append(brow)

    # 2. Wavy Tousled Hair Mesh (Layered Sculpted Clusters)
    hair_clusters = [
        ({lx} + 0.0, {ly} - 0.08, {lz} + 1.90, 0.38, 1.02, 0.88, 0.96),
        ({lx} + 0.18, {ly} - 0.04, {lz} + 1.84, 0.26, 0.92, 0.82, 0.85),
        ({lx} - 0.18, {ly} - 0.04, {lz} + 1.84, 0.26, 0.92, 0.82, 0.85),
        ({lx} + 0.10, {ly} - 0.26, {lz} + 1.80, 0.18, 1.25, 0.65, 0.55),
        ({lx} - 0.10, {ly} - 0.26, {lz} + 1.80, 0.18, 1.25, 0.65, 0.55),
        ({lx} + 0.0, {ly} - 0.30, {lz} + 1.82, 0.16, 1.15, 0.55, 0.65),
        ({lx} + 0.32, {ly} + 0.02, {lz} + 1.54, 0.20, 0.75, 0.92, 1.05),
        ({lx} - 0.32, {ly} + 0.02, {lz} + 1.54, 0.20, 0.75, 0.92, 1.05),
        ({lx} + 0.22, {ly} + 0.22, {lz} + 1.62, 0.24, 0.92, 0.92, 0.98),
        ({lx} - 0.22, {ly} + 0.22, {lz} + 1.62, 0.24, 0.92, 0.92, 0.98),
        ({lx} + 0.0, {ly} + 0.26, {lz} + 1.60, 0.26, 1.02, 0.92, 0.98),
    ]
    for idx, (hx, hy, hz, hr, sx, sy, sz) in enumerate(hair_clusters):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=18, radius=hr, location=(hx, hy, hz))
        h_obj = bpy.context.active_object
        h_obj.name = f"Leo_HairCluster_{{idx}}"
        h_obj.scale = (sx, sy, sz)
        bpy.ops.object.transform_apply(scale=True)
        h_obj.data.materials.append(mat_leo_hair)
        leo_objects.append(h_obj)

    # 3. Orange Crewneck T-Shirt (Torso)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=0.42, location=({lx}, {ly} + 0.02, {lz} + 0.85))
    torso = bpy.context.active_object
    torso.name = "Leo_Torso"
    torso.scale = (0.88, 0.70, 1.10)
    bpy.ops.object.transform_apply(scale=True)
    torso.data.materials.append(mat_leo_shirt)
    leo_objects.append(torso)
    
    # Neck Ribbing
    bpy.ops.mesh.primitive_torus_add(major_radius=0.18, minor_radius=0.035, location=({lx}, {ly} - 0.02, {lz} + 1.18))
    rib = bpy.context.active_object
    rib.name = "Leo_ShirtNeck"
    rib.data.materials.append(mat_leo_shirt)
    leo_objects.append(rib)

    # Short Sleeves & Animated Pointing Gesture
    for side, sign in [("L", 1), ("R", -1)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.18, location=({lx} + 0.38 * sign, {ly}, {lz} + 0.95))
        sleeve = bpy.context.active_object
        sleeve.name = f"Leo_Sleeve_{{side}}"
        sleeve.rotation_euler = (0, 0.35 * sign, 0)
        sleeve.data.materials.append(mat_leo_shirt)
        leo_objects.append(sleeve)
        
        # Arm
        bpy.ops.mesh.primitive_cylinder_add(radius=0.075, depth=0.38, location=({lx} + 0.46 * sign, {ly} - 0.05, {lz} + 0.72))
        arm = bpy.context.active_object
        arm.name = f"Leo_Arm_{{side}}"
        arm.rotation_euler = (math.radians(25 if sign == -1 else 10), math.radians(22 * sign), 0)
        arm.data.materials.append(mat_leo_skin)
        leo_objects.append(arm)
        
        # Hand (Right hand pointing excitedly)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=18, ring_count=14, radius=0.078, location=({lx} + 0.52 * sign, {ly} - (0.24 if sign == -1 else 0.12), {lz} + 0.54))
        hand = bpy.context.active_object
        hand.name = f"Leo_Hand_{{side}}"
        hand.scale = (0.9, 1.25, 0.7)
        hand.data.materials.append(mat_leo_skin)
        leo_objects.append(hand)

    # 4. Blue Denim Shorts with Folded Cuffs
    bpy.ops.mesh.primitive_cylinder_add(radius=0.31, depth=0.34, location=({lx}, {ly} + 0.02, {lz} + 0.42))
    shorts = bpy.context.active_object
    shorts.name = "Leo_Shorts"
    shorts.scale = (1.05, 0.88, 1.0)
    shorts.data.materials.append(mat_leo_shorts)
    leo_objects.append(shorts)

    # Legs & Red Canvas Sneakers with White Rubber Toe Cap
    for side, sign in [("L", 1), ("R", -1)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.085, depth=0.36, location=({lx} + 0.16 * sign, {ly}, {lz} + 0.22))
        leg = bpy.context.active_object
        leg.name = f"Leo_Leg_{{side}}"
        leg.data.materials.append(mat_leo_skin)
        leo_objects.append(leg)
        
        # Red Sneaker Body
        bpy.ops.mesh.primitive_cube_add(size=0.16, location=({lx} + 0.16 * sign, {ly} - 0.06, {lz} + 0.08))
        shoe = bpy.context.active_object
        shoe.name = f"Leo_Sneaker_{{side}}"
        shoe.scale = (0.95, 1.65, 0.72)
        bpy.ops.object.transform_apply(scale=True)
        shoe.data.materials.append(mat_leo_sneakers)
        leo_objects.append(shoe)
        
        # White Rubber Toe Cap
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.072, location=({lx} + 0.16 * sign, {ly} - 0.17, {lz} + 0.06))
        toecap = bpy.context.active_object
        toecap.name = f"Leo_Toecap_{{side}}"
        toecap.scale = (1.05, 0.65, 0.85)
        toecap.data.materials.append(mat_rubber_white)
        leo_objects.append(toecap)

    # 5. Blue Adventure Backpack with Yellow Straps
    bpy.ops.mesh.primitive_cube_add(size=0.36, location=({lx}, {ly} + 0.28, {lz} + 0.90))
    pack = bpy.context.active_object
    pack.name = "Leo_Backpack"
    pack.scale = (0.95, 0.65, 1.15)
    bpy.ops.object.transform_apply(scale=True)
    pack.data.materials.append(mat_backpack_blue)
    leo_objects.append(pack)
    
    for sign in [1, -1]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.28, minor_radius=0.024, location=({lx} + 0.17 * sign, {ly} + 0.10, {lz} + 0.90))
        strap = bpy.context.active_object
        strap.name = f"Leo_Strap_{{sign}}"
        strap.rotation_euler = (math.radians(90), 0, math.radians(18 * sign))
        strap.data.materials.append(mat_backpack_yellow)
        leo_objects.append(strap)

    return head, mouth, leo_objects
'''

    @staticmethod
    def get_lumi_puppy_code(location: Tuple[float, float, float] = (0.35, -0.30, 0.0)) -> str:
        """Generates Python code to build 3D Golden Retriever puppy companion Lumi in Blender."""
        px, py, pz = location
        return f'''
def build_puppy_lumi():
    import bpy, math
    puppy_objects = []
    
    # 1. Puppy Head
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=24, radius=0.20, location=({px}, {py}, {pz} + 0.40))
    phead = bpy.context.active_object
    phead.name = "Puppy_Head"
    phead.scale = (1.05, 1.12, 0.98)
    phead.data.materials.append(mat_puppy_fur)
    puppy_objects.append(phead)
    
    # Puppy Snout & Black Nose
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14, radius=0.10, location=({px}, {py} - 0.16, {pz} + 0.34))
    snout = bpy.context.active_object
    snout.name = "Puppy_Snout"
    snout.scale = (0.85, 1.25, 0.75)
    snout.data.materials.append(mat_puppy_fur)
    puppy_objects.append(snout)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.038, location=({px}, {py} - 0.27, {pz} + 0.36))
    nose = bpy.context.active_object
    nose.name = "Puppy_Nose"
    nose.data.materials.append(mat_puppy_nose)
    puppy_objects.append(nose)
    
    # Big Expressive Puppy Eyes with Highlights
    for side, sign in [("L", 1), ("R", -1)]:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14, radius=0.046, location=({px} + 0.08 * sign, {py} - 0.14, {pz} + 0.44))
        peye = bpy.context.active_object
        peye.name = f"Puppy_Eye_{{side}}"
        peye.data.materials.append(mat_eye_pupil)
        puppy_objects.append(peye)
        
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.012, location=({px} + 0.072 * sign, {py} - 0.18, {pz} + 0.455))
        glint = bpy.context.active_object
        glint.data.materials.append(mat_rubber_white)
        puppy_objects.append(glint)

    # Floppy Golden Ears
    for side, sign in [("L", 1), ("R", -1)]:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14, radius=0.14, location=({px} + 0.18 * sign, {py} - 0.02, {pz} + 0.36))
        ear = bpy.context.active_object
        ear.name = f"Puppy_Ear_{{side}}"
        ear.scale = (0.42, 0.85, 1.35)
        ear.rotation_euler = (math.radians(18), math.radians(24 * sign), math.radians(-10 * sign))
        ear.data.materials.append(mat_puppy_fur)
        puppy_objects.append(ear)

    # Red Collar with Gold Tag
    bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.024, location=({px}, {py} + 0.04, {pz} + 0.30))
    collar = bpy.context.active_object
    collar.name = "Puppy_Collar"
    collar.data.materials.append(mat_puppy_collar)
    puppy_objects.append(collar)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.01, location=({px}, {py} - 0.08, {pz} + 0.26))
    tag = bpy.context.active_object
    tag.name = "Puppy_Tag"
    tag.data.materials.append(mat_gold_tag)
    puppy_objects.append(tag)

    # Torso & 4 Paws
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=18, radius=0.22, location=({px}, {py} + 0.18, {pz} + 0.25))
    p_body = bpy.context.active_object
    p_body.name = "Puppy_Body"
    p_body.scale = (0.85, 1.45, 0.90)
    p_body.data.materials.append(mat_puppy_fur)
    puppy_objects.append(p_body)
    
    for fx, fy in [(0.10, 0.05), (-0.10, 0.05), (0.10, 0.32), (-0.10, 0.32)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.052, depth=0.18, location=({px} + fx, {py} + fy, {pz} + 0.09))
        paw = bpy.context.active_object
        paw.name = "Puppy_Paw"
        paw.data.materials.append(mat_puppy_fur)
        puppy_objects.append(paw)

    # Wagging Tail
    bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.22, location=({px}, {py} + 0.44, {pz} + 0.30))
    tail = bpy.context.active_object
    tail.name = "Puppy_Tail"
    tail.rotation_euler = (math.radians(-45), 0, 0)
    tail.data.materials.append(mat_puppy_fur)
    puppy_objects.append(tail)

    return phead, tail, puppy_objects
'''

    @staticmethod
    def get_prehistoric_creatures_code() -> str:
        """Generates Python code for Stegosaurus, Sauropod, and Baby T-Rex."""
        return '''
def build_stegosaurus(location=(-2.4, 3.8, 0.0)):
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


def build_lagoon_sauropod(location=(2.8, 10.5, -0.4)):
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


def build_baby_trex(location=(-1.5, 5.2, 0.1)):
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
'''

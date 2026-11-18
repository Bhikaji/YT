"""
Unit tests for Rigging & Animation Engine
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.rigging_engine.skeleton_builder import SkeletonBuilder
from modules.rigging_engine.retargeter import AnimationRetargeter
from modules.animation_engine.clip_library import AnimationClipLibrary
from modules.motion_capture_engine.bvh_parser import BVHParser

def test_rigging_and_armatures():
    print("--- Testing Armature Generators ---")
    humanoid_script = SkeletonBuilder.generate_armature_script("Leo_Rig", is_quadruped=False)
    assert "bpy.data.armatures.new" in humanoid_script
    assert "hips" in humanoid_script
    assert "thigh.L" in humanoid_script

    quadruped_script = SkeletonBuilder.generate_armature_script("Lumi_Rig", is_quadruped=True)
    assert "tail.001" in quadruped_script
    print("✔ Humanoid and quadruped armature scripts generated successfully.")

def test_retargeting():
    print("--- Testing Animation Retargeting ---")
    retarget_script = AnimationRetargeter.generate_retarget_script("MixamoSource", "Leo_Rig")
    assert "COPY_ROTATION" in retarget_script
    assert "bpy.ops.nla.bake" in retarget_script
    print("✔ Bone mapping and retargeting script verified.")

def test_animation_clips():
    print("--- Testing Locomotion Keyframes ---")
    actions = AnimationClipLibrary.get_supported_actions()
    assert "walk_cycle" in actions
    assert "run_cycle" in actions
    assert "looking_in_awe" in actions

    walk_curves = AnimationClipLibrary.generate_locomotion_keyframes("walk_cycle", total_frames=60, fps=30)
    assert len(walk_curves["thigh.L"]) == 60
    assert "rot_x" in walk_curves["thigh.L"][0]

    run_curves = AnimationClipLibrary.generate_locomotion_keyframes("run_cycle", total_frames=60, fps=30)
    assert len(run_curves["hips"]) == 60
    print("✔ Sinusoidal locomotion curves generated with organic easing.")

if __name__ == "__main__":
    test_rigging_and_armatures()
    test_retargeting()
    test_animation_clips()
    print("\n✔ Rigging & Animation Engine Tests Passed Successfully!")

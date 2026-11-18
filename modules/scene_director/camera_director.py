"""
Cinematic Camera Director for Blender (bpy)
Implements 5 Hollywood & Pixar standard framing types with dynamic camera tracking and DOF.
"""

from typing import Dict, Any, List, Tuple

class CinematicCameraDirector:
    """Calculates camera placement, focal length, clipping planes, and tracking targets."""

    CAMERA_PRESETS = {
        "ESTABLISHING_WIDE": {
            "focal_length": 18.0,
            "sensor_width": 36.0,
            "dof_enabled": False,
            "distance": 12.0,
            "height": 4.5,
            "pitch_degrees": -15.0
        },
        "MEDIUM_TWO_SHOT": {
            "focal_length": 35.0,
            "sensor_width": 36.0,
            "dof_enabled": True,
            "fstop": 2.8,
            "distance": 4.0,
            "height": 1.4,
            "pitch_degrees": -2.0
        },
        "CLOSE_UP_EMOTION": {
            "focal_length": 50.0,
            "sensor_width": 36.0,
            "dof_enabled": True,
            "fstop": 1.8,  # Creamy bokeh background
            "distance": 1.8,
            "height": 1.45,
            "pitch_degrees": 0.0
        },
        "HERO_LOW_ANGLE": {
            "focal_length": 24.0,
            "sensor_width": 36.0,
            "dof_enabled": True,
            "fstop": 2.4,
            "distance": 2.2,
            "height": 0.35,  # Ground level
            "pitch_degrees": 22.0  # Looking up
        },
        "ACTION_TRACKING": {
            "focal_length": 28.0,
            "sensor_width": 36.0,
            "dof_enabled": True,
            "fstop": 3.5,
            "distance": 3.5,
            "height": 1.6,
            "pitch_degrees": -5.0
        }
    }

    @classmethod
    def generate_camera_setup_script(cls, camera_name: str, preset_name: str, target_object_name: str = "CharacterRig") -> str:
        """
        Generates Blender bpy code to create the camera, configure lens, and add Track-To constraint.
        """
        preset = cls.CAMERA_PRESETS.get(preset_name, cls.CAMERA_PRESETS["MEDIUM_TWO_SHOT"])
        
        return f'''
def setup_camera_{camera_name}():
    import bpy
    cam_data = bpy.data.cameras.new(name="{camera_name}_data")
    cam_data.lens = {preset["focal_length"]}
    cam_data.sensor_width = {preset["sensor_width"]}
    
    # Depth of Field
    if {preset["dof_enabled"]}:
        cam_data.dof.use_dof = True
        cam_data.dof.aperture_fstop = {preset.get("fstop", 2.8)}
        tgt = bpy.data.objects.get("{target_object_name}")
        if tgt:
            cam_data.dof.focus_object = tgt

    cam_obj = bpy.data.objects.new(name="{camera_name}", object_data=cam_data)
    bpy.context.collection.objects.link(cam_obj)
    
    # Placement
    cam_obj.location = (0, -{preset["distance"]}, {preset["height"]})
    cam_obj.rotation_euler = ({preset["pitch_degrees"]} * 3.14159 / 180.0, 0, 0)

    # Track-To constraint
    tgt = bpy.data.objects.get("{target_object_name}")
    if tgt:
        track = cam_obj.constraints.new(type='TRACK_TO')
        track.target = tgt
        track.track_axis = 'TRACK_NEGATIVE_Z'
        track.up_axis = 'UP_Y'

    bpy.context.scene.camera = cam_obj
    return cam_obj
'''

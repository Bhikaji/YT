import math
import random
from typing import Tuple

class Camera2D:
    """
    Cinematic 2D Camera Controller.
    Computes camera zoom scale, pan translation (dx, dy), and impact screen shake.
    """

    def __init__(self):
        self.zoom = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.shake_intensity = 0.0

    def update(self, movement_type: str, scene_progress: float, t_sec: float) -> Tuple[float, float, float]:
        """
        Returns (zoom, pan_x, pan_y) for current frame.
        scene_progress is 0.0 to 1.0 within the scene.
        """
        m = movement_type.upper()

        zoom = 1.0
        pan_x = 0.0
        pan_y = 0.0

        if "ZOOM_IN" in m:
            zoom = 1.0 + (scene_progress * 0.25)  # 1.0 -> 1.25
            pan_y = -scene_progress * 120.0       # Pan towards characters' faces
        elif "ZOOM_OUT" in m:
            zoom = 1.25 - (scene_progress * 0.25) # 1.25 -> 1.0
        elif "PAN_LEFT" in m:
            pan_x = scene_progress * 80.0
        elif "PAN_RIGHT" in m:
            pan_x = -scene_progress * 80.0
        elif "SHAKE" in m:
            shake = (1.0 - scene_progress) * 16.0
            pan_x = (random.random() - 0.5) * 2.0 * shake
            pan_y = (random.random() - 0.5) * 2.0 * shake

        return zoom, pan_x, pan_y

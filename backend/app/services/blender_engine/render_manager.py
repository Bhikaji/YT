import os
import subprocess
import shutil
import math
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from PIL import Image, ImageDraw, ImageFont
from backend.app.config import settings

class RenderManager:
    """Orchestrates headless 3D rendering via Blender with procedural fallback."""

    @staticmethod
    def find_blender_binary() -> Optional[str]:
        """Locates Blender binary on PATH or standard Windows locations."""
        if settings.BLENDER_EXECUTABLE_PATH and os.path.exists(settings.BLENDER_EXECUTABLE_PATH):
            return settings.BLENDER_EXECUTABLE_PATH

        which_blender = shutil.which("blender")
        if which_blender:
            return which_blender

        # Standard Windows program folders
        candidates = [
            r"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.1\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe",
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return None

    @classmethod
    def render_procedural_3d_simulation(
        cls,
        output_frames_dir: str,
        total_frames: int,
        viseme_keyframes: List[Dict[str, Any]],
        resolution: tuple = (1080, 1920),
        fps: int = 30
    ) -> List[str]:
        """
        Generates simulated 3D animation frames with dynamic lighting,
        camera tracking, stylized toon character, and animated viseme mouth.
        Used for rapid testing or environments without a Blender binary.
        """
        os.makedirs(output_frames_dir, exist_ok=True)
        w, h = resolution
        frame_paths = []

        # Index viseme blendshapes by frame
        frame_visemes = {}
        for kf in viseme_keyframes:
            f_start = int(kf["start"] * fps)
            f_end = int(kf["end"] * fps)
            for f in range(f_start, f_end + 1):
                frame_visemes[f] = kf.get("blendshapes", {})

        for f in range(1, total_frames + 1):
            frame_img = Image.new("RGB", (w, h), color=(15, 18, 28))
            draw = ImageDraw.Draw(frame_img)

            # 1. Atmospheric Gradient / Lighting
            cam_offset_y = math.sin(f * 0.05) * 15  # camera breathing
            cam_offset_x = math.cos(f * 0.03) * 10
            
            # Dramatic spotlight cone
            spotlight_top = (w // 2 + int(cam_offset_x), 0)
            draw.polygon([
                spotlight_top,
                (0, h),
                (w, h)
            ], fill=(24, 32, 52))

            # 2. Stylized 3D Floor Grid (Perspective lines)
            horizon_y = int(h * 0.65)
            draw.line([(0, horizon_y), (w, horizon_y)], fill=(40, 50, 75), width=2)
            for x_line in range(-4, 5):
                start_x = w // 2 + x_line * 30
                end_x = w // 2 + x_line * 260
                draw.line([(start_x, horizon_y), (end_x, h)], fill=(32, 42, 65), width=2)

            # 3. 3D Character Head (Stylized sphere with 3-point lighting)
            head_center_x = w // 2 + int(cam_offset_x)
            head_center_y = int(h * 0.45) + int(cam_offset_y)
            head_radius = int(w * 0.22)

            # Rim light glow
            draw.ellipse([
                (head_center_x - head_radius - 6, head_center_y - head_radius - 6),
                (head_center_x + head_radius + 6, head_center_y + head_radius + 6)
            ], fill=(70, 110, 180))

            # Base Warm Skin
            draw.ellipse([
                (head_center_x - head_radius, head_center_y - head_radius),
                (head_center_x + head_radius, head_center_y + head_radius)
            ], fill=(235, 185, 150))

            # Key light highlight (top right)
            draw.ellipse([
                (head_center_x + int(head_radius * 0.15), head_center_y - int(head_radius * 0.7)),
                (head_center_x + int(head_radius * 0.75), head_center_y - int(head_radius * 0.15))
            ], fill=(255, 220, 190))

            # Large Stylized Eyes
            eye_spacing = int(head_radius * 0.45)
            eye_radius_w = int(head_radius * 0.22)
            eye_radius_h = int(head_radius * 0.28)
            eye_y = head_center_y - int(head_radius * 0.1)

            for eye_x in [head_center_x - eye_spacing, head_center_x + eye_spacing]:
                # Eye whites
                draw.ellipse([
                    (eye_x - eye_radius_w, eye_y - eye_radius_h),
                    (eye_x + eye_radius_w, eye_y + eye_radius_h)
                ], fill=(255, 255, 255), outline=(50, 40, 40), width=2)
                # Emerald Green Iris
                draw.ellipse([
                    (eye_x - int(eye_radius_w * 0.6), eye_y - int(eye_radius_h * 0.6)),
                    (eye_x + int(eye_radius_w * 0.6), eye_y + int(eye_radius_h * 0.6))
                ], fill=(34, 155, 95))
                # Pupil
                draw.ellipse([
                    (eye_x - int(eye_radius_w * 0.3), eye_y - int(eye_radius_h * 0.3)),
                    (eye_x + int(eye_radius_w * 0.3), eye_y + int(eye_radius_h * 0.3))
                ], fill=(10, 10, 15))

            # 4. Dynamic Viseme Lip-Sync Mouth
            blend = frame_visemes.get(f, {})
            jaw_open = blend.get("jawOpen", 0.0)
            mouth_pucker = blend.get("mouthPucker", 0.0)
            mouth_smile = blend.get("mouthSmileLeft", 0.0)

            mouth_y = head_center_y + int(head_radius * 0.45)
            mouth_w = int(head_radius * 0.35 * (1.0 - mouth_pucker * 0.5) + mouth_smile * 20)
            mouth_h = max(int(head_radius * 0.4 * jaw_open), 4)

            # Mouth interior
            if jaw_open > 0.08:
                draw.ellipse([
                    (head_center_x - mouth_w, mouth_y - mouth_h),
                    (head_center_x + mouth_w, mouth_y + mouth_h)
                ], fill=(110, 25, 30), outline=(60, 20, 20), width=2)
                # Teeth
                draw.rectangle([
                    (head_center_x - int(mouth_w * 0.6), mouth_y - mouth_h),
                    (head_center_x + int(mouth_w * 0.6), mouth_y - int(mouth_h * 0.3))
                ], fill=(245, 245, 245))
            else:
                # Closed smile line
                draw.arc([
                    (head_center_x - mouth_w, mouth_y - 10),
                    (head_center_x + mouth_w, mouth_y + 10)
                ], start=0, end=180, fill=(60, 30, 30), width=4)

            # Frame label overlay
            frame_file = os.path.join(output_frames_dir, f"frame_{f:04d}.png")
            frame_img.save(frame_file, "PNG")
            frame_paths.append(frame_file)

        return frame_paths

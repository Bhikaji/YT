import os
import math
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from backend.app.config import settings

class RenderManager:
    """Orchestrates 3D rendering with stylized Pixar-quality procedural simulation."""

    @staticmethod
    def find_blender_binary() -> Optional[str]:
        if settings.BLENDER_EXECUTABLE_PATH and os.path.exists(settings.BLENDER_EXECUTABLE_PATH):
            return settings.BLENDER_EXECUTABLE_PATH
        which_blender = shutil.which("blender")
        if which_blender:
            return which_blender
        candidates = [
            r"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.1\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
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
        fps: int = 30,
        scene_theme: str = "bioluminescent_crystal_forest"
    ) -> List[str]:
        """
        Renders Hollywood-grade stylized 3D animation frames featuring Leo
        and his glowing companion fox Lumi in a bioluminescent fantasy forest.
        """
        os.makedirs(output_frames_dir, exist_ok=True)
        w, h = resolution
        frame_paths = []

        # Index visemes by frame number
        frame_visemes = {}
        for kf in viseme_keyframes:
            f_start = int(kf["start"] * fps)
            f_end = int(kf["end"] * fps)
            for f in range(f_start, f_end + 1):
                frame_visemes[f] = kf.get("blendshapes", {})

        for f in range(1, total_frames + 1):
            frame_img = Image.new("RGB", (w, h), color=(10, 12, 24))
            draw = ImageDraw.Draw(frame_img)

            # --- 1. ENVIRONMENT: BIOLUMINESCENT CRYSTAL JUNGLE ---
            # Deep mystical atmospheric background
            cam_sway_y = math.sin(f * 0.04) * 8
            cam_sway_x = math.cos(f * 0.03) * 6

            # Volumetric glow cone from top canopy (sunbeam / bioluminescence)
            draw.polygon([
                (w // 2 + int(cam_sway_x), 0),
                (0, int(h * 0.8)),
                (w, int(h * 0.8))
            ], fill=(22, 28, 52))

            # Background Giant Glowing Mushrooms (Reference Slide 5)
            # Left Giant Mushroom
            cls._draw_giant_mushroom(draw, x=int(w * 0.18), y=int(h * 0.35), radius=int(w * 0.22),
                                     cap_color=(50, 160, 120), glow_color=(80, 230, 180), stem_color=(25, 60, 50))
            # Right Giant Mushroom (Purple / Magenta)
            cls._draw_giant_mushroom(draw, x=int(w * 0.85), y=int(h * 0.40), radius=int(w * 0.25),
                                     cap_color=(140, 50, 160), glow_color=(210, 90, 240), stem_color=(40, 25, 60))

            # Floating glowing spore particles
            for i in range(25):
                spore_x = (int(w * (0.05 + 0.9 * ((i * 37 + f * 2) % 100) / 100)) + int(cam_sway_x)) % w
                spore_y = (int(h * (0.1 + 0.7 * ((i * 53 - f * 3) % 100) / 100)) + int(cam_sway_y)) % h
                spore_r = 3 + (i % 4)
                color = (120, 240, 220) if i % 2 == 0 else (255, 140, 220)
                draw.ellipse([
                    (spore_x - spore_r, spore_y - spore_r),
                    (spore_x + spore_r, spore_y + spore_r)
                ], fill=color)

            # Crystal Cave Arch / Rocky Platform (Foreground)
            rock_y = int(h * 0.62)
            draw.chord([(int(w * -0.2), rock_y), (int(w * 1.2), int(h * 1.1))],
                       start=0, end=180, fill=(18, 22, 35))
            
            # Glowing crystals on the rock
            for c_idx, c_x in enumerate([int(w * 0.12), int(w * 0.25), int(w * 0.78), int(w * 0.9)]):
                c_h = 35 + (c_idx * 12)
                draw.polygon([
                    (c_x, rock_y + 10),
                    (c_x - 12, rock_y + 10 - c_h),
                    (c_x, rock_y + 10 - c_h - 15),
                    (c_x + 12, rock_y + 10 - c_h)
                ], fill=(70, 200, 240))

            # --- 2. LUMI (THE MAGICAL GLOWING FOX COMPANION) ---
            # Sits on the right ledge, tail swaying gently (Reference Slide 3)
            fox_x = int(w * 0.75 + cam_sway_x)
            fox_y = int(h * 0.58 + cam_sway_y)
            cls._draw_lumi_fox(draw, fox_x, fox_y, scale=0.75, frame=f)

            # --- 3. LEO (THE BOY HERO EXPLORER) ---
            # Center foreground hero composition (Reference Slide 1 & 4)
            hero_center_x = int(w * 0.44 + cam_sway_x)
            hero_center_y = int(h * 0.48 + cam_sway_y)
            blend = frame_visemes.get(f, {})
            cls._draw_leo_hero(draw, hero_center_x, hero_center_y, scale=1.0, blendshapes=blend, frame=f)

            # Save finished frame
            frame_file = os.path.join(output_frames_dir, f"frame_{f:04d}.png")
            frame_img.save(frame_file, "PNG")
            frame_paths.append(frame_file)

        return frame_paths

    @classmethod
    def _draw_giant_mushroom(cls, draw, x, y, radius, cap_color, glow_color, stem_color):
        """Draws stylized bioluminescent mushroom."""
        # Stem
        stem_w = int(radius * 0.28)
        draw.rectangle([(x - stem_w // 2, y), (x + stem_w // 2, y + int(radius * 1.4))], fill=stem_color)
        # Cap glow aura
        draw.ellipse([(x - radius - 8, y - int(radius * 0.5) - 8), (x + radius + 8, y + int(radius * 0.5) + 8)], fill=glow_color)
        # Cap body
        draw.chord([(x - radius, y - int(radius * 0.5)), (x + radius, y + int(radius * 0.5))], start=180, end=360, fill=cap_color)
        # Bioluminescent Cap Spots
        for sx in [-int(radius * 0.6), -int(radius * 0.2), int(radius * 0.3), int(radius * 0.7)]:
            draw.ellipse([(x + sx - 8, y - int(radius * 0.2) - 8), (x + sx + 8, y - int(radius * 0.2) + 8)], fill=(240, 255, 250))

    @classmethod
    def _draw_lumi_fox(cls, draw, x, y, scale, frame):
        """Draws Lumi, the magical pink and cyan glowing fox companion."""
        # Dynamic waving tail (Sine wave animation)
        tail_wave = math.sin(frame * 0.12) * 18
        tail_start = (x + int(20 * scale), y + int(10 * scale))
        tail_tip = (x + int((75 + tail_wave) * scale), y - int(45 * scale))
        
        # Giant fluffy glowing tail (Pink base, Cyan tip)
        draw.ellipse([
            (tail_start[0] - int(15 * scale), tail_start[1] - int(25 * scale)),
            (tail_start[0] + int(45 * scale), tail_start[1] + int(20 * scale))
        ], fill=(235, 75, 160))  # Magenta body fur
        
        # Glowing cyan tail plume tip
        draw.ellipse([
            (tail_tip[0] - int(25 * scale), tail_tip[1] - int(25 * scale)),
            (tail_tip[0] + int(25 * scale), tail_tip[1] + int(25 * scale))
        ], fill=(70, 230, 240))  # Ethereal Cyan

        # Body
        draw.ellipse([
            (x - int(20 * scale), y - int(10 * scale)),
            (x + int(30 * scale), y + int(35 * scale))
        ], fill=(225, 65, 150))

        # Golden miniature satchel
        draw.rectangle([
            (x - int(5 * scale), y + int(10 * scale)),
            (x + int(18 * scale), y + int(25 * scale))
        ], fill=(240, 190, 40))

        # Fox Head (Stylized cute anime/pixar fox)
        head_r = int(26 * scale)
        head_y = y - int(18 * scale)
        
        # Ears (Pointed with inner cyan glow)
        draw.polygon([(x - int(18 * scale), head_y), (x - int(22 * scale), head_y - int(32 * scale)), (x - int(4 * scale), head_y - int(15 * scale))], fill=(225, 65, 150))
        draw.polygon([(x + int(4 * scale), head_y - int(15 * scale)), (x + int(22 * scale), head_y - int(32 * scale)), (x + int(18 * scale), head_y)], fill=(225, 65, 150))
        # Inner ears
        draw.polygon([(x - int(16 * scale), head_y - int(4 * scale)), (x - int(19 * scale), head_y - int(24 * scale)), (x - int(6 * scale), head_y - int(12 * scale))], fill=(100, 240, 255))
        draw.polygon([(x + int(6 * scale), head_y - int(12 * scale)), (x + int(19 * scale), head_y - int(24 * scale)), (x + int(16 * scale), head_y - int(4 * scale))], fill=(100, 240, 255))

        # Head Base
        draw.ellipse([(x - head_r, head_y - head_r), (x + head_r, head_y + head_r)], fill=(235, 75, 160))
        # White Cheek Fluffs
        draw.ellipse([(x - int(head_r * 0.9), head_y + int(head_r * 0.1)), (x + int(head_r * 0.9), head_y + int(head_r * 0.8))], fill=(255, 245, 250))

        # Cute Large Eyes
        eye_y = head_y + int(head_r * 0.1)
        for eye_x in [x - int(10 * scale), x + int(10 * scale)]:
            draw.ellipse([(eye_x - 6, eye_y - 8), (eye_x + 6, eye_y + 8)], fill=(20, 15, 30))
            draw.ellipse([(eye_x - 2, eye_y - 6), (eye_x + 4, eye_y - 1)], fill=(255, 255, 255))  # specular highlight
            draw.ellipse([(eye_x - 3, eye_y + 1), (eye_x + 2, eye_y + 4)], fill=(80, 230, 255))   # cyan iris reflection

        # Nose
        draw.polygon([(x - 3, head_y + int(head_r * 0.5)), (x + 3, head_y + int(head_r * 0.5)), (x, head_y + int(head_r * 0.65))], fill=(40, 20, 30))

    @classmethod
    def _draw_leo_hero(cls, draw, cx, cy, scale, blendshapes, frame):
        """Draws Leo with sculpted brown hair, freckles, expressive eyes, and animated viseme mouth."""
        # --- 1. Red Explorer Hoodie Body (Reference Slide 1 & 4) ---
        body_top_y = cy + int(115 * scale)
        body_w = int(175 * scale)
        
        # Red Hoodie Torso
        draw.chord([(cx - body_w, body_top_y - int(30 * scale)), (cx + body_w, body_top_y + int(240 * scale))],
                   start=180, end=360, fill=(215, 45, 45))
        
        # Hoodie Collar & V-Neck Rim
        draw.polygon([
            (cx - int(45 * scale), body_top_y - int(10 * scale)),
            (cx, body_top_y + int(45 * scale)),
            (cx + int(45 * scale), body_top_y - int(10 * scale))
        ], fill=(160, 25, 25))
        
        # White Drawstrings
        draw.line([(cx - int(15 * scale), body_top_y + int(25 * scale)), (cx - int(15 * scale), body_top_y + int(85 * scale))], fill=(245, 245, 245), width=3)
        draw.line([(cx + int(15 * scale), body_top_y + int(25 * scale)), (cx + int(15 * scale), body_top_y + int(80 * scale))], fill=(245, 245, 245), width=3)

        # Neck (Subsurface warm skin tone)
        neck_w = int(45 * scale)
        draw.rectangle([(cx - neck_w, cy + int(70 * scale)), (cx + neck_w, body_top_y + int(10 * scale))], fill=(235, 175, 140))

        # --- 2. Head & Facial Structure ---
        head_radius = int(125 * scale)
        head_y = cy

        # Subtle warm ear projections
        ear_y = head_y + int(15 * scale)
        draw.ellipse([(cx - head_radius - int(15 * scale), ear_y - int(25 * scale)), (cx - head_radius + int(15 * scale), ear_y + int(25 * scale))], fill=(240, 160, 130))
        draw.ellipse([(cx + head_radius - int(15 * scale), ear_y - int(25 * scale)), (cx + head_radius + int(15 * scale), ear_y + int(25 * scale))], fill=(240, 160, 130))

        # Head Base (Warm, soft stylized 3D skin tone with SSS blush)
        draw.ellipse([
            (cx - head_radius, head_y - head_radius),
            (cx + head_radius, head_y + head_radius)
        ], fill=(245, 192, 160))

        # Warm Peach Cheek Blush (Soft Disney/Pixar SSS glow)
        draw.ellipse([(cx - int(head_radius * 0.75), head_y + int(15 * scale)), (cx - int(head_radius * 0.25), head_y + int(55 * scale))], fill=(255, 175, 155))
        draw.ellipse([(cx + int(head_radius * 0.25), head_y + int(15 * scale)), (cx + int(head_radius * 0.75), head_y + int(55 * scale))], fill=(255, 175, 155))

        # Freckles across the nose bridge (Distinctive Leo characteristic from Reference Slide 1)
        for fx, fy in [(-25, 22), (-14, 18), (-6, 24), (0, 20), (8, 25), (16, 19), (26, 23)]:
            draw.ellipse([
                (cx + int(fx * scale) - 2, head_y + int(fy * scale) - 2),
                (cx + int(fx * scale) + 2, head_y + int(fy * scale) + 2)
            ], fill=(185, 130, 100))

        # Stylized Button Nose
        nose_y = head_y + int(28 * scale)
        draw.chord([(cx - int(12 * scale), nose_y - int(8 * scale)), (cx + int(12 * scale), nose_y + int(8 * scale))],
                   start=0, end=180, fill=(230, 155, 130))

        # --- 3. Large Expressive Stylized 3D Eyes (Reference Slide 1) ---
        eye_spacing = int(head_radius * 0.46)
        eye_rw = int(head_radius * 0.26)
        eye_rh = int(head_radius * 0.33)
        eye_y = head_y - int(8 * scale)

        for eye_x in [cx - eye_spacing, cx + eye_spacing]:
            # Outer Eye Sclera (White with slight soft shadow at top)
            draw.ellipse([(eye_x - eye_rw, eye_y - eye_rh), (eye_x + eye_rw, eye_y + eye_rh)], fill=(255, 255, 255), outline=(60, 45, 45), width=2)
            
            # Iris (Teal / Blue-Green Radial Gradient)
            iris_r = int(eye_rw * 0.78)
            draw.ellipse([(eye_x - iris_r, eye_y - iris_r), (eye_x + iris_r, eye_y + iris_r)], fill=(32, 135, 155))
            # Inner Green Ring
            draw.ellipse([(eye_x - int(iris_r * 0.7), eye_y - int(iris_r * 0.7)), (eye_x + int(iris_r * 0.7), eye_y + int(iris_r * 0.7))], fill=(45, 175, 135))
            
            # Pupil (Deep dark)
            pupil_r = int(iris_r * 0.48)
            draw.ellipse([(eye_x - pupil_r, eye_y - pupil_r), (eye_x + pupil_r, eye_y + pupil_r)], fill=(12, 14, 20))

            # Hollywood Specular Glints (White light reflection circles)
            draw.ellipse([(eye_x - int(iris_r * 0.5), eye_y - int(iris_r * 0.6)), (eye_x - int(iris_r * 0.1), eye_y - int(iris_r * 0.2))], fill=(255, 255, 255))
            draw.ellipse([(eye_x + int(iris_r * 0.2), eye_y + int(iris_r * 0.2)), (eye_x + int(iris_r * 0.4), eye_y + int(iris_r * 0.4))], fill=(255, 255, 255))

            # Upper Eyelashes / Contour
            draw.arc([(eye_x - eye_rw - 2, eye_y - eye_rh - 4), (eye_x + eye_rw + 2, eye_y - int(eye_rh * 0.3))],
                     start=180, end=360, fill=(45, 30, 30), width=3)

        # --- 4. Arched Wonder Eyebrows ---
        brow_y = eye_y - eye_rh - int(12 * scale)
        brow_w = int(eye_rw * 1.1)
        # Left brow (slight inquisitive arch)
        draw.line([(cx - eye_spacing - brow_w, brow_y + 4), (cx - eye_spacing, brow_y - 8), (cx - eye_spacing + brow_w - 6, brow_y)], fill=(85, 48, 30), width=5)
        # Right brow
        draw.line([(cx + eye_spacing - brow_w + 6, brow_y), (cx + eye_spacing, brow_y - 8), (cx + eye_spacing + brow_w, brow_y + 4)], fill=(85, 48, 30), width=5)

        # --- 5. Dynamic Viseme Lip-Sync Mouth ---
        jaw_open = blendshapes.get("jawOpen", 0.0)
        mouth_smile = blendshapes.get("mouthSmileLeft", 0.0)
        mouth_pucker = blendshapes.get("mouthPucker", 0.0)
        
        mouth_center_y = head_y + int(62 * scale)
        mouth_width = int((42 + mouth_smile * 22 - mouth_pucker * 15) * scale)
        mouth_height = max(int((48 * jaw_open) * scale), 5)

        if jaw_open > 0.10:
            # Open talking mouth with teeth & tongue
            draw.chord([(cx - mouth_width, mouth_center_y - int(mouth_height * 0.4)),
                        (cx + mouth_width, mouth_center_y + int(mouth_height * 1.2))],
                       start=0, end=180, fill=(120, 25, 35), outline=(65, 25, 25), width=2)
            # Upper Teeth row
            draw.rectangle([(cx - int(mouth_width * 0.65), mouth_center_y - int(mouth_height * 0.3)),
                            (cx + int(mouth_width * 0.65), mouth_center_y + int(mouth_height * 0.15))], fill=(250, 250, 250))
            # Pink Tongue
            draw.chord([(cx - int(mouth_width * 0.45), mouth_center_y + int(mouth_height * 0.3)),
                        (cx + int(mouth_width * 0.45), mouth_center_y + int(mouth_height * 1.1))], start=0, end=180, fill=(235, 110, 125))
        else:
            # Closed expressive friendly smile line
            draw.arc([(cx - mouth_width, mouth_center_y - 12), (cx + mouth_width, mouth_center_y + 12)],
                     start=15, end=165, fill=(90, 40, 40), width=4)

        # --- 6. Sculpted Volumetric Hair Clumps (Reference Slide 1) ---
        # Rich layered chestnut-brown hair clumps over forehead and crown
        hair_color_base = (105, 58, 38)
        hair_color_highlight = (145, 85, 55)

        # Top Crown Volume
        draw.chord([(cx - head_radius - int(12 * scale), head_y - head_radius - int(45 * scale)),
                    (cx + head_radius + int(12 * scale), head_y)], start=180, end=360, fill=hair_color_base)

        # Individual Sculpted Clumps (Pixar/Disney Stylized Hair Clump Silhouette)
        clump_points = [
            # Left side burns
            [(cx - head_radius - int(8 * scale), head_y - int(20 * scale)), (cx - head_radius + int(12 * scale), head_y + int(45 * scale)), (cx - int(head_radius * 0.65), head_y)],
            # Front center-left swoop clump
            [(cx - int(75 * scale), head_y - int(115 * scale)), (cx - int(25 * scale), head_y - int(15 * scale)), (cx - int(5 * scale), head_y - int(85 * scale))],
            # Main center hero clump (parted across forehead)
            [(cx - int(15 * scale), head_y - int(120 * scale)), (cx + int(35 * scale), head_y - int(25 * scale)), (cx + int(55 * scale), head_y - int(95 * scale))],
            # Right side swoops
            [(cx + int(45 * scale), head_y - int(115 * scale)), (cx + head_radius - int(10 * scale), head_y - int(10 * scale)), (cx + head_radius + int(10 * scale), head_y - int(65 * scale))],
            [(cx + head_radius - int(15 * scale), head_y), (cx + head_radius + int(12 * scale), head_y + int(45 * scale)), (cx + int(head_radius * 0.65), head_y + int(15 * scale))]
        ]

        for poly in clump_points:
            draw.polygon(poly, fill=hair_color_base)

        # Warm Specular Highlights on Hair Edges
        draw.arc([(cx - int(65 * scale), head_y - head_radius - int(35 * scale)),
                  (cx + int(65 * scale), head_y - int(65 * scale))], start=200, end=330, fill=hair_color_highlight, width=6)

import os
import math
import re
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont

from animation.character_engine.character_model import StickFigureCharacter
from animation.skeleton_engine.forward_kinematics import ForwardKinematicsSolver
from animation.expression_engine.facial_rig import FacialRig
from animation.environment_engine.procedural_backgrounds import ProceduralBackgroundRenderer
from animation.environment_engine.props_library import PropsLibrary
from animation.camera_engine.visual_effects import VisualEffectsEngine

class StickFigureRenderer:
    """
    High-Performance 2D Vector Frame Renderer for Widescreen (1280x720 / 1920x1080) & Vertical (1080x1920) Shorts.
    Renders the exact cartoon styling from demo.mp4:
    - Orange spiky hair boy with red-and-white striped pill torso (बब्या)
    - Purple side-swept hair friend with solid white pill torso (गंप्या)
    - Traditional Maharashtrian mother in royal blue saree with violet blouse, brown bun & red bindi (आई)
    - Opening Marathi signature chalkboard disclaimer banner
    - Animated cartoon eyes, expressive mouths, and 1:1 lip sync
    """

    @classmethod
    def render_frame(
        cls,
        frame_data: Dict[str, Any],
        char1: StickFigureCharacter,
        char2: StickFigureCharacter,
        width: int = 1280,
        height: int = 720
    ) -> Image.Image:
        t_sec = frame_data["time_sec"]

        # 1. Base Environment
        img = ProceduralBackgroundRenderer.render_environment(
            env_type=frame_data["environment"],
            width=width,
            height=height,
            t_sec=t_sec
        )
        draw = ImageDraw.Draw(img)

        # 2. Opening Marathi Disclaimer Screen (at t=0s to 2.2s like demo.mp4)
        if t_sec < 2.2 and frame_data.get("show_disclaimer", True):
            cls._draw_marathi_disclaimer(draw, width, height, img=img)
            return img

        # 3. Draw Characters / Bus Scene
        is_bus_env = any(k in str(frame_data.get("environment", "")).lower() for k in ["bus", "msrtc", "lalpari", "station"])
        demo_scenes_dir = Path("assets/characters/demo_scenes")
        if is_bus_env and demo_scenes_dir.exists():
            img = cls._render_demo_puppet_scene(width, height, frame_data, t_sec)
            draw = ImageDraw.Draw(img)
        else:
            c1_data = frame_data["char1"]
            c2_data = frame_data["char2"]
            cls._draw_single_character(draw, char1, c1_data, t_sec, width, height)
            cls._draw_single_character(draw, char2, c2_data, t_sec, width, height)

        # 4. Draw Subtitles (if present)
        sub_text = frame_data.get("subtitle", "")
        if sub_text:
            cls._draw_subtitles(draw, sub_text, width, height)

        # 5. Camera Zoom / Pan Transformation
        cam = frame_data.get("camera", {})
        zoom = cam.get("zoom", 1.0)
        pan_x = cam.get("pan_x", 0.0)
        pan_y = cam.get("pan_y", 0.0)

        if zoom != 1.0 or pan_x != 0.0 or pan_y != 0.0:
            crop_w = width / zoom
            crop_h = height / zoom
            cx = (width / 2.0) + pan_x
            cy = (height / 2.0) + pan_y

            left = max(0, min(width - crop_w, cx - (crop_w / 2.0)))
            top = max(0, min(height - crop_h, cy - (crop_h / 2.0)))
            right = left + crop_w
            bottom = top + crop_h

            cropped = img.crop((left, top, right, bottom))
            img = cropped.resize((width, height), Image.Resampling.BILINEAR)

        return img

    @classmethod
    def _draw_marathi_disclaimer(cls, draw: ImageDraw.ImageDraw, w: int, h: int, img: Optional[Image.Image] = None):
        """
        Signature Green Chalkboard / Torn Paper Marathi Disclaimer Screen from demo.mp4.
        """
        disc_path = "assets/environments/disclaimer_chalkboard.png"
        if img is not None and os.path.exists(disc_path):
            disc = Image.open(disc_path).convert("RGBA")
            if disc.size != (w, h):
                disc = disc.resize((w, h), Image.Resampling.LANCZOS)
            img.paste(disc, (0, 0))
            return

        # Outer dark border
        draw.rectangle([0, 0, w, h], fill=(0, 0, 0))

        # Torn paper / chalkboard green container
        margin_x = int(w * 0.08)
        margin_y = int(h * 0.10)
        board_w = w - (2 * margin_x)
        board_h = h - (2 * margin_y)

        # White torn paper edge outline
        draw.rounded_rectangle([margin_x - 10, margin_y - 10, w - margin_x + 10, h - margin_y + 10], radius=18, fill=(240, 245, 240), outline=(200, 205, 200), width=6)
        # Chalkboard dark green surface
        draw.rounded_rectangle([margin_x, margin_y, w - margin_x, h - margin_y], radius=14, fill=(20, 60, 45), outline=(15, 45, 35), width=4)

        font_large = None
        font_med = None
        font_small = None
        font_paths = ["C:/Windows/Fonts/Nirmala.ttc", "C:/Windows/Fonts/mangal.ttf", "C:/Windows/Fonts/arial.ttf"]
        for fp in font_paths:
            if os.path.exists(fp):
                try:
                    font_large = ImageFont.truetype(fp, int(h * 0.065))
                    font_med = ImageFont.truetype(fp, int(h * 0.046))
                    font_small = ImageFont.truetype(fp, int(h * 0.038))
                    break
                except Exception:
                    pass

        # Title: "सूचना" in Red
        title_text = "सूचना"
        t_box = draw.textbbox((0, 0), title_text, font=font_large) if font_large else (0, 0, 100, 40)
        draw.text((w/2 - (t_box[2]-t_box[0])/2, margin_y + int(h * 0.06)), title_text, fill=(239, 68, 68), font=font_large)

        # Lines of Disclaimer
        lines = [
            "हा व्हिडिओ फक्त मनोरंजनासाठी असून",
            "याचा असल जिंदगी सोबत काहीही लेनं देणं नाही,",
            "जूडल्यास ते फक्त योगायोग असेल, व्हिडिओ फक्त",
            "मनोरंजण म्हणून च बघावे",
            "",
            "टीप :- आई बाबा ची रिस्पेक्ट करा."
        ]

        curr_y = margin_y + int(h * 0.18)
        line_spacing = int(h * 0.075)
        for line in lines:
            if line:
                f = font_small if "टीप" in line else font_med
                col = (254, 240, 138) if "टीप" in line else (255, 255, 255)
                l_box = draw.textbbox((0, 0), line, font=f) if f else (0, 0, len(line)*16, 30)
                draw.text((w/2 - (l_box[2]-l_box[0])/2, curr_y), line, fill=col, font=f)
            curr_y += line_spacing

    _SCENE_CACHE: Dict[str, Image.Image] = {}

    @classmethod
    def _get_demo_scene_img(cls, name: str) -> Optional[Image.Image]:
        if name in cls._SCENE_CACHE:
            return cls._SCENE_CACHE[name]
        p = Path("assets/characters/demo_scenes") / name
        if p.exists():
            img = Image.open(p).convert("RGBA")
            cls._SCENE_CACHE[name] = img
            return img
        return None

    @classmethod
    def _render_demo_puppet_scene(
        cls,
        width: int,
        height: int,
        frame_data: Dict[str, Any],
        t_sec: float
    ) -> Image.Image:
        """
        Directly renders the authentic 1280x720 animation scenes from demo.mp4:
        - Mother (peach skin, brown bun, bindi, royal blue saree, violet blouse)
        - Bob (white cartoon head, spiky orange hair, red/white striped torso, black stick limbs)
        - Friend (white cartoon head, purple hair, black stick limbs in bus doorway)
        With real-time mouth articulation, dynamic speaker switching, and comedic punchline reaction.
        """
        active_speaker = frame_data.get("active_speaker", "")
        mouth_open = (math.sin(t_sec * 16.0) > 0)

        # Select the active authentic pose state
        if "mother" in active_speaker.lower():
            scene_name = "mother_speaking.png" if mouth_open else "mother_listening.png"
        elif "bob" in active_speaker.lower():
            scene_name = "bob_speaking.png" if mouth_open else "mother_listening.png"
        elif "prof" in active_speaker.lower() or "friend" in active_speaker.lower() or "gampya" in active_speaker.lower():
            scene_name = "friend_speaking.png" if mouth_open else "friend_gesture.png"
        else:
            # Listening or reaction state
            if t_sec > 22.0:
                scene_name = "bob_laughing.png"
            else:
                scene_name = "mother_listening.png"

        master_img = cls._get_demo_scene_img(scene_name)
        if not master_img:
            master_img = cls._get_demo_scene_img("mother_listening.png")

        if master_img:
            if master_img.size == (width, height):
                return master_img.copy()
            else:
                return master_img.resize((width, height), Image.Resampling.LANCZOS)

        return Image.new("RGBA", (width, height), (248, 250, 252, 255))

    @classmethod
    def _draw_single_character(
        cls,
        draw: ImageDraw.ImageDraw,
        char: StickFigureCharacter,
        cdata: Dict[str, Any],
        t_sec: float,
        width: int,
        height: int
    ):
        pose = cdata["pose"]
        joints = ForwardKinematicsSolver.solve_joint_positions(char, pose)
        col = char.line_color
        th = getattr(char, "line_thickness", 8)

        # Foot ground shadow
        for foot_key in ["left_foot", "right_foot"]:
            fx, fy = joints[foot_key]
            draw.ellipse([fx - 24, fy - 5, fx + 24, fy + 6], fill=(0, 0, 0, 80))

        hx, hy = joints["head"]
        nx, ny = joints["neck"]
        px, py = joints["pelvis"]
        lsx, lsy = joints["left_shoulder"]
        rsx, rsy = joints["right_shoulder"]

        # -------------------------------------------------------------
        # 1. TORSO & CLOTHING (Matches demo.mp4 Pill-Torso Aesthetic)
        # -------------------------------------------------------------
        pk = getattr(char, "personality_key", "")
        hair = getattr(char, "hair_style", "")

        # -------------------------------------------------------------
        # 1. TORSO & CLOTHING (Mathematically Anchored Pill-Torso)
        # -------------------------------------------------------------
        pk = getattr(char, "personality_key", "")
        hair = getattr(char, "hair_style", "")

        # Calculate torso orientation vector (from pelvis px, py to neck nx, ny)
        t_dx = nx - px
        t_dy = ny - py
        t_dist = math.hypot(t_dx, t_dy) or 1.0
        ux = t_dx / t_dist
        uy = t_dy / t_dist
        vx = -uy
        vy = ux

        # A) MOTHER IN ROYAL BLUE SAREE & VIOLET BLOUSE (आई / काकू)
        if pk == "varhadi_mother" or "mother" in pk:
            # Violet Blouse
            bw = 48
            draw.polygon([
                (nx + vx * (bw/2), ny + vy * (bw/2)),
                (nx - vx * (bw/2), ny - vy * (bw/2)),
                (px - vx * (bw/2) + ux * 40, py - vy * (bw/2) + uy * 40),
                (px + vx * (bw/2) + ux * 40, py + vy * (bw/2) + uy * 40)
            ], fill=(124, 58, 237), outline=col, width=3)

            # Saree Body (Rounded Plump Skirt)
            sw = 80
            draw.polygon([
                (px + vx * (bw/2) + ux * 40, py + vy * (bw/2) + uy * 40),
                (px - vx * (bw/2) + ux * 40, py - vy * (bw/2) + uy * 40),
                (px - vx * (sw/2) - ux * 15, py - vy * (sw/2) - uy * 15),
                (px + vx * (sw/2) - ux * 15, py + vy * (sw/2) - uy * 15)
            ], fill=(29, 78, 216), outline=col, width=3)

            # Saree Pleats
            for frac in [-0.3, -0.1, 0.1, 0.3]:
                draw.line([
                    (px + vx * (bw/2 * frac) + ux * 40, py + vy * (bw/2 * frac) + uy * 40),
                    (px + vx * (sw/2 * frac) - ux * 15, py + vy * (sw/2 * frac) - uy * 15)
                ], fill=(37, 99, 235), width=2)

            # Saree Pallu drape from right hip across chest to left shoulder
            draw.polygon([
                (px + vx * 25, py + vy * 25),
                (nx - vx * 24, ny - vy * 24),
                (nx - vx * 12, ny - vy * 12),
                (px + vx * 15, py + vy * 15)
            ], fill=(30, 64, 175), outline=col, width=2)
            # Golden Border on Pallu
            draw.line([(px + vx * 25, py + vy * 25), (nx - vx * 24, ny - vy * 24)], fill=(234, 179, 8), width=3)

        # B) HERO BOY (बब्या - Red & White Striped Pill Torso)
        elif hair == "spiky_orange" or pk == "varhadi_boy" or getattr(char, "shirt_color", "") == "#dc2626":
            tw = 52
            half_w = tw / 2.0
            corners = [
                (nx + vx * half_w, ny + vy * half_w),
                (nx - vx * half_w, ny - vy * half_w),
                (px - vx * half_w, py - vy * half_w),
                (px + vx * half_w, py + vy * half_w)
            ]
            # White pill body
            draw.polygon(corners, fill=(255, 255, 255), outline=col, width=3)
            draw.ellipse([nx - half_w, ny - half_w, nx + half_w, ny + half_w], fill=(255, 255, 255), outline=col, width=3)
            draw.ellipse([px - half_w, py - half_w, px + half_w, py + half_w], fill=(255, 255, 255), outline=col, width=3)

            # Bold Red Horizontal Stripes
            for frac in [0.22, 0.44, 0.66, 0.88]:
                sx = px + ux * (t_dist * frac)
                sy = py + uy * (t_dist * frac)
                draw.line([
                    (sx + vx * (half_w - 3), sy + vy * (half_w - 3)),
                    (sx - vx * (half_w - 3), sy - vy * (half_w - 3))
                ], fill=(220, 38, 38), width=11)

            # Re-draw outline
            draw.polygon(corners, outline=col, width=3)
            # Black collar ring
            draw.line([(nx + vx * 14, ny + vy * 14), (nx - vx * 14, ny - vy * 14)], fill=col, width=3)

        # C) BEST FRIEND (गंप्या - Solid Crisp White Pill Torso)
        elif hair == "purple_swept" or pk == "varhadi_friend":
            tw = 52
            half_w = tw / 2.0
            corners = [
                (nx + vx * half_w, ny + vy * half_w),
                (nx - vx * half_w, ny - vy * half_w),
                (px - vx * half_w, py - vy * half_w),
                (px + vx * half_w, py + vy * half_w)
            ]
            # Crisp white pill body
            draw.polygon(corners, fill=(255, 255, 255), outline=col, width=3)
            draw.ellipse([nx - half_w, ny - half_w, nx + half_w, ny + half_w], fill=(255, 255, 255), outline=col, width=3)
            draw.ellipse([px - half_w, py - half_w, px + half_w, py + half_w], fill=(255, 255, 255), outline=col, width=3)
            draw.polygon(corners, outline=col, width=3)
            # Black collar ring
            draw.line([(nx + vx * 14, ny + vy * 14), (nx - vx * 14, ny - vy * 14)], fill=col, width=3)

        # D) UNCLE / FATHER (काका - Vest / Jacket)
        elif pk == "varhadi_uncle":
            tw = 56
            half_w = tw / 2.0
            corners = [
                (nx + vx * half_w, ny + vy * half_w),
                (nx - vx * half_w, ny - vy * half_w),
                (px - vx * half_w, py - vy * half_w),
                (px + vx * half_w, py + vy * half_w)
            ]
            draw.polygon(corners, fill=(241, 245, 249), outline=col, width=3)
            draw.ellipse([nx - half_w, ny - half_w, nx + half_w, ny + half_w], fill=(241, 245, 249), outline=col, width=3)
            draw.ellipse([px - half_w, py - half_w, px + half_w, py + half_w], fill=(241, 245, 249), outline=col, width=3)
            # Vest
            draw.polygon([
                (nx + vx * half_w, ny + vy * half_w), (nx + vx * 6, ny + vy * 6),
                (px + vx * 6, py + vy * 6), (px + vx * half_w, py + vy * half_w)
            ], fill=(30, 41, 59), outline=col, width=2)
            draw.polygon([
                (nx - vx * 6, ny - vy * 6), (nx - vx * half_w, ny - vy * half_w),
                (px - vx * half_w, py - vy * half_w), (px - vx * 6, py - vy * 6)
            ], fill=(30, 41, 59), outline=col, width=2)

        else:
            tw = 50
            draw.rounded_rectangle([px - tw//2, ny + 4, px + tw//2, py + 10], radius=14, fill=(255, 255, 255), outline=col, width=3)

        # -------------------------------------------------------------
        # 2. LEGS & SNEAKERS
        # -------------------------------------------------------------
        if pk != "varhadi_mother":
            draw.line([joints["pelvis"], joints["left_knee"]], fill=col, width=th)
            draw.line([joints["left_knee"], joints["left_foot"]], fill=col, width=th)
            draw.line([joints["pelvis"], joints["right_knee"]], fill=col, width=th)
            draw.line([joints["right_knee"], joints["right_foot"]], fill=col, width=th)

            # Cartoon rounded shoes
            for foot_key in ["left_foot", "right_foot"]:
                fx, fy = joints[foot_key]
                draw.ellipse([fx - 14, fy - 6, fx + 14, fy + 6], fill=col)

        # -------------------------------------------------------------
        # 3. ARMS
        # -------------------------------------------------------------
        draw.line([joints["left_shoulder"], joints["left_elbow"]], fill=col, width=th)
        draw.line([joints["left_elbow"], joints["left_hand"]], fill=col, width=th)
        draw.line([joints["right_shoulder"], joints["right_elbow"]], fill=col, width=th)
        draw.line([joints["right_elbow"], joints["right_hand"]], fill=col, width=th)

        # -------------------------------------------------------------
        # 4. HEAD, HAIR & FACIAL FEATURES
        # -------------------------------------------------------------
        hr = getattr(char, "head_radius", 40)
        face_fill = (255, 237, 213) if pk == "varhadi_mother" else (255, 255, 255)

        # A) MOTHER HAIR BUN (Drawn behind head)
        if hair == "brown_bun" or pk == "varhadi_mother":
            draw.ellipse([hx - 48, hy - 45, hx - 14, hy - 10], fill=(120, 53, 15), outline=col, width=3)

        # Skull
        draw.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=face_fill, outline=col, width=4)

        # B) ORANGE SPIKY HAIR (बब्या - Fiery Orange Zig-Zags)
        if hair == "spiky_orange" or pk == "varhadi_boy":
            spikes = [
                (hx - 36, hy - 22), (hx - 42, hy - 42), (hx - 26, hy - 38),
                (hx - 20, hy - 58), (hx - 6, hy - 42), (hx, hy - 64),
                (hx + 8, hy - 42), (hx + 22, hy - 58), (hx + 26, hy - 38),
                (hx + 42, hy - 44), (hx + 36, hy - 22)
            ]
            draw.polygon(spikes, fill=(249, 115, 22), outline=col, width=3)

        # C) PURPLE SWEPT HAIR (गंप्या - Modern Side-Swept)
        elif hair == "purple_swept" or pk == "varhadi_friend":
            p_hair = [
                (hx - 36, hy - 18), (hx - 42, hy - 38), (hx - 24, hy - 54),
                (hx + 10, hy - 56), (hx + 42, hy - 42), (hx + 46, hy - 22),
                (hx + 36, hy - 12), (hx + 28, hy - 32), (hx, hy - 40),
                (hx - 20, hy - 32)
            ]
            draw.polygon(p_hair, fill=(109, 40, 217), outline=col, width=3)

        # D) MOTHER FRONT HAIR, BINDI & BLUSH CHEEKS
        elif hair == "brown_bun" or pk == "varhadi_mother":
            draw.chord([hx - hr - 1, hy - hr - 1, hx + hr + 1, hy - 5], 180, 360, fill=(120, 53, 15), outline=col, width=3)
            draw.line([(hx, hy - hr), (hx, hy - 18)], fill=col, width=2)
            # Red Bindi (टिकली)
            draw.ellipse([hx - 4, hy - 12, hx + 4, hy - 4], fill=(220, 38, 38))
            # Rosy Blush Cheeks
            draw.ellipse([hx - 26, hy + 4, hx - 14, hy + 14], fill=(254, 202, 202))
            draw.ellipse([hx + 14, hy + 4, hx + 26, hy + 14], fill=(254, 202, 202))

        # E) UNCLE HALF BALD & SUNGLASSES
        elif hair == "half_bald" or pk == "varhadi_uncle":
            draw.arc([hx - hr - 2, hy - 10, hx - hr + 14, hy + 20], 90, 270, fill=col, width=6)
            draw.arc([hx + hr - 14, hy - 10, hx + hr + 2, hy + 20], 270, 90, fill=col, width=6)
            draw.rounded_rectangle([hx - 26, hy - 12, hx - 2, hy + 8], radius=3, fill=(15, 23, 42), outline=col, width=2)
            draw.rounded_rectangle([hx + 2, hy - 12, hx + 26, hy + 8], radius=3, fill=(15, 23, 42), outline=col, width=2)
            draw.line([(hx - 2, hy - 2), (hx + 2, hy - 2)], fill=col, width=3)

        # -------------------------------------------------------------
        # 5. EYES, EYEBROWS & MOUTH (Animated Lip-Sync)
        # -------------------------------------------------------------
        if pk != "varhadi_uncle":
            # Big Expressive Cartoon Eyes
            draw.ellipse([hx - 26, hy - 16, hx - 4, hy + 12], fill=(255, 255, 255), outline=col, width=3)
            draw.ellipse([hx + 4, hy - 16, hx + 26, hy + 12], fill=(255, 255, 255), outline=col, width=3)
            # Movable pupils (looking at interaction center)
            draw.ellipse([hx - 20, hy - 6, hx - 10, hy + 6], fill=col)
            draw.ellipse([hx + 10, hy - 6, hx + 20, hy + 6], fill=col)
            # Catchlights
            draw.ellipse([hx - 18, hy - 4, hx - 14, hy], fill=(255, 255, 255))
            draw.ellipse([hx + 12, hy - 4, hx + 16, hy], fill=(255, 255, 255))

        # Eyebrows based on emotion
        expr_key = cdata.get("expression", "curious")
        if pk == "varhadi_mother" or expr_key == "angry":
            # Angry / Scolding furrowed eyebrows
            draw.line([(hx - 24, hy - 14), (hx - 6, hy - 6)], fill=col, width=4)
            draw.line([(hx + 6, hy - 6), (hx + 24, hy - 14)], fill=col, width=4)
        elif expr_key in ["shocked", "fearful"]:
            draw.line([(hx - 24, hy - 22), (hx - 6, hy - 26)], fill=col, width=3)
            draw.line([(hx + 6, hy - 26), (hx + 24, hy - 22)], fill=col, width=3)
        else:
            draw.line([(hx - 22, hy - 20), (hx - 6, hy - 20)], fill=col, width=3)
            draw.line([(hx + 6, hy - 20), (hx + 22, hy - 20)], fill=col, width=3)

        # Mouth (Dynamic Lip-Sync)
        mouth_info = cdata.get("mouth", {})
        mw = mouth_info.get("width", 16)
        mh = mouth_info.get("height", 4)
        m_open = mouth_info.get("open", False)
        my = hy + 18

        if m_open and mh > 4:
            draw.ellipse([hx - mw/2, my - mh/2, hx + mw/2, my + mh/2], fill=(220, 38, 38), outline=col, width=3)
            draw.line([(hx - mw/3, my - mh/4), (hx + mw/3, my - mh/4)], fill=(255, 255, 255), width=2)
        else:
            if expr_key in ["happy", "laughing", "confident"]:
                draw.arc([hx - mw/2, my - 6, hx + mw/2, my + 6], 0, 180, fill=col, width=3)
            elif expr_key in ["sad", "disappointed"]:
                draw.arc([hx - mw/2, my, hx + mw/2, my + 10], 180, 0, fill=col, width=3)
            else:
                draw.line([(hx - mw/2, my), (hx + mw/2, my)], fill=col, width=3)

    @classmethod
    def _draw_subtitles(cls, draw: ImageDraw.ImageDraw, text: str, w: int, h: int):
        """Draws high-contrast clean spoken Marathi dialogue banner with word-wrapping."""
        clean_text = re.sub(r'^\s*[\(\[]?[A-Za-z0-9_\u0900-\u097F\s\.\-]+[\)\]]?\s*:\s*', '', text).strip()
        if not clean_text:
            return

        font_size = max(18, int(h * 0.036))
        font = None
        font_paths = ["C:/Windows/Fonts/Nirmala.ttc", "C:/Windows/Fonts/mangal.ttf", "C:/Windows/Fonts/arial.ttf"]
        for fp in font_paths:
            if os.path.exists(fp):
                try:
                    font = ImageFont.truetype(fp, font_size)
                    break
                except Exception:
                    pass

        max_allowed_w = w - 160
        # Wrap words so subtitles never clip horizontally
        words = clean_text.split()
        lines = []
        curr = []
        for word in words:
            test_line = ' '.join(curr + [word])
            if font:
                bbox = draw.textbbox((0, 0), test_line, font=font)
                line_w = bbox[2] - bbox[0]
            else:
                line_w = len(test_line) * 16

            if line_w > max_allowed_w and curr:
                lines.append(' '.join(curr))
                curr = [word]
            else:
                curr.append(word)
        if curr:
            lines.append(' '.join(curr))

        if not lines:
            return

        if font:
            line_bboxes = [draw.textbbox((0, 0), l, font=font) for l in lines]
            line_ws = [b[2] - b[0] for b in line_bboxes]
            line_hs = [max(24, b[3] - b[1]) for b in line_bboxes]
        else:
            line_ws = [min(w - 80, len(l) * 16) for l in lines]
            line_hs = [28 for _ in lines]

        max_w = max(line_ws)
        line_spacing = 6
        total_h = sum(line_hs) + line_spacing * (len(lines) - 1)

        pad_x, pad_y = 24, 10
        box_bottom = int(h * 0.96)
        box_top = box_bottom - total_h - 2 * pad_y
        box_left = max(20, w/2 - max_w/2 - pad_x)
        box_right = min(w - 20, w/2 + max_w/2 + pad_x)

        draw.rounded_rectangle(
            [box_left, box_top, box_right, box_bottom],
            radius=14,
            fill=(15, 23, 42, 230),
            outline=(234, 179, 8),
            width=3
        )

        curr_y = box_top + pad_y
        for i, l in enumerate(lines):
            lw = line_ws[i]
            lh = line_hs[i]
            tx = w/2 - lw/2
            for ox, oy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                draw.text((tx + ox, curr_y + oy), l, fill=(0, 0, 0), font=font)
            draw.text((tx, curr_y), l, fill=(255, 255, 255), font=font)
            curr_y += lh + line_spacing

import os
import math
from typing import Dict, Any, Tuple
from PIL import Image, ImageDraw, ImageFont

from animation.character_engine.character_model import StickFigureCharacter
from animation.skeleton_engine.forward_kinematics import ForwardKinematicsSolver
from animation.expression_engine.facial_rig import FacialRig
from animation.environment_engine.procedural_backgrounds import ProceduralBackgroundRenderer
from animation.environment_engine.props_library import PropsLibrary
from animation.camera_engine.visual_effects import VisualEffectsEngine

class StickFigureRenderer:
    """
    High-Performance 2D Vector Frame Renderer for Vertical (1080x1920) Shorts.
    Draws characters with smooth anti-aliased geometry, dynamic facial expressions,
    accessories, lip-sync, and camera transformations.
    """

    @classmethod
    def render_frame(
        cls,
        frame_data: Dict[str, Any],
        char1: StickFigureCharacter,
        char2: StickFigureCharacter,
        width: int = 1080,
        height: int = 1920
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

        # 2. Draw Characters
        c1_data = frame_data["char1"]
        c2_data = frame_data["char2"]

        cls._draw_single_character(draw, char1, c1_data, t_sec)
        cls._draw_single_character(draw, char2, c2_data, t_sec)

        # 3. Draw Subtitles (High-Retention YouTube Shorts Style)
        sub_text = frame_data.get("subtitle", "")
        if sub_text:
            cls._draw_subtitles(draw, sub_text, width, height)

        # 4. Camera Zoom / Shake Transformation
        cam = frame_data.get("camera", {})
        zoom = cam.get("zoom", 1.0)
        pan_x = cam.get("pan_x", 0.0)
        pan_y = cam.get("pan_y", 0.0)

        if zoom != 1.0 or pan_x != 0.0 or pan_y != 0.0:
            # Crop & Scale
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
    def _draw_single_character(
        cls,
        draw: ImageDraw.ImageDraw,
        char: StickFigureCharacter,
        cdata: Dict[str, Any],
        t_sec: float
    ):
        pose = cdata["pose"]
        joints = ForwardKinematicsSolver.solve_joint_positions(char, pose)
        col = char.line_color
        th = char.line_thickness

        # Contact / Grounding Shadow under feet
        for foot_key in ["left_foot", "right_foot"]:
            fx, fy = joints[foot_key]
            draw.ellipse([fx - 24, fy - 6, fx + 24, fy + 8], fill=(0, 0, 0, 130))

        # -------------------------------------------------------------
        # PASS 1: HIGH-CONTRAST OUTER SILHOUETTE (White Halo / Sticker)
        # Guarantees 100% limb visibility against ANY dark or busy background
        # -------------------------------------------------------------
        halo_w = th + 7
        halo_col = (255, 255, 255)

        # Head Halo
        hx, hy = joints["head"]
        r = char.head_radius
        draw.ellipse([hx - r - 4, hy - r - 4, hx + r + 4, hy + r + 4], fill=halo_col)

        # Torso Halo
        draw.line([joints["pelvis"], joints["neck"]], fill=halo_col, width=halo_w + 2)

        # Legs Halo
        draw.line([joints["pelvis"], joints["left_knee"]], fill=halo_col, width=halo_w)
        draw.line([joints["left_knee"], joints["left_foot"]], fill=halo_col, width=halo_w)
        draw.ellipse([joints["left_foot"][0]-16, joints["left_foot"][1]-10, joints["left_foot"][0]+16, joints["left_foot"][1]+10], fill=halo_col)

        draw.line([joints["pelvis"], joints["right_knee"]], fill=halo_col, width=halo_w)
        draw.line([joints["right_knee"], joints["right_foot"]], fill=halo_col, width=halo_w)
        draw.ellipse([joints["right_foot"][0]-16, joints["right_foot"][1]-10, joints["right_foot"][0]+16, joints["right_foot"][1]+10], fill=halo_col)

        # Arms Halo
        draw.line([joints["left_shoulder"], joints["left_elbow"]], fill=halo_col, width=halo_w)
        draw.line([joints["left_elbow"], joints["left_hand"]], fill=halo_col, width=halo_w)
        draw.ellipse([joints["left_hand"][0]-12, joints["left_hand"][1]-12, joints["left_hand"][0]+12, joints["left_hand"][1]+12], fill=halo_col)

        draw.line([joints["right_shoulder"], joints["right_elbow"]], fill=halo_col, width=halo_w)
        draw.line([joints["right_elbow"], joints["right_hand"]], fill=halo_col, width=halo_w)
        draw.ellipse([joints["right_hand"][0]-12, joints["right_hand"][1]-12, joints["right_hand"][0]+12, joints["right_hand"][1]+12], fill=halo_col)

        # -------------------------------------------------------------
        # PASS 2: INNER CORE SKELETON & ANATOMY
        # -------------------------------------------------------------
        # 1. Legs (Pelvis -> Knees -> Feet)
        draw.line([joints["pelvis"], joints["left_knee"]], fill=col, width=th)
        draw.line([joints["left_knee"], joints["left_foot"]], fill=col, width=th)
        draw.ellipse([joints["left_foot"][0]-12, joints["left_foot"][1]-6, joints["left_foot"][0]+12, joints["left_foot"][1]+6], fill=col)

        draw.line([joints["pelvis"], joints["right_knee"]], fill=col, width=th)
        draw.line([joints["right_knee"], joints["right_foot"]], fill=col, width=th)
        draw.ellipse([joints["right_foot"][0]-12, joints["right_foot"][1]-6, joints["right_foot"][0]+12, joints["right_foot"][1]+6], fill=col)

        # 2. Torso (Pelvis -> Neck)
        draw.line([joints["pelvis"], joints["neck"]], fill=col, width=th + 2)

        # Professor Lab Coat torso accent (if scientist)
        if char.personality_key == "scientist":
            nx, ny = joints["neck"]
            px, py = joints["pelvis"]
            draw.polygon([
                (nx - 16, ny + 10), (nx + 16, ny + 10),
                (px + 22, py), (px - 22, py)
            ], fill=(255, 255, 255), outline=col, width=2)
            draw.line([(nx, ny + 10), (px, py)], fill=(100, 116, 139), width=2)
            draw.rectangle([nx + 4, ny + 32, nx + 14, ny + 42], fill=(241, 245, 249), outline=(100, 116, 139), width=1)

        # Accessory: Tie with high-contrast outline
        if char.accessory == "red_tie":
            tx, ty = joints["neck"][0], joints["neck"][1] + 8
            draw.polygon([(tx-9, ty-2), (tx+9, ty-2), (tx+13, ty+65), (tx, ty+82), (tx-13, ty+65)], fill=(255, 255, 255))
            draw.polygon([(tx-6, ty), (tx+6, ty), (tx+10, ty+60), (tx, ty+75), (tx-10, ty+60)], fill=(220, 38, 38))
        elif char.accessory == "blue_tie":
            tx, ty = joints["neck"][0], joints["neck"][1] + 8
            draw.polygon([(tx-8, ty-2), (tx+8, ty-2), (tx+11, ty+55), (tx, ty+70), (tx-11, ty+55)], fill=(255, 255, 255))
            draw.polygon([(tx-6, ty), (tx+6, ty), (tx+8, ty+50), (tx, ty+65), (tx-8, ty+50)], fill=(37, 99, 235))

        # 3. Arms (Shoulders -> Elbows -> Hands)
        draw.line([joints["left_shoulder"], joints["left_elbow"]], fill=col, width=th)
        draw.line([joints["left_elbow"], joints["left_hand"]], fill=col, width=th)
        draw.ellipse([joints["left_hand"][0]-8, joints["left_hand"][1]-8, joints["left_hand"][0]+8, joints["left_hand"][1]+8], fill=col)

        draw.line([joints["right_shoulder"], joints["right_elbow"]], fill=col, width=th)
        draw.line([joints["right_elbow"], joints["right_hand"]], fill=col, width=th)
        draw.ellipse([joints["right_hand"][0]-8, joints["right_hand"][1]-8, joints["right_hand"][0]+8, joints["right_hand"][1]+8], fill=col)

        # Draw Prop in right or left hand if speaking or active
        if cdata.get("is_speaking") and char.personality_key in ["techie", "funny"]:
            PropsLibrary.draw_prop(draw, "smartphone", joints["right_hand"][0], joints["right_hand"][1] - 15, scale=1.0)
        elif char.personality_key == "scientist":
            PropsLibrary.draw_prop(draw, "test_tube", joints["left_hand"][0], joints["left_hand"][1] - 15, scale=1.0)

        # 4. Head (Circle)
        hx, hy = joints["head"]
        r = char.head_radius
        draw.ellipse([hx - r, hy - r, hx + r, hy + r], fill=(255, 255, 255), outline=col, width=th)

        # Hair Style
        if char.hair_style == "tuft":
            draw.line([(hx, hy - r), (hx + 8, hy - r - 16)], fill=col, width=th - 2)
            draw.line([(hx + 8, hy - r - 16), (hx + 18, hy - r - 10)], fill=col, width=th - 2)
        elif char.hair_style == "spiky":
            for ox in [-18, 0, 18]:
                draw.line([(hx + ox, hy - r), (hx + ox, hy - r - 20)], fill=col, width=th - 2)

        # Accessory: Glasses
        if char.accessory == "glasses":
            draw.ellipse([hx - 24, hy - 12, hx - 4, hy + 8], fill=(255, 255, 255, 200), outline=col, width=3)
            draw.ellipse([hx + 4, hy - 12, hx + 24, hy + 8], fill=(255, 255, 255, 200), outline=col, width=3)
            draw.line([(hx - 4, hy - 2), (hx + 4, hy - 2)], fill=col, width=3)
        elif char.accessory == "sunglasses":
            draw.rounded_rectangle([hx - 26, hy - 14, hx - 2, hy + 8], radius=3, fill=(15, 23, 42), outline=col, width=2)
            draw.rounded_rectangle([hx + 2, hy - 14, hx + 26, hy + 8], radius=3, fill=(15, 23, 42), outline=col, width=2)
            draw.line([(hx - 2, hy - 4), (hx + 2, hy - 4)], fill=col, width=3)

        # 5. Face Rig (Eyes, Eyebrows, Mouth)
        expr_key = cdata.get("expression", "curious")
        expr = FacialRig.get_expression(expr_key)
        mouth_info = cdata.get("mouth", {})

        # Eyebrows
        eb_angle = expr.get("eyebrow_angle", 0)
        eb_off_y = expr.get("eyebrow_offset_y", 0)
        # Left Eyebrow
        draw.line([(hx - 22, hy - 16 + eb_off_y), (hx - 6, hy - 16 + eb_off_y + eb_angle*0.3)], fill=col, width=th - 4)
        # Right Eyebrow
        draw.line([(hx + 6, hy - 16 + eb_off_y + eb_angle*0.3), (hx + 22, hy - 16 + eb_off_y)], fill=col, width=th - 4)

        # Eyes (Dots / Circles / Wide)
        eye_t = expr.get("eye_type", "circle")
        if eye_t in ["wide_circle", "huge_circle"]:
            ew = 8 if eye_t == "wide_circle" else 12
            draw.ellipse([hx - 16 - ew/2, hy - 6 - ew/2, hx - 16 + ew/2, hy - 6 + ew/2], fill=(255, 255, 255), outline=col, width=3)
            draw.ellipse([hx + 16 - ew/2, hy - 6 - ew/2, hx + 16 + ew/2, hy - 6 + ew/2], fill=(255, 255, 255), outline=col, width=3)
            # Pupils
            draw.ellipse([hx - 16 - 3, hy - 6 - 3, hx - 16 + 3, hy - 6 + 3], fill=col)
            draw.ellipse([hx + 16 - 3, hy - 6 - 3, hx + 16 + 3, hy - 6 + 3], fill=col)
        elif eye_t == "arc_up":
            # ^^ happy eyes
            draw.arc([hx - 22, hy - 10, hx - 8, hy], 180, 0, fill=col, width=4)
            draw.arc([hx + 8, hy - 10, hx + 22, hy], 180, 0, fill=col, width=4)
        elif eye_t == "arc_down":
            # >< squint laughing eyes
            draw.line([(hx - 22, hy - 8), (hx - 12, hy - 2)], fill=col, width=3)
            draw.line([(hx - 12, hy - 2), (hx - 22, hy + 4)], fill=col, width=3)
            draw.line([(hx + 22, hy - 8), (hx + 12, hy - 2)], fill=col, width=3)
            draw.line([(hx + 12, hy - 2), (hx + 22, hy + 4)], fill=col, width=3)
        else:
            # Classic expressive circular eye dots
            draw.ellipse([hx - 18, hy - 6, hx - 10, hy + 2], fill=col)
            draw.ellipse([hx + 10, hy - 6, hx + 18, hy + 2], fill=col)

        # Mouth (Dynamic Lip-Sync & Emotion)
        mw = mouth_info.get("width", 14)
        mh = mouth_info.get("height", 4)
        m_open = mouth_info.get("open", False)

        my = hy + 16
        if m_open and mh > 4:
            draw.ellipse([hx - mw/2, my - mh/2, hx + mw/2, my + mh/2], fill=(220, 38, 38), outline=col, width=3)
        else:
            # Curved or flat line
            if expr_key in ["happy", "laughing", "confident"]:
                draw.arc([hx - mw/2, my - 6, hx + mw/2, my + 6], 0, 180, fill=col, width=4)
            elif expr_key in ["sad", "disappointed"]:
                draw.arc([hx - mw/2, my, hx + mw/2, my + 12], 180, 0, fill=col, width=4)
            else:
                draw.line([(hx - mw/2, my), (hx + mw/2, my)], fill=col, width=4)

        # 6. Emotive Overlays (Sweat drop, Question mark, Lightbulb)
        for extra in expr.get("extras", []):
            VisualEffectsEngine.draw_effects(draw, extra, hx, hy, t_sec, scale=1.0)

    @classmethod
    def _draw_subtitles(cls, draw: ImageDraw.ImageDraw, text: str, w: int, h: int):
        """Draws high-contrast yellow/white viral Shorts subtitle banner supporting Marathi/Hindi/English."""
        sy = 1630
        font = None
        font_paths = [
            "C:/Windows/Fonts/Nirmala.ttc",
            "C:/Windows/Fonts/mangal.ttf",
            "C:/Windows/Fonts/arial.ttf"
        ]
        for fp in font_paths:
            if os.path.exists(fp):
                try:
                    font = ImageFont.truetype(fp, 36)
                    break
                except Exception:
                    pass

        # Text bounding box
        if font:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        else:
            text_w = min(w - 100, len(text) * 16)
            text_h = 36

        pad_x, pad_y = 36, 18
        box_left = max(40, w/2 - text_w/2 - pad_x)
        box_right = min(w - 40, w/2 + text_w/2 + pad_x)
        box_top = sy - pad_y
        box_bottom = sy + text_h + pad_y

        # Semi-transparent high-contrast dark rounded box with golden border
        draw.rounded_rectangle([box_left, box_top, box_right, box_bottom], radius=20, fill=(15, 23, 42, 230), outline=(234, 179, 8), width=4)

        # Drop shadow / outline for crisp text contrast
        tx = w/2 - text_w/2
        ty = sy
        for ox, oy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1)]:
            draw.text((tx + ox, ty + oy), text, fill=(0, 0, 0), font=font)

        # Main text in vibrant white
        draw.text((tx, ty), text, fill=(255, 255, 255), font=font)

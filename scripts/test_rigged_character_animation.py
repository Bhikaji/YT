"""
Prototype for Rigged 3D Pixar Character Animation (Walk, Hand Pointing, Eye Saccades/Blinks, Emotional Lip-Sync)
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont

WIDTH = 1080
HEIGHT = 1920
FONT_PATH = r"C:\Windows\Fonts\arialbd.ttf"
FONT_MAIN = ImageFont.truetype(FONT_PATH, 34)
FONT_NAME = ImageFont.truetype(FONT_PATH, 24)

SRC_SCENE1 = r"E:\YT\assets\characters\demo_leo_and_lumi_pixar.jpg"
SRC_PORTRAIT = r"E:\YT\assets\characters\char_leo_portrait.jpg"

def create_animated_frame(frame_idx, total_frames=300):
    t = frame_idx / 30.0
    
    if frame_idx < 155:
        # SCENE 1: Walk Cycle + Hand Pointing + Eye Gaze + Lumi
        source = Image.open(SRC_SCENE1).convert("RGBA")
        
        # Background blur fill
        bg_scale = max(WIDTH / source.width, HEIGHT / source.height) * 1.15
        bg_w, bg_h = int(source.width * bg_scale), int(source.height * bg_scale)
        bg = source.resize((bg_w, bg_h), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=40))
        bg = ImageEnhance.Brightness(bg).enhance(0.40)
        left = (bg_w - WIDTH) // 2
        top = (bg_h - HEIGHT) // 2
        frame = bg.crop((left, top, left + WIDTH, top + HEIGHT))
        
        # Camera zoom
        zoom = 1.0 + 0.08 * (frame_idx / 155.0)
        fg_w = int(WIDTH * zoom)
        fg_h = int((WIDTH / source.width) * source.height * zoom)
        fg = source.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
        
        fg_x = (WIDTH - fg_w) // 2
        fg_y = (HEIGHT - fg_h) // 2
        
        # If in walking phase (frames 0 to 95):
        if frame_idx <= 95:
            walk_phase = (frame_idx / 26.0) * (2 * math.pi)
            # Bobbing bounce of walk locomotion
            walk_bob = int(abs(math.sin(walk_phase)) * 14)
            # Sway angle
            walk_sway = math.sin(walk_phase) * 1.8
            fg_y += walk_bob
            
            # Subtle rotation for natural body sway
            fg = fg.rotate(walk_sway, resample=Image.Resampling.BICUBIC, center=(fg_w // 2, fg_h // 2))
        else:
            # Stop & Settle into Stance
            fg_y += 6
            
        # Paste foreground onto frame
        shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw_sh = ImageDraw.Draw(shadow)
        draw_sh.rectangle([fg_x - 6, fg_y - 6, fg_x + fg_w + 6, fg_y + fg_h + 6], fill=(0, 0, 0, 180))
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=24))
        frame.paste(shadow, (0, 0), shadow)
        frame.paste(fg, (fg_x, fg_y), fg)
        
        # Overlay Hand Pointing Animation (Frames 95 to 155):
        # Leo's right arm and hand raises and points at the crystals!
        if frame_idx >= 95:
            progress = min(1.0, (frame_idx - 95) / 35.0)
            arm_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            draw_arm = ImageDraw.Draw(arm_layer)
            
            # Anchor shoulder position on Leo
            shoulder_x = fg_x + int(fg_w * 0.44)
            shoulder_y = fg_y + int(fg_h * 0.52)
            
            # Animated hand pointing coordinates
            target_hand_x = shoulder_x + int(120 * progress)
            target_hand_y = shoulder_y - int(80 * progress)
            
            # Draw stylized red hoodie sleeve raising
            draw_arm.line([shoulder_x, shoulder_y, target_hand_x, target_hand_y], fill=(215, 52, 42, int(230 * progress)), width=int(26 * zoom))
            # Forearm / cuff
            draw_arm.ellipse([target_hand_x - 14, target_hand_y - 14, target_hand_x + 14, target_hand_y + 14], fill=(215, 52, 42, int(240 * progress)))
            # Pointing hand & index finger
            finger_x = target_hand_x + int(24 * progress)
            finger_y = target_hand_y - int(16 * progress)
            draw_arm.line([target_hand_x, target_hand_y, finger_x, finger_y], fill=(242, 192, 162, int(250 * progress)), width=int(10 * zoom))
            draw_arm.ellipse([target_hand_x - 10, target_hand_y - 10, target_hand_x + 10, target_hand_y + 10], fill=(242, 192, 162, int(250 * progress)))
            
            arm_layer = arm_layer.filter(ImageFilter.GaussianBlur(radius=1))
            frame = Image.alpha_composite(frame, arm_layer)
            
        # Overlay Eye Blink & Mouth Lip-Sync on Leo in Scene 1:
        face_x = fg_x + int(fg_w * 0.455)
        face_y = fg_y + int(fg_h * 0.435)
        
        # Natural Blink at frame 38-44 and frame 115-121
        is_blinking = (38 <= frame_idx <= 44) or (115 <= frame_idx <= 121)
        if is_blinking:
            blink_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            draw_bl = ImageDraw.Draw(blink_layer)
            # Left & Right eyelids drop
            draw_bl.ellipse([face_x - 30, face_y - 12, face_x - 10, face_y + 4], fill=(225, 172, 142, 230))
            draw_bl.ellipse([face_x + 10, face_y - 12, face_x + 30, face_y + 4], fill=(225, 172, 142, 230))
            blink_layer = blink_layer.filter(ImageFilter.GaussianBlur(radius=2))
            frame = Image.alpha_composite(frame, blink_layer)
            
        # Mouth Viseme Lip-Sync (Frames 95 to 145: "Whoa... Lumi, look! The ancient crystals are glowing!")
        if 98 <= frame_idx <= 145:
            mouth_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            draw_mo = ImageDraw.Draw(mouth_layer)
            mouth_y = face_y + 32
            # Mouth aperture oscillates with phonemes
            mouth_open = int(abs(math.sin((frame_idx - 98) * 0.45)) * 9) + 2
            draw_mo.ellipse([face_x - 8, mouth_y - mouth_open, face_x + 8, mouth_y + mouth_open], fill=(120, 35, 30, 220))
            draw_mo.arc([face_x - 12, mouth_y - 4, face_x + 12, mouth_y + 8], 0, 180, fill=(200, 140, 120, 240), width=2)
            mouth_layer = mouth_layer.filter(ImageFilter.GaussianBlur(radius=1))
            frame = Image.alpha_composite(frame, mouth_layer)
            
        # Floating bioluminescent spores
        random.seed(42)
        spores = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw_sp = ImageDraw.Draw(spores)
        for i in range(40):
            base_x = random.randint(40, WIDTH - 40)
            speed_y = random.uniform(60, 140)
            y = int((HEIGHT - (t * speed_y + random.randint(0, HEIGHT))) % HEIGHT)
            drift_x = int(base_x + math.sin(t * 2.0 + i) * 25)
            radius = random.randint(4, 9)
            color = (60, 220, 255, 210) if i % 2 == 0 else (255, 90, 200, 210)
            draw_sp.ellipse([drift_x - radius, y - radius, drift_x + radius, y + radius], fill=color)
        spores = spores.filter(ImageFilter.GaussianBlur(radius=3))
        frame = Image.alpha_composite(frame, spores)
        
        # Subtitle
        if 15 <= frame_idx <= 145:
            draw_txt = ImageDraw.Draw(frame)
            sub_text = '“Whoa... Lumi, look! The ancient crystals are glowing!”'
            pill_w, pill_h = 1000, 110
            pill_x = (WIDTH - pill_w) // 2
            pill_y = HEIGHT - 360
            draw_txt.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=28, fill=(8, 12, 22, 220), outline=(56, 189, 248, 140), width=2)
            draw_txt.text((pill_x + 36, pill_y + 16), "LEO", font=FONT_NAME, fill=(56, 189, 248))
            draw_txt.text((WIDTH // 2, pill_y + 68), sub_text, font=FONT_MAIN, fill=(255, 245, 150), anchor="mm")
            
    else:
        # SCENE 2: Hero Close-Up with Eye Saccades, Hand Gripping Strap, and Whispered Lip-Sync
        source = Image.open(SRC_PORTRAIT).convert("RGBA")
        local_f = frame_idx - 155
        local_t = local_f / 30.0
        
        base_scale = max(WIDTH / source.width, HEIGHT / source.height) * 1.05
        zoom = base_scale * (1.0 + 0.08 * (local_f / 145.0))
        target_w = int(source.width * zoom)
        target_h = int(source.height * zoom)
        scaled = source.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Breathing movement
        breath = int(math.sin(local_t * math.pi * 1.2) * 6)
        crop_x = (target_w - WIDTH) // 2 + int(math.sin(local_t * 0.8) * 4)
        crop_y = int((target_h - HEIGHT) * 0.35) - breath
        frame = scaled.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
        
        # Eye Saccades & Movement:
        # In frame 156-210: Eyes look upward at the glowing cavern ceiling.
        # At frame 210-230: Eyes dart down toward the camera.
        # Double-blink at frame 215-223.
        eye_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw_eye = ImageDraw.Draw(eye_layer)
        
        left_eye_center = (WIDTH // 2 - 128, int(HEIGHT * 0.448))
        right_eye_center = (WIDTH // 2 + 36, int(HEIGHT * 0.448))
        
        # Calculate pupil gaze offset
        if local_f < 55:
            # Looking up in awe
            gaze_ox, gaze_oy = -4, -14
        else:
            # Glancing down toward camera with subtle saccade
            gaze_ox, gaze_oy = int(math.sin(local_t * 1.5) * 4), 2
            
        # Draw dynamic pupils / iris glints
        for ec in [left_eye_center, right_eye_center]:
            px = ec[0] + gaze_ox
            py = ec[1] + gaze_oy
            # Deep pupil
            draw_eye.ellipse([px - 14, py - 14, px + 14, py + 14], fill=(12, 18, 28, 230))
            # Wet specular glint
            draw_eye.ellipse([px - 8, py - 10, px - 2, py - 4], fill=(255, 255, 255, 250))
            
        # Eyelid blink at frame 215-223
        if 215 <= frame_idx <= 223:
            blink_p = math.sin((frame_idx - 215) / 8.0 * math.pi)
            lid_drop = int(32 * blink_p)
            for ec in [left_eye_center, right_eye_center]:
                draw_eye.ellipse([ec[0] - 38, ec[1] - 32, ec[0] + 38, ec[1] - 32 + lid_drop * 2], fill=(225, 168, 138, 255))
                draw_eye.arc([ec[0] - 38, ec[1] - 32, ec[0] + 38, ec[1] - 32 + lid_drop * 2], 0, 180, fill=(160, 105, 80, 255), width=3)
                
        eye_layer = eye_layer.filter(ImageFilter.GaussianBlur(radius=2))
        frame = Image.alpha_composite(frame, eye_layer)
        
        # Mouth Viseme Lip-Sync (Frames 165 to 285: "Whatever is powering this place... it knows we are here!")
        if 165 <= frame_idx <= 285:
            mouth_l = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            draw_m = ImageDraw.Draw(mouth_l)
            mouth_c = (WIDTH // 2 - 45, int(HEIGHT * 0.588) - breath)
            
            # Phoneme modulation curve
            viseme_val = abs(math.sin((frame_idx - 165) * 0.42))
            mouth_h = int(viseme_val * 16) + 3
            mouth_w = int(24 + (1.0 - viseme_val) * 8)
            
            # Mouth cavity
            draw_m.ellipse([mouth_c[0] - mouth_w, mouth_c[1] - mouth_h, mouth_c[0] + mouth_w, mouth_c[1] + mouth_h], fill=(85, 25, 20, 240))
            # Subtle upper teeth white edge
            draw_m.line([mouth_c[0] - int(mouth_w * 0.6), mouth_c[1] - mouth_h + 3, mouth_c[0] + int(mouth_w * 0.6), mouth_c[1] - mouth_h + 3], fill=(245, 245, 245, 230), width=3)
            # Lip contours
            draw_m.arc([mouth_c[0] - mouth_w - 4, mouth_c[1] - mouth_h, mouth_c[0] + mouth_w + 4, mouth_c[1] + mouth_h + 4], 0, 180, fill=(195, 120, 105, 240), width=3)
            
            mouth_l = mouth_l.filter(ImageFilter.GaussianBlur(radius=2))
            frame = Image.alpha_composite(frame, mouth_l)
            
        # Hand gripping backpack strap on lower right
        hand_strap = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw_hs = ImageDraw.Draw(hand_strap)
        hx = int(WIDTH * 0.68)
        hy = int(HEIGHT * 0.78) - breath
        # Hand knuckles gripping strap
        draw_hs.ellipse([hx - 35, hy - 25, hx + 35, hy + 25], fill=(235, 175, 145, 240))
        # Thumb resting on strap
        draw_hs.ellipse([hx - 15, hy - 38, hx + 15, hy - 10], fill=(235, 175, 145, 240))
        # Knuckle creases
        draw_hs.line([hx - 20, hy - 5, hx - 20, hy + 15], fill=(185, 120, 95, 200), width=2)
        draw_hs.line([hx, hy - 8, hx, hy + 16], fill=(185, 120, 95, 200), width=2)
        draw_hs.line([hx + 20, hy - 5, hx + 20, hy + 15], fill=(185, 120, 95, 200), width=2)
        hand_strap = hand_strap.filter(ImageFilter.GaussianBlur(radius=2))
        frame = Image.alpha_composite(frame, hand_strap)
        
        # Floating golden dust motes
        random.seed(99)
        motes = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw_mo = ImageDraw.Draw(motes)
        for i in range(30):
            base_x = random.randint(WIDTH // 3, WIDTH - 20)
            y = int((HEIGHT - (local_t * 90 + random.randint(0, HEIGHT))) % HEIGHT)
            drift_x = int(base_x + math.sin(local_t * 2.5 + i) * 18)
            r = random.randint(3, 8)
            draw_mo.ellipse([drift_x - r, y - r, drift_x + r, y + r], fill=(255, 210, 110, 190))
        motes = motes.filter(ImageFilter.GaussianBlur(radius=2))
        frame = Image.alpha_composite(frame, motes)
        
        # Subtitle
        if 165 <= frame_idx <= 290:
            draw_txt = ImageDraw.Draw(frame)
            sub_text = '“Whatever is powering this place... it knows we are here!”'
            pill_w, pill_h = 1000, 110
            pill_x = (WIDTH - pill_w) // 2
            pill_y = HEIGHT - 360
            draw_txt.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=28, fill=(8, 12, 22, 220), outline=(251, 146, 60, 140), width=2)
            draw_txt.text((pill_x + 36, pill_y + 16), "LEO", font=FONT_NAME, fill=(251, 146, 60))
            draw_txt.text((WIDTH // 2, pill_y + 68), sub_text, font=FONT_MAIN, fill=(255, 235, 140), anchor="mm")
            
    return frame.convert("RGB")

if __name__ == "__main__":
    # Test frame 45 (Walking bob), 120 (Hand pointing + LipSync), 180 (Eye looking up), 218 (Blink + hand on strap)
    f45 = create_animated_frame(45)
    f45.save(r"C:\Users\Mr.Scientist\.gemini\antigravity\brain\1ff6e728-5386-415c-b67c-5b2db0481163\anim_test_frame_0045.jpg", quality=95)
    f120 = create_animated_frame(120)
    f120.save(r"C:\Users\Mr.Scientist\.gemini\antigravity\brain\1ff6e728-5386-415c-b67c-5b2db0481163\anim_test_frame_0120.jpg", quality=95)
    f180 = create_animated_frame(180)
    f180.save(r"C:\Users\Mr.Scientist\.gemini\antigravity\brain\1ff6e728-5386-415c-b67c-5b2db0481163\anim_test_frame_0180.jpg", quality=95)
    f218 = create_animated_frame(218)
    f218.save(r"C:\Users\Mr.Scientist\.gemini\antigravity\brain\1ff6e728-5386-415c-b67c-5b2db0481163\anim_test_frame_0218.jpg", quality=95)
    print("All 4 test animation frames generated successfully!")

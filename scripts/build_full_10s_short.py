"""
Autonomous AI Cartoon Studio - Complete 10-Second Cinematic Short Video Pipeline
Generates 300 animated frames (30 fps), mixes master audio, and encodes production MP4.
"""

import math
import os
import subprocess
import time
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont
import imageio_ffmpeg

WIDTH = 1080
HEIGHT = 1920
TOTAL_FRAMES = 300  # Exactly 10.0 seconds at 30 fps
FPS = 30

FONT_PATH = r"C:\Windows\Fonts\arialbd.ttf"
FONT_MAIN = ImageFont.truetype(FONT_PATH, 34)
FONT_NAME = ImageFont.truetype(FONT_PATH, 24)

OUTPUT_FRAMES_DIR = Path(r"E:\YT\output\renders\short_10s")
OUTPUT_FRAMES_DIR.mkdir(parents=True, exist_ok=True)

IMG_SCENE_1 = r"E:\YT\assets\characters\demo_leo_and_lumi_pixar.jpg"
IMG_SCENE_2 = r"E:\YT\assets\characters\char_leo_portrait.jpg"
MASTER_AUDIO = r"E:\YT\assets\audio\demo_short\master_cinematic_audio_10s.wav"
FINAL_VIDEO = r"E:\YT\output\shorts\demo_pixar_short_10s.mp4"
THUMBNAIL_FILE = r"E:\YT\assets\thumbnails\demo_pixar_short_10s_thumb.jpg"

def render_all_frames():
    print(f"[1/3] Generating {TOTAL_FRAMES} high-resolution frames (1080x1920 @ {FPS}fps)...")
    start_time = time.time()
    
    # Pre-load base assets
    src1 = Image.open(IMG_SCENE_1).convert("RGBA")
    src2 = Image.open(IMG_SCENE_2).convert("RGBA")
    
    # Precompute blurred background for Scene 1
    bg_scale = max(WIDTH / src1.width, HEIGHT / src1.height) * 1.15
    bg_w, bg_h = int(src1.width * bg_scale), int(src1.height * bg_scale)
    bg1_base = src1.resize((bg_w, bg_h), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=40))
    bg1_base = ImageEnhance.Brightness(bg1_base).enhance(0.40)
    left = (bg_w - WIDTH) // 2
    top = (bg_h - HEIGHT) // 2
    bg1_cropped = bg1_base.crop((left, top, left + WIDTH, top + HEIGHT))

    for frame_idx in range(TOTAL_FRAMES):
        t = frame_idx / float(FPS)
        
        if frame_idx < 155:
            # --- SCENE 1 (0.0s - 5.17s): Leo & Lumi Crystal Bridge ---
            frame = bg1_cropped.copy()
            
            # Smooth camera dolly-in (zoom 1.0 -> 1.08)
            zoom = 1.0 + 0.08 * (frame_idx / 155.0)
            fg_w = int(WIDTH * zoom)
            fg_h = int((WIDTH / src1.width) * src1.height * zoom)
            fg = src1.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
            
            fg_x = (WIDTH - fg_w) // 2
            fg_y = (HEIGHT - fg_h) // 2 + int(math.sin(t * 1.5) * 4)
            
            # Shadow behind cinema box
            shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            draw_sh = ImageDraw.Draw(shadow)
            draw_sh.rectangle([fg_x - 6, fg_y - 6, fg_x + fg_w + 6, fg_y + fg_h + 6], fill=(0, 0, 0, 180))
            shadow = shadow.filter(ImageFilter.GaussianBlur(radius=24))
            frame.paste(shadow, (0, 0), shadow)
            frame.paste(fg, (fg_x, fg_y), fg)
            
            # Pulsing crystal emission glow
            pulse = 0.5 + 0.5 * math.sin(t * 3.0)
            glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            draw_gl = ImageDraw.Draw(glow)
            glow_alpha = int(35 + 30 * pulse)
            draw_gl.ellipse([WIDTH // 2 - 250, HEIGHT // 2 - 50, WIDTH // 2 + 250, HEIGHT // 2 + 350], fill=(40, 210, 255, glow_alpha))
            glow = glow.filter(ImageFilter.GaussianBlur(radius=60))
            frame = Image.alpha_composite(frame, glow)
            
            # 3D Drifting Bioluminescent Spores
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
            # --- SCENE 2 (5.17s - 10.0s): Leo Close-Up Hero Shot ---
            local_f = frame_idx - 155
            local_t = local_f / float(FPS)
            
            base_scale = max(WIDTH / src2.width, HEIGHT / src2.height) * 1.05
            zoom = base_scale * (1.0 + 0.08 * (local_f / 145.0))
            target_w = int(src2.width * zoom)
            target_h = int(src2.height * zoom)
            scaled = src2.resize((target_w, target_h), Image.Resampling.LANCZOS)
            
            # Breathing movement
            breath = int(math.sin(local_t * math.pi * 1.2) * 5)
            crop_x = (target_w - WIDTH) // 2 + int(math.sin(local_t * 0.8) * 4)
            crop_y = int((target_h - HEIGHT) * 0.35) - breath
            frame = scaled.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
            
            # Floating amber dust motes
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
                
        # Save frame as JPEG
        frame_file = OUTPUT_FRAMES_DIR / f"frame_{frame_idx+1:04d}.jpg"
        frame.convert("RGB").save(frame_file, quality=96)
        
        if (frame_idx + 1) % 50 == 0 or frame_idx == TOTAL_FRAMES - 1:
            print(f"  -> Rendered {frame_idx + 1}/{TOTAL_FRAMES} frames ({((frame_idx+1)/TOTAL_FRAMES)*100:.0f}%)")
            
    print(f"[1/3] Frame rendering completed in {time.time() - start_time:.2f} seconds.")

def encode_video():
    print("[2/3] Encoding 1080x1920 60fps/30fps MP4 with master audio via FFmpeg...")
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    os.makedirs(Path(FINAL_VIDEO).parent, exist_ok=True)
    
    frames_pattern = str(OUTPUT_FRAMES_DIR / "frame_%04d.jpg")
    
    cmd = [
        ffmpeg_exe,
        "-y",
        "-framerate", str(FPS),
        "-i", frames_pattern,
        "-i", MASTER_AUDIO,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-shortest",
        "-movflags", "+faststart",
        FINAL_VIDEO
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg Error:", res.stderr)
        raise RuntimeError("Video encoding failed")
        
    print(f"[2/3] Video successfully encoded: {FINAL_VIDEO}")

def generate_thumbnail():
    print("[3/3] Generating high-CTR YouTube Shorts thumbnail...")
    hero_frame = OUTPUT_FRAMES_DIR / "frame_0200.jpg"
    im = Image.open(hero_frame).convert("RGB")
    
    # High-contrast typography overlay
    draw = ImageDraw.Draw(im)
    title_font = ImageFont.truetype(FONT_PATH, 58)
    sub_font = ImageFont.truetype(FONT_PATH, 32)
    
    # Top badge
    draw.rounded_rectangle([WIDTH // 2 - 240, 160, WIDTH // 2 + 240, 230], radius=20, fill=(239, 68, 68), outline=(255, 255, 255), width=3)
    draw.text((WIDTH // 2, 195), "DANGER UNLOCKED", font=sub_font, fill=(255, 255, 255), anchor="mm")
    
    # Headline text with thick black outline
    headline = "WHO'S WATCHING?!"
    for ox in [-4, 0, 4]:
        for oy in [-4, 0, 4]:
            draw.text((WIDTH // 2 + ox, 310 + oy), headline, font=title_font, fill=(0, 0, 0), anchor="mm")
    draw.text((WIDTH // 2, 310), headline, font=title_font, fill=(255, 235, 59), anchor="mm")
    
    os.makedirs(Path(THUMBNAIL_FILE).parent, exist_ok=True)
    im.save(THUMBNAIL_FILE, quality=95)
    print(f"[3/3] Thumbnail created at: {THUMBNAIL_FILE}")

if __name__ == "__main__":
    render_all_frames()
    encode_video()
    generate_thumbnail()
    print("\n✅ Autonomous 10-Second Short Video Production Completed Successfully!")

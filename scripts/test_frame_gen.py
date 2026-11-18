"""
Refined frame generator for high-end cinematic 10-second Short video.
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

def generate_short_frame(frame_idx, total_frames=300):
    t = frame_idx / 30.0  # seconds
    
    if frame_idx < 155:
        # SCENE 1: Leo & Lumi on Crystal Bridge (0.0s - 5.17s)
        source = Image.open(r"E:\YT\assets\characters\demo_leo_and_lumi_pixar.jpg").convert("RGBA")
        
        # Background: heavily blurred ambient version filling 1080x1920
        bg_scale = max(WIDTH / source.width, HEIGHT / source.height) * 1.15
        bg_w, bg_h = int(source.width * bg_scale), int(source.height * bg_scale)
        bg = source.resize((bg_w, bg_h), Image.Resampling.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(radius=40))
        enhancer = ImageEnhance.Brightness(bg)
        bg = enhancer.enhance(0.40)
        
        left = (bg_w - WIDTH) // 2
        top = (bg_h - HEIGHT) // 2
        frame = bg.crop((left, top, left + WIDTH, top + HEIGHT))
        
        # Foreground: Sharp cinematic widescreen box with slow camera push-in
        zoom = 1.0 + 0.08 * (frame_idx / 155.0)
        fg_w = int(WIDTH * zoom)
        fg_h = int((WIDTH / source.width) * source.height * zoom)
        fg = source.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
        
        fg_x = (WIDTH - fg_w) // 2
        fg_y = (HEIGHT - fg_h) // 2 + int(math.sin(t * 1.5) * 4)
        
        # Soft outer shadow
        shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw_sh = ImageDraw.Draw(shadow)
        draw_sh.rectangle([fg_x - 6, fg_y - 6, fg_x + fg_w + 6, fg_y + fg_h + 6], fill=(0, 0, 0, 180))
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=24))
        frame.paste(shadow, (0, 0), shadow)
        
        # Paste sharp foreground
        frame.paste(fg, (fg_x, fg_y), fg)
        
        # Pulsing crystal glow
        pulse = 0.5 + 0.5 * math.sin(t * 3.0)
        glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw_gl = ImageDraw.Draw(glow)
        glow_alpha = int(35 + 30 * pulse)
        draw_gl.ellipse([WIDTH // 2 - 250, HEIGHT // 2 - 50, WIDTH // 2 + 250, HEIGHT // 2 + 350], fill=(40, 210, 255, glow_alpha))
        glow = glow.filter(ImageFilter.GaussianBlur(radius=60))
        frame = Image.alpha_composite(frame, glow)
        
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
        # SCENE 2: Dramatic Leo Close-Up (5.17s - 10.0s)
        source = Image.open(r"E:\YT\assets\characters\char_leo_portrait.jpg").convert("RGBA")
        local_f = frame_idx - 155
        local_t = local_f / 30.0
        
        # Fullscreen scale filling 1080x1920
        base_scale = max(WIDTH / source.width, HEIGHT / source.height) * 1.05
        zoom = base_scale * (1.0 + 0.08 * (local_f / 145.0))
        target_w = int(source.width * zoom)
        target_h = int(source.height * zoom)
        scaled = source.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Subtle breathing cycle
        breath = int(math.sin(local_t * math.pi * 1.2) * 5)
        
        crop_x = (target_w - WIDTH) // 2 + int(math.sin(local_t * 0.8) * 4)
        crop_y = int((target_h - HEIGHT) * 0.35) - breath
        frame = scaled.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + HEIGHT))
        
        # Floating golden dust motes catching rim light
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
    f1 = generate_short_frame(30)
    f1.save(r"C:\Users\Mr.Scientist\.gemini\antigravity\brain\1ff6e728-5386-415c-b67c-5b2db0481163\test_short_scene_1.jpg", quality=95)
    f2 = generate_short_frame(200)
    f2.save(r"C:\Users\Mr.Scientist\.gemini\antigravity\brain\1ff6e728-5386-415c-b67c-5b2db0481163\test_short_scene_2.jpg", quality=95)
    print("Updated test frames generated!")

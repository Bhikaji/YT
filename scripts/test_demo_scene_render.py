from PIL import Image, ImageDraw, ImageFont
import math, os
from pathlib import Path

def test_render():
    w, h = 1280, 720
    canvas = Image.new("RGBA", (w, h))

    # Test mother speaking frame at t = 3.5s
    t_sec = 3.5
    is_speaking = True
    mouth_open = (math.sin(t_sec * 16.0) > 0)
    
    if is_speaking and mouth_open:
        base_path = "assets/characters/demo_scenes/mother_speaking.png"
    else:
        base_path = "assets/characters/demo_scenes/mother_listening.png"
        
    scene_img = Image.open(base_path).convert("RGBA")
    canvas.paste(scene_img, (0, 0))
    
    # Subtitle
    draw = ImageDraw.Draw(canvas)
    sub_text = "तवा मस्त्या कराल का? माझ्या बापाचं गाव काय?"
    font_path = "C:/Windows/Fonts/Nirmala.ttc"
    font = ImageFont.truetype(font_path, 28)
    bbox = draw.textbbox((0, 0), sub_text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    pad_x, pad_y = 20, 10
    cx = w // 2
    cy = h - 65
    rect = [cx - tw//2 - pad_x, cy - th//2 - pad_y, cx + tw//2 + pad_x, cy + th//2 + pad_y]
    
    draw.rounded_rectangle(rect, radius=12, fill=(15, 23, 42, 235), outline=(234, 179, 8), width=3)
    draw.text((cx - tw//2, cy - th//2 - 2), sub_text, fill=(255, 255, 255), font=font)
    
    out_p = "output/test_perfect_demo_frame.png"
    canvas.save(out_p)
    print("Saved", out_p)

test_render()

import os
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter

class ThumbnailGenerator:
    """Generates high-CTR 3D cartoon thumbnails with bold text overlays."""

    @classmethod
    def create_thumbnail(
        cls,
        base_frame_path: str,
        output_thumbnail_path: str,
        headline_text: str = "WHAT IS IN THERE?!",
        emotion_tag: str = "SHOCK",
        format_type: str = "SHORT"  # SHORT (9:16) or LONG (16:9)
    ) -> str:
        """
        Creates a high-contrast YouTube thumbnail.
        """
        os.makedirs(Path(output_thumbnail_path).parent, exist_ok=True)
        base_img = Image.open(base_frame_path).convert("RGBA")
        
        # Long-form standard 1280x720 or Shorts 1080x1920
        target_size = (1080, 1920) if format_type == "SHORT" else (1280, 720)
        img = base_img.resize(target_size, Image.Resampling.LANCZOS)
        
        # 1. Color punch enhancement (boost contrast & saturation slightly)
        overlay = Image.new("RGBA", target_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Vignette around edges to focus center character
        w, h = target_size
        draw.rectangle([(0, 0), (w, 80)], fill=(0, 0, 0, 80))
        draw.rectangle([(0, h - 220), (w, h)], fill=(0, 0, 0, 160))
        
        # 2. Draw High-Impact Outlined Headline
        font_size = int(w * 0.08)
        try:
            # Fallback to default or standard Windows font
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Center text horizontally near bottom or top
        text_y = int(h * 0.82)
        
        # Draw outline (stroke) for high legibility against any background
        stroke_color = (0, 0, 0, 255)
        text_color = (255, 220, 0, 255) if emotion_tag == "SHOCK" else (255, 60, 60, 255)
        
        # Simple multi-directional stroke
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                draw.text((w // 2 + dx, text_y + dy), headline_text, font=font, fill=stroke_color, anchor="mm")
                
        # Main text
        draw.text((w // 2, text_y), headline_text, font=font, fill=text_color, anchor="mm")

        # Composite & save as JPG/PNG
        final_thumb = Image.alpha_composite(img, overlay).convert("RGB")
        final_thumb.save(output_thumbnail_path, "JPEG", quality=95)
        return output_thumbnail_path

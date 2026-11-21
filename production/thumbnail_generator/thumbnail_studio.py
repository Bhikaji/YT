from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Dict, Any, List

class StickThumbnailStudio:
    """
    Dedicated AI Thumbnail Studio for 2D Stick-Figure YouTube Shorts.
    Generates 3 vertical (1080x1920) thumbnail concepts with bold typography,
    expressive character poses, and high-contrast color palettes.
    """

    CONCEPTS = [
        {"bg": (239, 68, 68), "banner": "DON'T DO THIS!", "tag": "SHOCKING TRUTH", "accent": (250, 204, 21)},
        {"bg": (37, 99, 235), "banner": "THE SECRET REVEALED!", "tag": "HOW IT WORKS", "accent": (56, 189, 248)},
        {"bg": (15, 23, 42), "banner": "100% A LIE?!", "tag": "MUST WATCH", "accent": (234, 179, 8)}
    ]

    @classmethod
    def generate_thumbnails(
        cls,
        topic: str,
        hero_frame_path: Path,
        output_dir: Path,
        width: int = 1080,
        height: int = 1920
    ) -> Dict[str, Any]:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        results = []

        base_img = None
        if hero_frame_path and Path(hero_frame_path).exists():
            base_img = Image.open(hero_frame_path).convert("RGBA")

        for idx, c in enumerate(cls.CONCEPTS):
            thumb = Image.new("RGBA", (width, height), c["bg"])
            draw = ImageDraw.Draw(thumb)

            if base_img:
                # Composite character from hero frame with slight enlargement
                resized_hero = base_img.resize((width, height))
                thumb.alpha_composite(resized_hero)
                draw = ImageDraw.Draw(thumb)

            # Dramatic Top Badge
            draw.rounded_rectangle([60, 100, 1020, 240], radius=24, fill=(15, 23, 42, 240), outline=c["accent"], width=6)
            draw.text((width/2 - 240, 140), c["tag"], fill=c["accent"])

            # High-CTR Bold Headline Banner
            draw.rounded_rectangle([60, 1450, 1020, 1750], radius=32, fill=(0, 0, 0, 230), outline=(255, 255, 255), width=8)
            draw.text((width/2 - 280, 1500), c["banner"], fill=(255, 255, 255))
            
            clean_sub = (topic[:35] + "...") if len(topic) > 35 else topic
            draw.text((width/2 - 280, 1620), clean_sub.upper(), fill=c["accent"])

            out_path = output_dir / f"thumb_concept_{idx+1}.jpg"
            thumb.convert("RGB").save(out_path, quality=95)
            results.append(str(out_path))

        # Select best concept (concept 1 by default for highest contrast)
        return {
            "selected_thumbnail": results[0],
            "all_concepts": results
        }

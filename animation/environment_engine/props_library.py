from PIL import Image, ImageDraw
import math

class PropsLibrary:
    """
    Renders 2D cartoon props that stick figures hold and interact with.
    """

    @classmethod
    def draw_prop(cls, draw: ImageDraw.ImageDraw, prop_name: str, x: float, y: float, scale: float = 1.0):
        name = prop_name.lower()

        if "phone" in name or "smartphone" in name:
            # Modern smartphone
            w, h = 32 * scale, 56 * scale
            draw.rounded_rectangle([x - w/2, y - h/2, x + w/2, y + h/2], radius=6*scale, fill=(15, 23, 42), outline=(51, 65, 85), width=int(2*scale))
            # Screen glowing cyan
            draw.rounded_rectangle([x - w/2 + 3*scale, y - h/2 + 6*scale, x + w/2 - 3*scale, y + h/2 - 6*scale], radius=3*scale, fill=(56, 189, 248))
            # Notification icon
            draw.ellipse([x - 4*scale, y - 8*scale, x + 4*scale, y], fill=(239, 68, 68))

        elif "tube" in name or "potion" in name:
            # Science test tube
            w, h = 16 * scale, 50 * scale
            draw.rounded_rectangle([x - w/2, y - h/2, x + w/2, y + h/2], radius=8*scale, fill=(241, 245, 249, 150), outline=(14, 165, 233), width=int(2*scale))
            # Green bubbling chemical
            draw.rounded_rectangle([x - w/2 + 2*scale, y, x + w/2 - 2*scale, y + h/2 - 2*scale], radius=6*scale, fill=(16, 185, 129))

        elif "coffee" in name or "mug" in name:
            # Coffee mug
            w, h = 30 * scale, 34 * scale
            draw.rectangle([x - w/2, y - h/2, x + w/2, y + h/2], fill=(255, 255, 255), outline=(30, 41, 59), width=int(2*scale))
            # Handle
            draw.arc([x + w/2 - 4*scale, y - h/4, x + w/2 + 12*scale, y + h/4], 270, 90, fill=(30, 41, 59), width=int(3*scale))
            # Steam squiggles
            draw.line([(x - 4*scale, y - h/2 - 4*scale), (x - 2*scale, y - h/2 - 14*scale)], fill=(148, 163, 184), width=int(2*scale))
            draw.line([(x + 4*scale, y - h/2 - 4*scale), (x + 6*scale, y - h/2 - 16*scale)], fill=(148, 163, 184), width=int(2*scale))

        elif "money" in name or "dollar" in name:
            # Money bag
            r = 24 * scale
            draw.ellipse([x - r, y - r/2, x + r, y + r*1.2], fill=(234, 179, 8), outline=(161, 98, 7), width=int(2*scale))
            # Tie at top
            draw.polygon([(x - 8*scale, y - r/2), (x + 8*scale, y - r/2), (x, y - r)], fill=(161, 98, 7))
            draw.text((x - 6*scale, y), "$", fill=(113, 63, 18))

        elif "laptop" in name:
            # Open laptop
            w, h = 60 * scale, 40 * scale
            # Screen
            draw.rectangle([x - w/2, y - h, x + w/2, y], fill=(30, 41, 59), outline=(100, 116, 139), width=int(2*scale))
            draw.rectangle([x - w/2 + 4*scale, y - h + 4*scale, x + w/2 - 4*scale, y - 4*scale], fill=(59, 130, 246))
            # Base
            draw.polygon([(x - w/2 - 8*scale, y + 8*scale), (x + w/2 + 8*scale, y + 8*scale), (x + w/2, y), (x - w/2, y)], fill=(71, 85, 105))

        else:
            # Generic tablet/clipboard
            w, h = 36 * scale, 48 * scale
            draw.rectangle([x - w/2, y - h/2, x + w/2, y + h/2], fill=(241, 245, 249), outline=(30, 41, 59), width=int(2*scale))

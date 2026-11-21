from PIL import Image, ImageDraw
import math

class VisualEffectsEngine:
    """
    Renders expressive cartoon overlays:
    - Speed lines / Impact bursts
    - Question marks (?) above head for confusion
    - Exclamation marks (!) for shock
    - Lightbulb for revelation / payoff idea
    - Sweat drops for panic / tension
    - Anger cross / popping vein mark
    """

    @classmethod
    def draw_effects(
        cls,
        draw: ImageDraw.ImageDraw,
        effect_name: str,
        x: float,
        y: float,
        t_sec: float,
        scale: float = 1.0
    ):
        eff = effect_name.lower()

        if "sweat" in eff:
            # Blue teardrop sweat bead
            sw_x, sw_y = x + 35 * scale, y - 25 * scale
            draw.polygon([(sw_x, sw_y - 12*scale), (sw_x - 7*scale, sw_y + 4*scale), (sw_x + 7*scale, sw_y + 4*scale)], fill=(56, 189, 248))
            draw.ellipse([sw_x - 7*scale, sw_y - 2*scale, sw_x + 7*scale, sw_y + 10*scale], fill=(56, 189, 248))

        elif "question" in eff:
            # Floating yellow/orange question mark
            qx, qy = x + 25 * scale, y - 60 * scale - math.sin(t_sec * 6.0) * 8.0
            draw.arc([qx - 10*scale, qy - 20*scale, qx + 10*scale, qy], 180, 0, fill=(234, 179, 8), width=int(4*scale))
            draw.line([(qx + 10*scale, qy - 10*scale), (qx, qy + 5*scale)], fill=(234, 179, 8), width=int(4*scale))
            draw.ellipse([qx - 3*scale, qy + 12*scale, qx + 3*scale, qy + 18*scale], fill=(234, 179, 8))

        elif "lightbulb" in eff or "idea" in eff:
            # Golden glowing lightbulb
            bx, by = x, y - 75 * scale
            draw.ellipse([bx - 16*scale, by - 24*scale, bx + 16*scale, by + 8*scale], fill=(250, 204, 21), outline=(202, 138, 4), width=int(2*scale))
            draw.rectangle([bx - 8*scale, by + 8*scale, bx + 8*scale, by + 18*scale], fill=(148, 163, 184))
            # Radiating glow rays
            for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
                rad = math.radians(angle)
                r1, r2 = 22 * scale, 32 * scale
                draw.line([(bx + r1*math.cos(rad), by - 8*scale + r1*math.sin(rad)),
                           (bx + r2*math.cos(rad), by - 8*scale + r2*math.sin(rad))], fill=(250, 204, 21), width=int(2*scale))

        elif "anger" in eff:
            # Red popping vein cross
            ax, ay = x - 35 * scale, y - 25 * scale
            draw.arc([ax - 12*scale, ay - 12*scale, ax + 12*scale, ay + 12*scale], 0, 90, fill=(239, 68, 68), width=int(3*scale))
            draw.arc([ax - 12*scale, ay - 12*scale, ax + 12*scale, ay + 12*scale], 180, 270, fill=(239, 68, 68), width=int(3*scale))
            draw.arc([ax - 12*scale, ay - 12*scale, ax + 12*scale, ay + 12*scale], 90, 180, fill=(239, 68, 68), width=int(3*scale))
            draw.arc([ax - 12*scale, ay - 12*scale, ax + 12*scale, ay + 12*scale], 270, 360, fill=(239, 68, 68), width=int(3*scale))

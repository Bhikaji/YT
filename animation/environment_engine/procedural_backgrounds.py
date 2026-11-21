from PIL import Image, ImageDraw, ImageFont
import math

class ProceduralBackgroundRenderer:
    """
    Renders clean, vibrant 2D vector-style backgrounds for vertical (1080x1920) Shorts.
    Supports science lab, modern office, classroom, tech showroom, space station, retail shop, living room.
    """

    @classmethod
    def render_environment(cls, env_type: str, width: int = 1080, height: int = 1920, t_sec: float = 0.0) -> Image.Image:
        img = Image.new("RGBA", (width, height), (248, 250, 252, 255))
        draw = ImageDraw.Draw(img)

        env = env_type.lower()
        if "lab" in env:
            cls._draw_science_lab(draw, width, height, t_sec)
        elif "office" in env:
            cls._draw_modern_office(draw, width, height, t_sec)
        elif "class" in env:
            cls._draw_classroom(draw, width, height, t_sec)
        elif "tech" in env or "gadget" in env:
            cls._draw_tech_showroom(draw, width, height, t_sec)
        elif "space" in env:
            cls._draw_space_station(draw, width, height, t_sec)
        elif "shop" in env or "retail" in env or "mall" in env:
            cls._draw_retail_shop(draw, width, height, t_sec)
        else:
            cls._draw_modern_office(draw, width, height, t_sec)

        return img

    @classmethod
    def _draw_science_lab(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        floor_y = int(h * 0.68)
        table_y = int(h * 0.60)
        # Wall: Clean high-tech teal/cyan
        draw.rectangle([0, 0, w, floor_y], fill=(230, 245, 248))
        # Floor: Checkered lab tile
        draw.rectangle([0, floor_y, w, h], fill=(203, 213, 225))
        # Floor grid lines
        for y in range(floor_y, h, 60):
            draw.line([(0, y), (w, y)], fill=(148, 163, 184), width=2)
        for x in range(0, w, 120):
            draw.line([(x, floor_y), (x, h)], fill=(148, 163, 184), width=2)

        # Periodic Table / Whiteboard on back wall
        wb_top = int(h * 0.13)
        wb_bot = int(h * 0.36)
        draw.rectangle([int(w*0.15), wb_top, int(w*0.85), wb_bot], fill=(255, 255, 255), outline=(100, 116, 139), width=5)
        draw.text((int(w*0.2), wb_top + 20), "QUANTUM RESEARCH LAB - 2026", fill=(30, 41, 59))
        draw.rectangle([int(w*0.2), wb_top + 60, int(w*0.8), wb_bot - 20], fill=(241, 245, 249), outline=(148, 163, 184), width=2)
        draw.text((int(w*0.23), wb_top + 80), "H2O + AI -> Discovery", fill=(15, 118, 110))
        draw.text((int(w*0.23), wb_top + 130), "E = mc^2  [VERIFIED]", fill=(3, 105, 161))

        # Lab bench table in background
        draw.rectangle([int(w*0.08), table_y, int(w*0.92), floor_y + 20], fill=(71, 85, 105))
        draw.rectangle([int(w*0.06), table_y - 20, int(w*0.94), table_y], fill=(15, 23, 42))

        # Bubbling Flask on table
        bubble_y = math.sin(t_sec * 5.0) * 8.0
        flask_x = int(w * 0.2)
        draw.polygon([(flask_x, table_y), (flask_x+60, table_y), (flask_x+40, table_y-80), (flask_x+20, table_y-80)], fill=(56, 189, 248, 180), outline=(14, 165, 233), width=3)
        draw.ellipse([flask_x+5, table_y-50, flask_x+55, table_y], fill=(16, 185, 129, 200))
        draw.ellipse([flask_x+25, table_y-60 + bubble_y, flask_x+35, table_y-50 + bubble_y], fill=(255, 255, 255))

        # Microscope on table
        mic_x = int(w * 0.78)
        draw.rectangle([mic_x+20, table_y-70, mic_x+40, table_y], fill=(30, 41, 59))
        draw.ellipse([mic_x, table_y-100, mic_x+60, table_y-60], fill=(15, 23, 42))
        draw.rectangle([mic_x-10, table_y-5, mic_x+70, table_y+5], fill=(100, 116, 139))

    @classmethod
    def _draw_modern_office(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        floor_y = int(h * 0.68)
        # Wall: Soft warm grey
        draw.rectangle([0, 0, w, floor_y], fill=(241, 245, 249))
        # Carpet: Slate blue
        draw.rectangle([0, floor_y, w, h], fill=(226, 232, 240))
        draw.line([(0, floor_y), (w, floor_y)], fill=(148, 163, 184), width=4)

        # Whiteboard on wall with growth chart
        wb_top = int(h * 0.12)
        wb_bot = int(h * 0.35)
        draw.rectangle([int(w*0.13), wb_top, int(w*0.87), wb_bot], fill=(255, 255, 255), outline=(100, 116, 139), width=6)
        draw.text((int(w*0.17), wb_top + 20), "Q4 VIRAL SHORTS GROWTH METRICS", fill=(30, 41, 59))
        # Growth graph
        points = [
            (int(w*0.2), wb_bot - 40),
            (int(w*0.35), wb_bot - 80),
            (int(w*0.5), wb_bot - 140),
            (int(w*0.68), wb_bot - 110),
            (int(w*0.82), wb_bot - 220)
        ]
        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill=(16, 185, 129), width=6)
            draw.ellipse([points[i][0]-8, points[i][1]-8, points[i][0]+8, points[i][1]+8], fill=(5, 150, 105))
        draw.ellipse([points[-1][0]-8, points[-1][1]-8, points[-1][0]+8, points[-1][1]+8], fill=(239, 68, 68))

        # Wall Clock with animated second hand
        draw.ellipse([int(w*0.06), int(h*0.04), int(w*0.16), int(h*0.09)], fill=(255, 255, 255), outline=(30, 41, 59), width=4)
        sec_angle = t_sec * 6.0 * (math.pi / 180.0)
        cx, cy = int(w * 0.11), int(h * 0.065)
        draw.line([(cx, cy), (cx + 25 * math.sin(sec_angle), cy - 25 * math.cos(sec_angle))], fill=(239, 68, 68), width=2)

        # Office desk
        desk_y = int(h * 0.61)
        draw.rectangle([int(w*0.1), desk_y + 20, int(w*0.9), floor_y + 10], fill=(168, 85, 247, 50), outline=(120, 113, 108), width=3)
        draw.rectangle([int(w*0.08), desk_y, int(w*0.92), desk_y + 30], fill=(120, 113, 108))

    @classmethod
    def _draw_classroom(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        floor_y = int(h * 0.68)
        draw.rectangle([0, 0, w, floor_y], fill=(254, 243, 199))
        draw.rectangle([0, floor_y, w, h], fill=(217, 119, 6))
        # Giant chalkboard
        draw.rectangle([int(w*0.1), int(h*0.1), int(w*0.9), int(h*0.38)], fill=(22, 101, 52), outline=(180, 83, 9), width=8)
        draw.text((int(w*0.14), int(h*0.12)), "TODAY'S LESSON: THE TRUTH REVEALED", fill=(254, 240, 138))
        draw.text((int(w*0.14), int(h*0.18)), "1. Misconception vs Reality", fill=(255, 255, 255))
        draw.text((int(w*0.14), int(h*0.23)), "2. The Hidden Formula: Success = Focus x 10", fill=(255, 255, 255))
        draw.text((int(w*0.14), int(h*0.28)), "3. Pay attention to the ending!", fill=(252, 211, 77))

    @classmethod
    def _draw_tech_showroom(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        # Cyber dark theme
        draw.rectangle([0, 0, w, h], fill=(10, 15, 30))
        # Neon grid lines on floor
        for y in range(1250, h, 50):
            draw.line([(0, y), (w, y)], fill=(6, 182, 212, 120), width=2)
        for x in range(0, w, 90):
            draw.line([(x, 1250), (x, h)], fill=(147, 51, 234, 100), width=2)
        # Hologram pedestal
        pulse = abs(math.sin(t_sec * 3.0)) * 40
        draw.ellipse([440, 1200, 640, 1270], fill=(6, 182, 212, 180), outline=(56, 189, 248), width=3)
        draw.rectangle([530, 850, 550, 1210], fill=(6, 182, 212, 100))
        # Floating holo cube
        draw.rectangle([480 - pulse/4, 900 - pulse/2, 600 + pulse/4, 1020 + pulse/2], outline=(168, 85, 247), width=3)
        draw.text((360, 300), "FUTURE TECHNOLOGY LAB", fill=(6, 182, 212))

    @classmethod
    def _draw_space_station(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        # Deep space window
        draw.rectangle([0, 0, w, h], fill=(3, 7, 18))
        # Twinkling stars
        for i in range(60):
            sx = (i * 97) % w
            sy = (i * 131) % 1200
            sz = 2 if (i + int(t_sec * 3)) % 3 == 0 else 1
            draw.rectangle([sx, sy, sx+sz, sy+sz], fill=(255, 255, 255))
        # Big alien planet in viewport
        draw.ellipse([700, 150, 1020, 470], fill=(168, 85, 247), outline=(236, 72, 153), width=4)
        draw.arc([660, 270, 1060, 350], 0, 360, fill=(244, 114, 182), width=6)
        # Station interior frame
        draw.rectangle([0, 1250, w, h], fill=(30, 41, 59))
        draw.rectangle([0, 0, 100, h], fill=(15, 23, 42))
        draw.rectangle([w-100, 0, w, h], fill=(15, 23, 42))
        draw.rectangle([0, 0, w, 100], fill=(15, 23, 42))

    @classmethod
    def _draw_retail_shop(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        draw.rectangle([0, 0, w, 1250], fill=(255, 251, 235))
        draw.rectangle([0, 1250, w, h], fill=(241, 245, 249))
        # Store shelf with products
        draw.rectangle([80, 300, 1000, 1150], fill=(254, 215, 170), outline=(194, 65, 12), width=4)
        for y in [550, 850, 1150]:
            draw.line([(80, y), (1000, y)], fill=(154, 52, 18), width=8)
            # Products on shelves
            for px in range(120, 960, 90):
                color = (239, 68, 68) if px % 180 == 0 else (59, 130, 246)
                draw.rectangle([px, y - 90, px + 65, y - 5], fill=color, outline=(30, 41, 59), width=2)
        # SALE banner
        draw.rectangle([340, 140, 740, 240], fill=(239, 68, 68), outline=(255, 255, 255), width=4)
        draw.text((380, 170), "SPECIAL 50% OFF SALE!", fill=(255, 255, 255))

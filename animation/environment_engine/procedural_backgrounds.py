from PIL import Image, ImageDraw, ImageFont
import math

class ProceduralBackgroundRenderer:
    """
    Renders clean, vibrant 2D vector-style backgrounds for vertical (1080x1920) Shorts.
    Supports authentic Village Katta (गावचा कट्टा / चावडी), science lab, modern office,
    classroom, tech showroom, space station, and retail shop.
    Guarantees ZERO English prompt leaks or text in any environment.
    """

    @classmethod
    def render_environment(cls, env_type: str, width: int = 1080, height: int = 1920, t_sec: float = 0.0) -> Image.Image:
        img = Image.new("RGBA", (width, height), (248, 250, 252, 255))
        draw = ImageDraw.Draw(img)

        env = env_type.lower()
        if any(k in env for k in ["village", "katta", "chawadi", "rural", "gav", "outdoor", "park"]):
            cls._draw_village_katta(draw, width, height, t_sec)
        elif "lab" in env:
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
            cls._draw_village_katta(draw, width, height, t_sec)

        return img

    @classmethod
    def _draw_village_katta(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        """
        Vibrant, authentic Maharashtrian Village Square (गावाकडचा पार / कट्टा / चावडी).
        Features sunny sky, banyan/neem tree shade, rustic stone sitting deck, cutting chai glasses.
        """
        # 1. Warm Daytime Sky Gradient
        horizon_y = int(h * 0.64)
        for y in range(0, horizon_y, 4):
            r = int(186 + (240 - 186) * (y / horizon_y))
            g = int(230 + (249 - 230) * (y / horizon_y))
            b = int(253 + (255 - 253) * (y / horizon_y))
            draw.line([(0, y), (w, y)], fill=(r, g, b), width=4)

        # 2. Warm Village Sun with Soft Glow
        sun_cx, sun_cy = int(w * 0.82), int(h * 0.16)
        draw.ellipse([sun_cx - 90, sun_cy - 90, sun_cx + 90, sun_cy + 90], fill=(254, 240, 138, 90))
        draw.ellipse([sun_cx - 65, sun_cy - 65, sun_cx + 65, sun_cy + 65], fill=(253, 224, 71, 150))
        draw.ellipse([sun_cx - 45, sun_cy - 45, sun_cx + 45, sun_cy + 45], fill=(251, 191, 36))

        # Fluffy Cartoon Clouds
        for cx, cy in [(int(w * 0.22), int(h * 0.14)), (int(w * 0.55), int(h * 0.22))]:
            draw.ellipse([cx - 70, cy - 25, cx + 70, cy + 25], fill=(255, 255, 255, 230))
            draw.ellipse([cx - 40, cy - 45, cx + 25, cy + 20], fill=(255, 255, 255, 240))
            draw.ellipse([cx - 10, cy - 35, cx + 55, cy + 20], fill=(255, 255, 255, 240))

        # 3. Distant Rolling Green Sahyadri Hills Silhouette
        hill_points = [
            (0, horizon_y),
            (int(w * 0.25), int(horizon_y * 0.88)),
            (int(w * 0.55), int(horizon_y * 0.94)),
            (int(w * 0.85), int(horizon_y * 0.85)),
            (w, horizon_y)
        ]
        draw.polygon(hill_points, fill=(187, 215, 172))
        draw.line([(0, horizon_y), (w, horizon_y)], fill=(163, 190, 140), width=3)

        # 4. Warm Rustic Village Soil Ground
        ground_y = horizon_y
        draw.rectangle([0, ground_y, w, h], fill=(245, 236, 215))

        # Ground texture paths
        draw.line([(0, ground_y + 120), (w, ground_y + 80)], fill=(234, 216, 185), width=6)
        draw.line([(0, ground_y + 280), (w, ground_y + 320)], fill=(234, 216, 185), width=8)

        # 5. Raised Village Stone Platform (चावडीचा कट्टा / पार)
        # Characters stand at y=1380 with feet at y=1535.
        katta_top = 1260
        katta_bot = 1680
        draw.rectangle([int(w * 0.05), katta_top, int(w * 0.95), katta_bot], fill=(226, 232, 240), outline=(148, 163, 184), width=5)

        # Stone slab top coping (smooth sitting ledge)
        draw.rectangle([int(w * 0.03), katta_top - 20, int(w * 0.97), katta_top], fill=(203, 213, 225), outline=(100, 116, 139), width=4)

        # Rustic stone masonry courses
        for sy in range(katta_top + 70, katta_bot, 70):
            draw.line([(int(w * 0.05), sy), (int(w * 0.95), sy)], fill=(148, 163, 184), width=3)
            # Staggered vertical stone joints
            offset = 40 if (sy // 70) % 2 == 0 else 0
            for sx in range(int(w * 0.1) + offset, int(w * 0.9), 110):
                draw.line([(sx, sy - 70), (sx, sy)], fill=(148, 163, 184), width=2)

        # 6. Majestic Village Banyan Tree (डावीकडचा वड / पिंपळ)
        # Strong rustic brown trunk on the left border
        draw.polygon([
            (-40, katta_top), (140, katta_top),
            (90, 0), (-40, 0)
        ], fill=(120, 80, 50), outline=(85, 55, 30), width=5)

        # Sprawling green canopy branches spreading across top
        draw.ellipse([-80, -60, 480, 280], fill=(34, 197, 94, 245), outline=(22, 163, 74), width=6)
        draw.ellipse([260, -40, 720, 220], fill=(22, 163, 74, 235), outline=(21, 128, 61), width=5)
        draw.ellipse([540, -50, 1050, 200], fill=(34, 197, 94, 235), outline=(22, 163, 74), width=5)
        draw.ellipse([820, -40, 1160, 240], fill=(22, 163, 74, 245), outline=(21, 128, 61), width=6)

        # Hanging aerial roots (वडाच्या पारंब्या)
        for rx, r_len in [(180, 220), (320, 180), (460, 140)]:
            draw.line([(rx, 140), (rx + 10, 140 + r_len)], fill=(101, 67, 33), width=4)

        # 7. Tea Kettle & Glasses on Katta Edge (गावातली चहाची किटली)
        bench_x = int(w * 0.12)
        bench_y = katta_top - 20
        # Copper Kettle
        draw.polygon([(bench_x, bench_y), (bench_x + 50, bench_y), (bench_x + 40, bench_y - 60), (bench_x + 10, bench_y - 60)], fill=(217, 119, 6), outline=(180, 83, 9), width=3)
        draw.ellipse([bench_x + 10, bench_y - 70, bench_x + 40, bench_y - 50], fill=(245, 158, 11), outline=(180, 83, 9), width=2)
        # Cutting chai glass
        draw.polygon([(bench_x + 65, bench_y), (bench_x + 85, bench_y), (bench_x + 90, bench_y - 35), (bench_x + 60, bench_y - 35)], fill=(254, 243, 199), outline=(100, 116, 139), width=2)
        draw.rectangle([bench_x + 63, bench_y - 25, bench_x + 87, bench_y - 5], fill=(217, 119, 6))

    @classmethod
    def _draw_science_lab(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        floor_y = int(h * 0.68)
        table_y = int(h * 0.60)
        draw.rectangle([0, 0, w, floor_y], fill=(230, 245, 248))
        draw.rectangle([0, floor_y, w, h], fill=(203, 213, 225))
        for y in range(floor_y, h, 60):
            draw.line([(0, y), (w, y)], fill=(148, 163, 184), width=2)
        for x in range(0, w, 120):
            draw.line([(x, floor_y), (x, h)], fill=(148, 163, 184), width=2)

        wb_top = int(h * 0.13)
        wb_bot = int(h * 0.36)
        draw.rectangle([int(w*0.15), wb_top, int(w*0.85), wb_bot], fill=(255, 255, 255), outline=(100, 116, 139), width=5)
        # Graphical atom icon on board instead of text
        acx, acy = int(w * 0.5), (wb_top + wb_bot) // 2
        draw.ellipse([acx - 60, acy - 25, acx + 60, acy + 25], outline=(14, 165, 233), width=3)
        draw.ellipse([acx - 25, acy - 60, acx + 25, acy + 60], outline=(16, 185, 129), width=3)
        draw.ellipse([acx - 14, acy - 14, acx + 14, acy + 14], fill=(239, 68, 68))

        draw.rectangle([int(w*0.08), table_y, int(w*0.92), floor_y + 20], fill=(71, 85, 105))
        draw.rectangle([int(w*0.06), table_y - 20, int(w*0.94), table_y], fill=(15, 23, 42))

        bubble_y = math.sin(t_sec * 5.0) * 8.0
        flask_x = int(w * 0.2)
        draw.polygon([(flask_x, table_y), (flask_x+60, table_y), (flask_x+40, table_y-80), (flask_x+20, table_y-80)], fill=(56, 189, 248, 180), outline=(14, 165, 233), width=3)
        draw.ellipse([flask_x+5, table_y-50, flask_x+55, table_y], fill=(16, 185, 129, 200))
        draw.ellipse([flask_x+25, table_y-60 + bubble_y, flask_x+35, table_y-50 + bubble_y], fill=(255, 255, 255))

        mic_x = int(w * 0.78)
        draw.rectangle([mic_x+20, table_y-70, mic_x+40, table_y], fill=(30, 41, 59))
        draw.ellipse([mic_x, table_y-100, mic_x+60, table_y-60], fill=(15, 23, 42))
        draw.rectangle([mic_x-10, table_y-5, mic_x+70, table_y+5], fill=(100, 116, 139))

    @classmethod
    def _draw_modern_office(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        floor_y = int(h * 0.68)
        draw.rectangle([0, 0, w, floor_y], fill=(241, 245, 249))
        draw.rectangle([0, floor_y, w, h], fill=(226, 232, 240))
        draw.line([(0, floor_y), (w, floor_y)], fill=(148, 163, 184), width=4)

        wb_top = int(h * 0.12)
        wb_bot = int(h * 0.35)
        draw.rectangle([int(w*0.13), wb_top, int(w*0.87), wb_bot], fill=(255, 255, 255), outline=(100, 116, 139), width=6)
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

        draw.ellipse([int(w*0.06), int(h*0.04), int(w*0.16), int(h*0.09)], fill=(255, 255, 255), outline=(30, 41, 59), width=4)
        sec_angle = t_sec * 6.0 * (math.pi / 180.0)
        cx, cy = int(w * 0.11), int(h * 0.065)
        draw.line([(cx, cy), (cx + 25 * math.sin(sec_angle), cy - 25 * math.cos(sec_angle))], fill=(239, 68, 68), width=2)

        desk_y = int(h * 0.61)
        draw.rectangle([int(w*0.1), desk_y + 20, int(w*0.9), floor_y + 10], fill=(168, 85, 247, 50), outline=(120, 113, 108), width=3)
        draw.rectangle([int(w*0.08), desk_y, int(w*0.92), desk_y + 30], fill=(120, 113, 108))

    @classmethod
    def _draw_classroom(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        floor_y = int(h * 0.68)
        draw.rectangle([0, 0, w, floor_y], fill=(254, 243, 199))
        draw.rectangle([0, floor_y, w, h], fill=(217, 119, 6))
        draw.rectangle([int(w*0.1), int(h*0.1), int(w*0.9), int(h*0.38)], fill=(22, 101, 52), outline=(180, 83, 9), width=8)
        # Clean geometric chalk diagrams instead of text
        draw.polygon([(int(w*0.25), int(h*0.32)), (int(w*0.45), int(h*0.32)), (int(w*0.35), int(h*0.16))], outline=(254, 240, 138), width=4)
        draw.ellipse([int(w*0.6), int(h*0.16), int(w*0.75), int(h*0.32)], outline=(255, 255, 255), width=4)

    @classmethod
    def _draw_tech_showroom(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        draw.rectangle([0, 0, w, h], fill=(15, 23, 42))

        for x_edge in [30, w - 30]:
            draw.rectangle([x_edge - 6, 80, x_edge + 6, h - 80], fill=(14, 165, 233, 180), outline=(56, 189, 248), width=2)
            draw.line([(x_edge, 80), (x_edge, h - 80)], fill=(255, 255, 255), width=2)

        ped_x = w // 2
        stage_cy = 1420
        stage_rx = int(w * 0.44)
        stage_ry = 210

        draw.polygon([
            (int(w * 0.35), 0), (int(w * 0.65), 0),
            (ped_x + stage_rx, stage_cy), (ped_x - stage_rx, stage_cy)
        ], fill=(30, 58, 138, 55))

        draw.ellipse([ped_x - stage_rx - 14, stage_cy - stage_ry - 14, ped_x + stage_rx + 14, stage_cy + stage_ry + 14], fill=(14, 165, 233, 130))
        draw.ellipse([ped_x - stage_rx, stage_cy - stage_ry, ped_x + stage_rx, stage_cy + stage_ry], fill=(240, 249, 255), outline=(56, 189, 248), width=6)
        draw.ellipse([ped_x - stage_rx + 35, stage_cy - stage_ry + 18, ped_x + stage_rx - 35, stage_cy + stage_ry - 18], outline=(186, 230, 253), width=3)

    @classmethod
    def _draw_space_station(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        draw.rectangle([0, 0, w, h], fill=(3, 7, 18))
        for i in range(60):
            sx = (i * 97) % w
            sy = (i * 131) % 1200
            sz = 2 if (i + int(t_sec * 3)) % 3 == 0 else 1
            draw.rectangle([sx, sy, sx+sz, sy+sz], fill=(255, 255, 255))
        draw.ellipse([700, 150, 1020, 470], fill=(168, 85, 247), outline=(236, 72, 153), width=4)
        draw.arc([660, 270, 1060, 350], 0, 360, fill=(244, 114, 182), width=6)
        floor_y = int(h * 0.65)
        draw.rectangle([0, floor_y, w, h], fill=(226, 232, 240))
        draw.rectangle([0, floor_y, w, floor_y + 16], fill=(14, 165, 233))
        draw.rectangle([int(w * 0.1), floor_y + 40, int(w * 0.9), h], fill=(241, 245, 249), outline=(148, 163, 184), width=3)
        draw.rectangle([0, 0, 80, h], fill=(30, 41, 59))
        draw.rectangle([w-80, 0, w, h], fill=(30, 41, 59))
        draw.rectangle([0, 0, w, 80], fill=(30, 41, 59))

    @classmethod
    def _draw_retail_shop(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        draw.rectangle([0, 0, w, 1250], fill=(255, 251, 235))
        draw.rectangle([0, 1250, w, h], fill=(241, 245, 249))
        draw.rectangle([80, 300, 1000, 1150], fill=(254, 215, 170), outline=(194, 65, 12), width=4)
        for y in [550, 850, 1150]:
            draw.line([(80, y), (1000, y)], fill=(154, 52, 18), width=8)
            for px in range(120, 960, 90):
                color = (239, 68, 68) if px % 180 == 0 else (59, 130, 246)
                draw.rectangle([px, y - 90, px + 65, y - 5], fill=color, outline=(30, 41, 59), width=2)
        # Clean shopping tag icon instead of English text
        draw.polygon([(480, 150), (560, 150), (600, 210), (520, 210)], fill=(239, 68, 68), outline=(255, 255, 255), width=3)
        draw.ellipse([500, 170, 515, 185], fill=(255, 255, 255))

from PIL import Image, ImageDraw, ImageFont
import math

class ProceduralBackgroundRenderer:
    """
    Renders clean, vibrant 2D vector-style backgrounds for both 16:9 widescreen and 9:16 vertical episodes.
    Matches demo.mp4 aesthetic:
    - MSRTC Red ST Bus Stand (लालपरी एसटी बस स्थानक)
    - Night Terrace with Giant Ferris Wheel (रात्रीची हॉटेल गॅलरी व आकाशपाळणा)
    - School / College Corridor (शाळा/कॉलेजचा कॉरिडॉर)
    - Village Katta (गावाकडचा कट्टा / पार / चावडी)
    Guarantees ZERO English prompt leaks or text in any environment.
    """

    @classmethod
    def render_environment(cls, env_type: str, width: int = 1280, height: int = 720, t_sec: float = 0.0) -> Image.Image:
        img = Image.new("RGBA", (width, height), (248, 250, 252, 255))
        draw = ImageDraw.Draw(img)

        env = env_type.lower()
        if any(k in env for k in ["bus", "msrtc", "lalpari", "station"]):
            cls._draw_msrtc_bus_stand(draw, width, height, t_sec)
        elif any(k in env for k in ["terrace", "restaurant", "ferris", "night", "hotel"]):
            cls._draw_night_terrace_ferris_wheel(draw, width, height, t_sec)
        elif any(k in env for k in ["college", "school", "corridor", "hallway", "class"]):
            cls._draw_college_corridor(draw, width, height, t_sec)
        elif any(k in env for k in ["village", "katta", "chawadi", "rural", "gav", "outdoor"]):
            cls._draw_village_katta(draw, width, height, t_sec)
        else:
            cls._draw_msrtc_bus_stand(draw, width, height, t_sec)

        return img

    @classmethod
    def _draw_msrtc_bus_stand(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        """
        Iconic Maharashtrian MSRTC Red ST Bus Stand (लालपरी एसटी बस स्थानक).
        Features the red-and-white ST bus parked with open folding passenger door,
        trees, terminal concrete pavement, and green grass patches.
        """
        horizon_y = int(h * 0.45)
        ground_y = int(h * 0.62)

        # 1. Sky Gradient (Bright sunny daytime)
        for y in range(0, horizon_y, 4):
            r = int(190 + (240 - 190) * (y / horizon_y))
            g = int(225 + (248 - 225) * (y / horizon_y))
            b = int(255)
            draw.line([(0, y), (w, y)], fill=(r, g, b), width=4)

        # Fluffy white clouds
        draw.ellipse([int(w * 0.35), int(h * 0.08), int(w * 0.52), int(h * 0.22)], fill=(255, 255, 255, 230))
        draw.ellipse([int(w * 0.40), int(h * 0.04), int(w * 0.48), int(h * 0.18)], fill=(255, 255, 255, 240))

        # 2. Lush green trees in background
        draw.ellipse([-50, horizon_y - 120, int(w * 0.35), horizon_y + 40], fill=(74, 107, 70), outline=(50, 80, 50), width=3)
        draw.ellipse([int(w * 0.2), horizon_y - 140, int(w * 0.5), horizon_y + 40], fill=(90, 125, 80), outline=(50, 80, 50), width=3)

        # 3. Ground / Concrete Bus Terminal Pavement
        draw.rectangle([0, ground_y, w, h], fill=(215, 212, 204))
        # Concrete slabs & perspective lines
        for y_l in range(ground_y, h, 65):
            draw.line([(0, y_l), (w, y_l)], fill=(185, 180, 170), width=2)

        # Green Grass Patch along pavement
        draw.polygon([(0, ground_y), (int(w * 0.45), ground_y), (int(w * 0.35), h), (0, h)], fill=(120, 160, 95))
        for gx in range(20, int(w * 0.4), 25):
            draw.line([(gx, ground_y + 30), (gx - 5, ground_y + 10)], fill=(75, 115, 55), width=3)
            draw.line([(gx, ground_y + 30), (gx + 6, ground_y + 8)], fill=(75, 115, 55), width=3)

        # 4. Bus Stand Platform Pillar / Monument on far left
        draw.rectangle([0, int(h * 0.25), int(w * 0.14), ground_y + 50], fill=(230, 228, 222), outline=(150, 145, 138), width=3)
        draw.rectangle([int(w * 0.02), int(h * 0.48), int(w * 0.12), int(h * 0.58)], fill=(200, 196, 188), outline=(150, 145, 138), width=2)
        for ly in range(int(h * 0.50), int(h * 0.57), 8):
            draw.line([(int(w * 0.03), ly), (int(w * 0.11), ly)], fill=(120, 115, 108), width=2)

        # 5. ICONIC MSRTC RED ST BUS (लालपरी बस)
        # Positioned parked from x ~ 0.38 to beyond right border
        bus_x1 = int(w * 0.36)
        bus_x2 = w + 40
        bus_top = int(h * 0.16)
        bus_bottom = int(h * 0.56)

        # Bus Body (Classic Maharashtra Red / Vermilion)
        draw.rounded_rectangle([bus_x1, bus_top, bus_x2, bus_bottom], radius=24, fill=(217, 70, 38), outline=(138, 35, 15), width=5)

        # Bus Cream Middle Belt Stripe
        draw.rectangle([bus_x1 + 4, bus_top + 160, bus_x2, bus_top + 205], fill=(254, 243, 199), outline=(180, 83, 9), width=2)

        # Bus Roof Accent / Luggage Carrier Rail
        draw.line([(bus_x1 + 30, bus_top - 6), (bus_x2, bus_top - 6)], fill=(180, 83, 9), width=4)
        for rx in range(bus_x1 + 40, bus_x2, 50):
            draw.line([(rx, bus_top - 6), (rx, bus_top)], fill=(180, 83, 9), width=3)

        # Bus Big Tinted Windows (Dark glass with subtle reflections)
        win_top = bus_top + 45
        win_bot = bus_top + 155
        for wx in range(bus_x1 + 25, bus_x2 - 120, 130):
            draw.rounded_rectangle([wx, win_top, wx + 115, win_bot], radius=8, fill=(40, 50, 60, 240), outline=(20, 25, 30), width=3)
            # Seat silhouettes inside window
            draw.rounded_rectangle([wx + 15, win_bot - 45, wx + 50, win_bot - 5], radius=4, fill=(80, 90, 100))
            draw.rounded_rectangle([wx + 65, win_bot - 45, wx + 100, win_bot - 5], radius=4, fill=(80, 90, 100))
            # Glass glare line
            draw.line([(wx + 10, win_top + 10), (wx + 35, win_bot - 10)], fill=(255, 255, 255, 120), width=2)

        # Front Windshield Glass
        draw.rounded_rectangle([bus_x2 - 100, win_top - 10, bus_x2, win_bot + 15], radius=10, fill=(30, 40, 50), outline=(15, 20, 25), width=3)

        # OPEN PASSENGER FOLDING DOOR (Entrance where conductor stands)
        door_x1 = int(w * 0.72)
        door_x2 = int(w * 0.84)
        draw.rectangle([door_x1, bus_top + 30, door_x2, bus_bottom + 15], fill=(25, 30, 35), outline=(138, 35, 15), width=4)
        # Bus interior steps
        draw.rectangle([door_x1 + 5, bus_bottom - 20, door_x2 - 5, bus_bottom + 10], fill=(71, 85, 105), outline=(15, 23, 42), width=2)
        # Open door leaf swung outward
        draw.polygon([(door_x1 - 10, bus_top + 35), (door_x1 + 8, bus_top + 25), (door_x1 + 8, bus_bottom + 10), (door_x1 - 10, bus_bottom + 15)], fill=(217, 70, 38), outline=(15, 23, 42), width=3)
        draw.rectangle([door_x1 - 6, bus_top + 55, door_x1 + 4, bus_top + 130], fill=(148, 163, 184, 180), outline=(15, 23, 42), width=2)

        # Heavy Black Bus Wheels / Tires
        for wx in [int(w * 0.46), int(w * 0.94)]:
            draw.ellipse([wx - 48, bus_bottom - 25, wx + 48, bus_bottom + 75], fill=(20, 24, 30), outline=(10, 12, 16), width=4)
            # Silver Rim
            draw.ellipse([wx - 26, bus_bottom - 2, wx + 26, bus_bottom + 52], fill=(148, 163, 184), outline=(100, 116, 139), width=3)
            draw.ellipse([wx - 10, bus_bottom + 14, wx + 10, bus_bottom + 34], fill=(30, 41, 59))

    @classmethod
    def _draw_night_terrace_ferris_wheel(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        """
        Nighttime Terrace Restaurant overlooking illuminated Giant Ferris Wheel.
        """
        # 1. Dark Blue Night Sky
        for y in range(0, int(h * 0.65), 4):
            draw.line([(0, y), (w, y)], fill=(10, 15, 30 + int(20 * (y / h))), width=4)

        # Twinkling Stars
        for i in range(45):
            sx = (i * 97) % w
            sy = (i * 131) % int(h * 0.5)
            draw.rectangle([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))

        # 2. Illuminated Giant Ferris Wheel (आकाशपाळणा)
        fw_cx = int(w * 0.75)
        fw_cy = int(h * 0.32)
        fw_r = int(h * 0.36)

        # Ferris Wheel Support Legs
        draw.line([(fw_cx, fw_cy), (fw_cx - 120, int(h * 0.70))], fill=(100, 116, 139), width=8)
        draw.line([(fw_cx, fw_cy), (fw_cx + 120, int(h * 0.70))], fill=(100, 116, 139), width=8)

        # Concentric Light Rings
        draw.ellipse([fw_cx - fw_r, fw_cy - fw_r, fw_cx + fw_r, fw_cy + fw_r], outline=(56, 189, 248), width=5)
        draw.ellipse([fw_cx - fw_r + 25, fw_cy - fw_r + 25, fw_cx + fw_r - 25, fw_cy + fw_r - 25], outline=(147, 51, 234), width=3)
        draw.ellipse([fw_cx - 20, fw_cy - 20, fw_cx + 20, fw_cy + 20], fill=(255, 255, 255))

        # Spokes & Cabins
        num_spokes = 16
        rot_ang = t_sec * 0.2
        for s in range(num_spokes):
            ang = rot_ang + s * (2 * math.pi / num_spokes)
            ex = fw_cx + int(fw_r * math.cos(ang))
            ey = fw_cy + int(fw_r * math.sin(ang))
            draw.line([(fw_cx, fw_cy), (ex, ey)], fill=(186, 230, 253, 140), width=2)
            # Illuminated Passenger Gondola / Cabin
            draw.rounded_rectangle([ex - 12, ey - 8, ex + 12, ey + 14], radius=4, fill=(244, 114, 182), outline=(255, 255, 255), width=2)

        # 3. Terrace Restaurant Wooden Flooring
        floor_y = int(h * 0.65)
        draw.rectangle([0, floor_y, w, h], fill=(160, 82, 45))
        for fy in range(floor_y, h, 35):
            draw.line([(0, fy), (w, fy)], fill=(120, 53, 15), width=2)

        # Terrace Balustrade / Railing
        rail_y = floor_y - 80
        draw.line([(0, rail_y), (w, rail_y)], fill=(226, 232, 240), width=6)
        draw.line([(0, floor_y), (w, floor_y)], fill=(203, 213, 225), width=4)
        for rx in range(0, w, 40):
            draw.line([(rx, rail_y), (rx, floor_y)], fill=(203, 213, 225), width=4)

        # 4. Center Dining Table with Tablecloth & Chairs
        tbl_x = int(w * 0.52)
        tbl_y = floor_y + 10
        # Round Table Base
        draw.ellipse([tbl_x - 140, tbl_y - 45, tbl_x + 140, tbl_y + 45], fill=(244, 215, 230), outline=(219, 150, 190), width=3)
        # Hanging tablecloth skirt
        draw.polygon([
            (tbl_x - 138, tbl_y), (tbl_x + 138, tbl_y),
            (tbl_x + 115, tbl_y + 120), (tbl_x - 115, tbl_y + 120)
        ], fill=(253, 232, 240), outline=(219, 150, 190), width=3)
        # Table pedestal base
        draw.rectangle([tbl_x - 15, tbl_y + 120, tbl_x + 15, tbl_y + 160], fill=(30, 41, 59))
        draw.ellipse([tbl_x - 45, tbl_y + 150, tbl_x + 45, tbl_y + 175], fill=(15, 23, 42))

        # Potted Flower Bush on Terrace
        draw.ellipse([int(w * 0.08) - 45, floor_y - 20, int(w * 0.08) + 45, floor_y + 60], fill=(34, 197, 94), outline=(21, 128, 61), width=3)
        draw.polygon([(int(w * 0.08) - 30, floor_y + 40), (int(w * 0.08) + 30, floor_y + 40), (int(w * 0.08) + 20, floor_y + 120), (int(w * 0.08) - 20, floor_y + 120)], fill=(180, 83, 9))

    @classmethod
    def _draw_college_corridor(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        """
        School / College Hallway with Classroom Doors and Polished Corridor.
        """
        floor_y = int(h * 0.64)

        # Upper Wall: Warm Cream / Golden Yellow
        draw.rectangle([0, 0, w, floor_y], fill=(254, 240, 138))

        # Lower Wall Runner
        draw.rectangle([0, floor_y - 80, w, floor_y], fill=(251, 191, 36), outline=(217, 119, 6), width=3)

        # Polished Cyan / Blue Floor with Reflections
        draw.rectangle([0, floor_y, w, h], fill=(125, 211, 252))
        for x in range(0, w, 140):
            draw.line([(x, floor_y), (int((x - w/2) * 2.2 + w/2), h)], fill=(56, 189, 248), width=2)

        # Bright Red Classroom Doors
        for dx in [int(w * 0.12), int(w * 0.58)]:
            draw.rectangle([dx, int(h * 0.18), dx + 140, floor_y], fill=(220, 38, 38), outline=(153, 27, 27), width=4)
            # Door Glass Window
            draw.rectangle([dx + 30, int(h * 0.24), dx + 110, int(h * 0.38)], fill=(241, 245, 249), outline=(100, 116, 139), width=3)
            # Door Silver Handle
            draw.rectangle([dx + 12, int(h * 0.44), dx + 24, int(h * 0.48)], fill=(226, 232, 240), outline=(100, 116, 139), width=2)

        # Notice Board between doors
        nb_x = int(w * 0.35)
        draw.rectangle([nb_x, int(h * 0.22), nb_x + 160, int(h * 0.45)], fill=(120, 53, 15), outline=(69, 26, 3), width=4)
        draw.rectangle([nb_x + 15, int(h * 0.25), nb_x + 75, int(h * 0.35)], fill=(255, 255, 255))
        draw.rectangle([nb_x + 85, int(h * 0.26), nb_x + 145, int(h * 0.38)], fill=(254, 243, 199))

    @classmethod
    def _draw_village_katta(cls, draw: ImageDraw.ImageDraw, w: int, h: int, t_sec: float):
        """
        Vibrant Maharashtrian Village Square (गावाकडचा पार / कट्टा / चावडी).
        """
        horizon_y = int(h * 0.52)
        ground_y = int(h * 0.64)

        # Sky Gradient
        for y in range(0, horizon_y, 4):
            r = int(186 + (240 - 186) * (y / horizon_y))
            g = int(230 + (249 - 230) * (y / horizon_y))
            b = 255
            draw.line([(0, y), (w, y)], fill=(r, g, b), width=4)

        # Village Sun
        draw.ellipse([int(w * 0.82) - 45, int(h * 0.16) - 45, int(w * 0.82) + 45, int(h * 0.16) + 45], fill=(251, 191, 36))

        # Distant Sahyadri Hills
        draw.polygon([(0, horizon_y), (int(w*0.3), int(horizon_y*0.85)), (int(w*0.7), int(horizon_y*0.9)), (w, horizon_y)], fill=(187, 215, 172))

        # Earthen Ground
        draw.rectangle([0, ground_y, w, h], fill=(245, 236, 215))

        # Raised Stone Katta
        katta_top = int(h * 0.60)
        draw.rectangle([int(w * 0.05), katta_top, int(w * 0.95), h], fill=(226, 232, 240), outline=(148, 163, 184), width=4)
        for sy in range(katta_top + 45, h, 45):
            draw.line([(int(w * 0.05), sy), (int(w * 0.95), sy)], fill=(148, 163, 184), width=2)

        # Shady Banyan Tree on left
        draw.polygon([(-30, h), (110, h), (70, 0), (-30, 0)], fill=(120, 80, 50))
        draw.ellipse([-50, -40, int(w * 0.5), int(h * 0.35)], fill=(34, 197, 94), outline=(22, 163, 74), width=4)

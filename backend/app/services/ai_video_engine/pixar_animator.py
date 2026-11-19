import os
import time
import urllib.request
import urllib.parse
from pathlib import Path
from typing import List, Dict, Any, Optional
from PIL import Image
from backend.app.config import settings

class PixarAiVideoEngine:
    """
    Generative AI Pixar/Disney Video Engine.
    Generates photorealistic keyframes with consistent characters, dinosaurs,
    and lush prehistoric environments, then compiles smooth cinematic camera motion.
    Uses PIL for robust cross-platform frame synthesis.
    """

    DEFAULT_PROMPTS = [
        "Disney Pixar 3D movie still, cute young adventurer boy in orange tshirt and blue denim shorts standing beside fluffy golden retriever puppy on a cliff edge overlooking lush prehistoric jungle with giant smoking volcano and waterfalls, golden hour sunrise, cinematic 8k octane render, masterpiece",
        "Disney Pixar 3D animation, close up shot of cute adventurer boy in orange tshirt and cute golden retriever puppy looking down in amazement at a gigantic dinosaur footprint puddle in the muddy jungle ground, dramatic sunbeams through giant jungle trees, 8k render, masterpiece",
        "Disney Pixar 3D animated film still, cute boy in orange tshirt smiling and pointing excitedly at a huge friendly Stegosaurus dinosaur with orange back plates walking between palm trees, cute puppy standing next to boy, 8k octane render, masterpiece",
        "Disney Pixar 3D movie scene, crystal clear turquoise water lagoon, cute long neck Brachiosaurus dinosaur swimming in water, young boy in orange tshirt and puppy watching from sandy shore, dramatic sunrise clouds, 8k render, masterpiece"
    ]

    @classmethod
    def fetch_scene_frame(cls, prompt: str, output_path: Path, width: int = 720, height: int = 1280) -> bool:
        """Fetches a free photorealistic Pixar frame via public inference endpoint with backoff."""
        if output_path.exists() and output_path.stat().st_size > 10000:
            return True
        output_path.parent.mkdir(parents=True, exist_ok=True)
        encoded = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&nologo=true"
        
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=35) as resp:
                    with open(output_path, "wb") as f:
                        f.write(resp.read())
                if output_path.exists() and output_path.stat().st_size > 5000:
                    return True
            except Exception as e:
                print(f"[PixarAiVideoEngine] Attempt {attempt+1} warning: {e}. Retrying in 5s...")
                time.sleep(5)
        return False

    @classmethod
    def load_and_fit(cls, img_path: Path, target_w: int, target_h: int) -> Image.Image:
        """Loads image and fits to target aspect ratio (cropping/padding smoothly)."""
        img = Image.open(str(img_path)).convert("RGB")
        w, h = img.size
        scale = max(target_w / w, target_h / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        start_x = (new_w - target_w) // 2
        start_y = (new_h - target_h) // 2
        return resized.crop((start_x, start_y, start_x + target_w, start_y + target_h))

    @classmethod
    def create_cinematic_shot(cls, img: Image.Image, frame_count: int, shot_type: str = "push_in") -> List[Image.Image]:
        """Generates smoothly interpolating cinematic camera frames."""
        frames = []
        w, h = img.size
        for i in range(frame_count):
            t = i / float(frame_count - 1) if frame_count > 1 else 0
            smooth_t = 3 * (t ** 2) - 2 * (t ** 3)
            if shot_type == "push_in":
                zoom = 1.0 + 0.12 * smooth_t
                center_x, center_y = w / 2.0, h * 0.45
            elif shot_type == "pan_down":
                zoom = 1.05 + 0.08 * smooth_t
                center_x, center_y = w / 2.0, h * (0.40 + 0.15 * smooth_t)
            elif shot_type == "tilt_up":
                zoom = 1.08 - 0.05 * smooth_t
                center_x, center_y = w / 2.0, h * (0.60 - 0.20 * smooth_t)
            else:  # reveal_wide
                zoom = 1.15 - 0.12 * smooth_t
                center_x, center_y = w * (0.45 + 0.10 * smooth_t), h / 2.0

            crop_w, crop_h = w / zoom, h / zoom
            x1 = max(0, int(center_x - crop_w / 2.0))
            y1 = max(0, int(center_y - crop_h / 2.0))
            x2 = min(w, int(x1 + crop_w))
            y2 = min(h, int(y1 + crop_h))
            crop = img.crop((x1, y1, x2, y2))
            frame = crop.resize((w, h), Image.Resampling.BILINEAR)
            frames.append(frame)
        return frames

    @classmethod
    def render_episode_frames(
        cls,
        output_dir: Path,
        total_frames: int = 300,
        resolution: tuple = (1080, 1920),
        custom_scene_prompts: Optional[List[str]] = None
    ) -> List[Path]:
        """
        Renders complete multi-act Pixar cinematic video frames.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        target_w, target_h = resolution
        prompts = custom_scene_prompts or cls.DEFAULT_PROMPTS
        
        # 1. Fetch Keyframes
        cache_dir = settings.ASSETS_DIR / "characters" / "pixar_ai_scenes"
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        loaded_scenes = []
        shot_types = ["push_in", "pan_down", "tilt_up", "reveal_wide"]
        
        for idx, prompt in enumerate(prompts):
            frame_path = cache_dir / f"scene_{idx + 1}.jpg"
            if not frame_path.exists():
                cls.fetch_scene_frame(prompt, frame_path, width=720, height=1280)
            if frame_path.exists():
                loaded_scenes.append((cls.load_and_fit(frame_path, target_w, target_h), shot_types[idx % len(shot_types)]))

        if not loaded_scenes:
            fallback_names = ["act1_lost_world.jpg", "act2_footprint_track.jpg", "act3_stego_encounter.jpg", "act4_lagoon_sauropod.jpg"]
            for idx, fname in enumerate(fallback_names):
                f_path = cache_dir / fname
                if f_path.exists():
                    loaded_scenes.append((cls.load_and_fit(f_path, target_w, target_h), shot_types[idx % len(shot_types)]))

        if not loaded_scenes:
            # Fallback to demo video extracted frame if present
            demo_frame = Path("E:/YT/demo_video/frames/frame_15s.jpg")
            if demo_frame.exists():
                loaded_scenes.append((cls.load_and_fit(demo_frame, target_w, target_h), "push_in"))

        # 2. Interpolate Shots
        frames_per_shot = max(total_frames // max(len(loaded_scenes), 1), 1)
        all_shots = [cls.create_cinematic_shot(img, frames_per_shot, s_type) for img, s_type in loaded_scenes]

        # 3. Apply Cross-dissolve transitions
        crossfade = 12
        rendered_frames: List[Image.Image] = []
        for s_idx, shot in enumerate(all_shots):
            if s_idx == 0:
                rendered_frames.extend(shot[:-crossfade])
            else:
                prev_shot = all_shots[s_idx - 1]
                for k in range(crossfade):
                    alpha = k / float(crossfade)
                    blend = Image.blend(prev_shot[-crossfade + k], shot[k], alpha)
                    rendered_frames.append(blend)
                if s_idx < len(all_shots) - 1:
                    rendered_frames.extend(shot[crossfade:-crossfade])
                else:
                    rendered_frames.extend(shot[crossfade:])

        # Normalize frame count
        while len(rendered_frames) < total_frames:
            rendered_frames.append(rendered_frames[-1])
        rendered_frames = rendered_frames[:total_frames]

        # 4. Write frames to disk
        frame_paths = []
        for idx, f in enumerate(rendered_frames):
            frame_file = output_dir / f"frame_{idx + 1:04d}.jpg"
            f.save(str(frame_file), "JPEG", quality=95)
            frame_paths.append(frame_file)

        print(f"[PixarAiVideoEngine] Rendered {len(frame_paths)} high-definition Pixar frames into {output_dir}")
        return frame_paths

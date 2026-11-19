import os
import time
import asyncio
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from backend.app.config import settings

class GoogleVeoVideoGenerator:
    """
    Official Google Veo / Gemini AI Video Generation Engine.
    Leverages Google's Veo 3 / Veo 2 foundation models via google-genai
    to generate cinematic Disney/Pixar 3D animated scenes with genuine character motion,
    facial expressions, quadruped animal movement, and dynamic camera physics.
    """

    DEFAULT_VEO_MODELS = [
        "veo-3.1-generate-001",
        "veo-3.1-fast-generate-preview",
        "veo-2.0-generate-001"
    ]

    CANONICAL_PIXAR_SCENES = [
        {
            "act": 1,
            "title": "Prehistoric Overlook",
            "prompt": (
                "Disney Pixar 3D animation, photorealistic cinematic lighting, young adventurer boy with messy brown hair "
                "in orange t-shirt and blue denim shorts standing beside an adorable fluffy golden retriever puppy on a mossy cliff edge. "
                "The boy smiles and points excitedly across a vast prehistoric tropical valley with waterfalls and a smoking volcano in the background. "
                "Gentle camera push-in, palm trees swaying in warm breeze, sunbeams, 8k resolution, octane render, Pixar movie quality."
            ),
            "duration": 5
        },
        {
            "act": 2,
            "title": "Dinosaur Footprint Discovery",
            "prompt": (
                "Disney Pixar 3D animated movie, close-up tracking shot, cute boy in orange t-shirt crouching down in jungle mud, "
                "his cute golden retriever puppy sniffing an enormous dinosaur footprint filled with muddy water. "
                "The boy gasps in wonder, wide expressive eyes, genuine facial animation, volumetric sunlight through giant ferns, masterpiece."
            ),
            "duration": 5
        },
        {
            "act": 3,
            "title": "Gentle Giant Encounter",
            "prompt": (
                "Disney Pixar 3D feature film, cute adventurer boy and smiling golden retriever puppy looking up in awe "
                "as a massive, friendly Stegosaurus dinosaur with mossy textured skin and orange back plates walks gracefully between ancient redwood trees. "
                "Cinematic camera tilt-up, lifelike dinosaur locomotion and breathing motion, warm golden hour glow, Pixar masterpiece."
            ),
            "duration": 5
        }
    ]

    @classmethod
    def get_api_client(cls, api_key: Optional[str] = None):
        """Initializes the google-genai client with proper credential resolution."""
        key = api_key or getattr(settings, "GEMINI_API_KEY", None) or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError(
                "GEMINI_API_KEY is not configured! Please set GEMINI_API_KEY in your E:\\YT\\.env file "
                "or export it as an environment variable to use Google Veo video generation."
            )
        try:
            from google import genai
            return genai.Client(api_key=key)
        except ImportError:
            raise ImportError(
                "google-genai is not installed! Run: python -m pip install google-genai"
            )

    @classmethod
    def generate_single_scene_veo(
        cls,
        prompt: str,
        output_file: Path,
        duration_seconds: int = 5,
        aspect_ratio: str = "9:16",
        resolution: str = "720p",
        model: Optional[str] = None,
        reference_image_path: Optional[Path] = None,
        api_key: Optional[str] = None
    ) -> Path:
        """
        Executes an asynchronous Veo video generation request and polls until completed.
        Supports both text-to-video and image-to-video conditioning.
        """
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        client = cls.get_api_client(api_key)
        from google.genai import types

        model_name = model or getattr(settings, "VEO_MODEL", "veo-3.1-fast-generate-preview")

        print(f"[GoogleVeo] Initiating video generation on model '{model_name}'...")
        print(f"[GoogleVeo] Prompt: \"{prompt[:90]}...\"")
        print(f"[GoogleVeo] Format: {aspect_ratio}, Duration: {duration_seconds}s, Resolution: {resolution}")

        config = types.GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            duration_seconds=duration_seconds,
            resolution=resolution,
            enhance_prompt=True
        )

        # Image-to-Video support
        source = None
        image_obj = None
        if reference_image_path and Path(reference_image_path).exists():
            print(f"[GoogleVeo] Attaching reference image: {reference_image_path}")
            image_obj = types.Image.from_file(location=str(reference_image_path))

        # Launch Veo operation
        try:
            if image_obj:
                operation = client.models.generate_videos(
                    model=model_name,
                    prompt=prompt,
                    image=image_obj,
                    config=config
                )
            else:
                operation = client.models.generate_videos(
                    model=model_name,
                    prompt=prompt,
                    config=config
                )
        except Exception as e:
            # Fallback to Veo 2.0 if preview model name differs in account tier
            if "not found" in str(e).lower() or "permission" in str(e).lower():
                fallback = "veo-2.0-generate-001"
                print(f"[GoogleVeo] Primary model failed ({e}). Retrying with fallback: {fallback}...")
                operation = client.models.generate_videos(
                    model=fallback,
                    prompt=prompt,
                    config=config
                )
            else:
                raise e

        print(f"[GoogleVeo] Operation submitted successfully. Operation ID: {operation.name}")
        print("[GoogleVeo] Processing cinematic video frames with Veo neural diffusion...")

        # Poll operation until completion
        start_time = time.time()
        poll_interval = 10
        while not operation.done:
            elapsed = int(time.time() - start_time)
            print(f"[GoogleVeo] Still generating ({elapsed}s elapsed)... Polling status...")
            time.sleep(poll_interval)
            operation = client.operations.get(operation)

        if hasattr(operation, "error") and operation.error:
            raise RuntimeError(f"Veo video generation failed: {operation.error}")

        # Download result
        generated_video = operation.response.generated_videos[0]
        client.files.download(file=generated_video.video)
        generated_video.video.save(str(output_file))
        print(f"[GoogleVeo] Success! Video generated and saved to: {output_file}")
        return output_file

    @classmethod
    def concatenate_scenes_ffmpeg(
        cls,
        scene_files: List[Path],
        output_file: Path,
        transition: str = "fade"
    ) -> Path:
        """Concatenates multiple Veo scenes into a continuous master episode."""
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        concat_list_file = output_file.parent / "veo_concat_list.txt"
        with open(concat_list_file, "w", encoding="utf-8") as f:
            for s in scene_files:
                f.write(f"file '{Path(s).resolve().as_posix()}'\n")

        cmd = [
            ffmpeg_exe, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list_file),
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "fast",
            "-pix_fmt", "yuv420p",
            str(output_file)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg concat failed: {res.stderr}")
        return output_file

    @classmethod
    def generate_full_short_pipeline(
        cls,
        output_path: Path,
        scene_prompts: Optional[List[str]] = None,
        aspect_ratio: str = "9:16",
        total_duration: int = 10
    ) -> Path:
        """
        Orchestrates full Veo AI video generation pipeline:
        Generates individual acts, merges them seamlessly, and returns final master video.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = output_path.parent / "veo_temp_scenes"
        temp_dir.mkdir(parents=True, exist_ok=True)

        prompts = scene_prompts or [s["prompt"] for s in cls.CANONICAL_PIXAR_SCENES[:2]]
        scene_duration = max(total_duration // len(prompts), 4)

        scene_files = []
        for idx, prompt in enumerate(prompts):
            s_file = temp_dir / f"scene_{idx + 1}.mp4"
            cls.generate_single_scene_veo(
                prompt=prompt,
                output_file=s_file,
                duration_seconds=scene_duration,
                aspect_ratio=aspect_ratio
            )
            scene_files.append(s_file)

        return cls.concatenate_scenes_ffmpeg(scene_files, output_path)

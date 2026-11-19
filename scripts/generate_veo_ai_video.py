"""
Autonomous AI Cartoon Studio - Google Veo / Gemini AI Video Generation CLI
Generates authentic Disney/Pixar 3D animated video clips using Google Veo 3 / Veo 2 models.
"""

import os
import sys
import argparse
from pathlib import Path

# Ensure E:\YT is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.app.config import settings
from backend.app.services.ai_video_engine.veo_video_generator import GoogleVeoVideoGenerator

def main():
    parser = argparse.ArgumentParser(description="Generate 3D Pixar Animation using Google Veo AI Video Generation")
    parser.add_argument("--prompt", type=str, default=None, help="Custom animation prompt")
    parser.add_argument("--image", type=str, default=None, help="Path to reference image for image-to-video animation")
    parser.add_argument("--model", type=str, default="veo-3.1-fast-generate-preview", help="Veo model (veo-3.1-fast-generate-preview, veo-3.1-generate-001, veo-2.0-generate-001)")
    parser.add_argument("--duration", type=int, default=5, help="Duration in seconds (5-10s)")
    parser.add_argument("--aspect_ratio", type=str, default="9:16", choices=["9:16", "16:9"], help="Video aspect ratio (9:16 for Shorts, 16:9 for widescreen)")
    parser.add_argument("--output", type=str, default=str(BASE_DIR / "output" / "shorts" / "veo_ai_generated_short.mp4"), help="Output MP4 path")
    parser.add_argument("--api_key", type=str, default=None, help="Gemini API Key (optional if set in .env)")

    args = parser.parse_args()

    api_key = args.api_key or getattr(settings, "GEMINI_API_KEY", None) or os.getenv("GEMINI_API_KEY")

    print("==========================================================================")
    print("      GOOGLE VEO / GEMINI AI VIDEO GENERATOR — PIXAR 3D ENGINE            ")
    print("==========================================================================")

    if not api_key:
        print("\n[VEO CONFIG] Warning: No GEMINI_API_KEY detected.")
        print("To generate real-time AI video using Google Veo:")
        print("  1. Obtain your API key from Google AI Studio: https://aistudio.google.com/app/apikey")
        print("  2. Add it to E:\\YT\\.env:")
        print("     GEMINI_API_KEY=AIzaSy...")
        print("  3. Re-run this command with your active key.")
        print("\nNote: Video generation requires an account tier or Google Cloud project with Veo video generation enabled.")
        sys.exit(1)

    prompt = args.prompt or (
        "Disney Pixar 3D animated film still, cute adventurer boy in orange t-shirt and blue shorts "
        "smiling and pointing excitedly at a huge friendly Stegosaurus dinosaur walking between palm trees, "
        "fluffy golden retriever puppy standing beside him, dynamic cinematic lighting, 8k render, masterpiece"
    )

    out_file = Path(args.output)
    print(f"\n[VEO CONFIG] Model: {args.model}")
    print(f"[VEO CONFIG] Aspect Ratio: {args.aspect_ratio}")
    print(f"[VEO CONFIG] Duration: {args.duration}s")
    print(f"[VEO CONFIG] Target Output: {out_file}")

    try:
        GoogleVeoVideoGenerator.generate_single_scene_veo(
            prompt=prompt,
            output_file=out_file,
            duration_seconds=args.duration,
            aspect_ratio=args.aspect_ratio,
            model=args.model,
            reference_image_path=Path(args.image) if args.image else None,
            api_key=api_key
        )
        print(f"\n✔ Master Veo video successfully created: {out_file}")
    except Exception as e:
        print(f"\n❌ Veo Generation Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

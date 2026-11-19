"""
Autonomous AI Cartoon Studio - Local GPU AI Video Generator (100% Free & Unlimited)
Executes neural video diffusion on your local NVIDIA GPU laptop using PyTorch & Hugging Face Diffusers.
"""

import os
import sys
import argparse
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.app.config import settings
from backend.app.services.ai_video_engine.local_diffusion_engine import LocalDiffusionVideoEngine

def main():
    parser = argparse.ArgumentParser(description="Generate 3D Pixar Animation locally on your GPU (100% Free & Unlimited)")
    parser.add_argument("--prompt", type=str, default=None, help="Animation text prompt")
    parser.add_argument("--model", type=str, default="Lightricks/LTX-Video", help="Diffusion model (Lightricks/LTX-Video or Wan-AI/Wan2.1-T2V-1.3B)")
    parser.add_argument("--frames", type=int, default=49, help="Number of frames (e.g. 49 for ~2s, 121 for ~5s)")
    parser.add_argument("--fps", type=int, default=24, help="Frames per second")
    parser.add_argument("--output", type=str, default=str(BASE_DIR / "output" / "shorts" / "local_gpu_pixar_short.mp4"), help="Output video path")

    args = parser.parse_args()

    default_prompt = (
        "Disney Pixar 3D animated movie, photorealistic cinematic lighting, cute young adventurer boy in orange t-shirt "
        "and blue denim shorts standing beside an adorable fluffy golden retriever puppy overlooking a lush prehistoric tropical valley "
        "with waterfalls and a smoking volcano, golden hour sunrise, palm trees swaying, 8k resolution, octane render, masterpiece"
    )

    prompt = args.prompt or default_prompt
    out_file = Path(args.output)

    print("==========================================================================")
    print("      LOCAL GPU AI VIDEO GENERATOR — 100% FREE & UNLIMITED                 ")
    print("==========================================================================")
    print(f"Model: {args.model}")
    print(f"Frames: {args.frames} @ {args.fps}fps")
    print(f"Output: {out_file}")

    try:
        LocalDiffusionVideoEngine.generate_video(
            prompt=prompt,
            output_file=out_file,
            num_frames=args.frames,
            fps=args.fps
        )
        print(f"\n✔ Video successfully generated: {out_file}")
    except Exception as e:
        print(f"\n❌ Local GPU Generation Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

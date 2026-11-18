"""
Assembles rendered Blender 3D frames into master 10s short video with cinematic audio.
"""

import os
import subprocess
import shutil
from pathlib import Path

FFMPEG_BIN = r"C:\Users\Mr.Scientist\AppData\Roaming\Python\Python312\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"
FRAMES_PATTERN = r"E:\YT\output\renders\blender_3d_frames\frame_%04d.jpg"
AUDIO_FILE = r"E:\YT\assets\audio\demo_short\master_cinematic_audio_10s.wav"
OUTPUT_VIDEO = r"E:\YT\output\shorts\master_blender_3d_short_10s.mp4"
THUMBNAIL_SRC = r"E:\YT\output\renders\blender_3d_frames\frame_0120.jpg"
THUMBNAIL_DST = r"E:\YT\assets\thumbnails\demo_pixar_short_10s_thumb.jpg"
BRAIN_DIR = r"C:\Users\Mr.Scientist\.gemini\antigravity\brain\1ff6e728-5386-415c-b67c-5b2db0481163"

def assemble():
    print(f"[Assembly] Compiling 300 frames from {FRAMES_PATTERN} with audio {AUDIO_FILE}...")
    os.makedirs(os.path.dirname(OUTPUT_VIDEO), exist_ok=True)
    
    cmd = [
        FFMPEG_BIN,
        "-y",
        "-framerate", "30",
        "-i", FRAMES_PATTERN,
        "-i", AUDIO_FILE,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("[Assembly] Error during FFmpeg encoding:\n", res.stderr)
        return False
        
    print(f"[Assembly] SUCCESS! Master 3D video created: {OUTPUT_VIDEO}")
    
    # Copy thumbnail
    if os.path.exists(THUMBNAIL_SRC):
        shutil.copy2(THUMBNAIL_SRC, THUMBNAIL_DST)
        print(f"[Assembly] Thumbnail updated: {THUMBNAIL_DST}")
        
    # Copy artifacts
    shutil.copy2(OUTPUT_VIDEO, os.path.join(BRAIN_DIR, "master_blender_3d_short_10s.mp4"))
    if os.path.exists(THUMBNAIL_SRC):
        shutil.copy2(THUMBNAIL_SRC, os.path.join(BRAIN_DIR, "master_blender_3d_frame_0120.jpg"))
    if os.path.exists(r"E:\YT\output\renders\blender_3d_frames\frame_0045.jpg"):
        shutil.copy2(r"E:\YT\output\renders\blender_3d_frames\frame_0045.jpg", os.path.join(BRAIN_DIR, "master_blender_3d_frame_0045.jpg"))
    if os.path.exists(r"E:\YT\output\renders\blender_3d_frames\frame_0210.jpg"):
        shutil.copy2(r"E:\YT\output\renders\blender_3d_frames\frame_0210.jpg", os.path.join(BRAIN_DIR, "master_blender_3d_frame_0210.jpg"))
        
    print("[Assembly] Artifact copies generated.")
    return True

if __name__ == "__main__":
    assemble()

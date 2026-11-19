import os
import cv2
import numpy as np
import asyncio
import edge_tts
import subprocess
from pathlib import Path

# Paths
BASE_DIR = Path("D:/YT")
SCENE_DIR = BASE_DIR / "assets" / "characters" / "pixar_ai_scenes"
AUDIO_DIR = BASE_DIR / "assets" / "audio" / "ai_short"
RENDER_DIR = BASE_DIR / "output" / "renders" / "ai_pixar_short"
OUTPUT_DIR = BASE_DIR / "output" / "shorts"
THUMB_DIR = BASE_DIR / "assets" / "thumbnails"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
RENDER_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
THUMB_DIR.mkdir(parents=True, exist_ok=True)

TARGET_W = 1080
TARGET_H = 1920
FPS = 30
TOTAL_FRAMES = 300  # 10.0 seconds

def load_and_fit(img_path, target_w=TARGET_W, target_h=TARGET_H):
    """Loads image and fits to target aspect ratio (cropping/padding smoothly)."""
    img = cv2.imread(str(img_path))
    if img is None:
        raise FileNotFoundError(f"Could not load {img_path}")
    h, w, _ = img.shape
    # Scale to cover target
    scale = max(target_w / w, target_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    # Center crop to target
    start_x = (new_w - target_w) // 2
    start_y = (new_h - target_h) // 2
    cropped = resized[start_y:start_y + target_h, start_x:start_x + target_w]
    return cropped

def create_camera_shot(img, frame_count, shot_type="push_in"):
    """Creates a sequence of smoothly moving frames (push-in, pan, zoom)."""
    frames = []
    h, w, _ = img.shape
    
    for i in range(frame_count):
        t = i / float(frame_count - 1) if frame_count > 1 else 0
        # Smooth ease in out: 3*t^2 - 2*t^3
        smooth_t = 3 * (t ** 2) - 2 * (t ** 3)
        
        if shot_type == "push_in":
            # Scale from 1.0 to 1.12
            zoom = 1.0 + 0.12 * smooth_t
            center_x = w / 2.0
            center_y = h * 0.45  # Focus slightly above center (character eyes)
        elif shot_type == "pan_down":
            zoom = 1.05 + 0.08 * smooth_t
            center_x = w / 2.0
            center_y = h * (0.40 + 0.15 * smooth_t)  # Pan down towards ground
        elif shot_type == "tilt_up":
            zoom = 1.08 - 0.05 * smooth_t
            center_x = w / 2.0
            center_y = h * (0.60 - 0.20 * smooth_t)  # Tilt up towards dinosaur head
        elif shot_type == "reveal_wide":
            zoom = 1.15 - 0.12 * smooth_t  # Pull back to reveal entire lagoon
            center_x = w * (0.45 + 0.10 * smooth_t)
            center_y = h / 2.0
        else:
            zoom = 1.0 + 0.08 * smooth_t
            center_x = w / 2.0
            center_y = h / 2.0
            
        crop_w = w / zoom
        crop_h = h / zoom
        x1 = max(0, int(center_x - crop_w / 2.0))
        y1 = max(0, int(center_y - crop_h / 2.0))
        x2 = min(w, int(x1 + crop_w))
        y2 = min(h, int(y1 + crop_h))
        
        # Ensure exact slice
        crop = img[y1:y2, x1:x2]
        frame = cv2.resize(crop, (w, h), interpolation=cv2.INTER_LINEAR)
        frames.append(frame)
        
    return frames

async def synthesize_neural_dialogue():
    """Generates authentic voice lines using Edge-TTS neural models."""
    dialogue_script = [
        ("scene1.mp3", "Whoa, look at this place! We're in dinosaur land!", "en-US-ChristopherNeural"),
        ("scene2.mp3", "Look at this huge footprint! A real dinosaur is nearby!", "en-US-ChristopherNeural"),
        ("scene3.mp3", "There's a friendly Stegosaurus! But wait... what's in the lagoon?!", "en-US-ChristopherNeural")
    ]
    
    mp3_paths = []
    for fname, text, voice in dialogue_script:
        dest = AUDIO_DIR / fname
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(dest))
        mp3_paths.append(dest)
        print(f"Generated voice: {fname}")
        
    # Combine dialogue into master audio
    master_dialogue = AUDIO_DIR / "master_dialogue.mp3"
    concat_txt = AUDIO_DIR / "concat_list.txt"
    with open(concat_txt, "w") as f:
        for p in mp3_paths:
            f.write(f"file '{p.as_posix()}'\n")
            
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy", str(master_dialogue)
    ]
    subprocess.run(cmd, check=True)
    return master_dialogue

def render_cinematic_animation():
    print("[1/4] Loading high-definition Pixar AI scenes...")
    img1 = load_and_fit(SCENE_DIR / "act1_lost_world.jpg")
    img2 = load_and_fit(SCENE_DIR / "act2_footprint_track.jpg")
    img3 = load_and_fit(SCENE_DIR / "act3_stego_encounter.jpg")
    img4 = load_and_fit(SCENE_DIR / "act4_lagoon_sauropod.jpg")
    
    # Save High-CTR Thumbnail
    thumb_path = THUMB_DIR / "master_ai_pixar_short_thumb.jpg"
    cv2.imwrite(str(thumb_path), img1, [cv2.IMWRITE_JPEG_QUALITY, 96])
    print(f"High-CTR Thumbnail saved: {thumb_path}")
    
    print("[2/4] Generating 300 cinematic camera motion frames...")
    shot1 = create_camera_shot(img1, 75, "push_in")
    shot2 = create_camera_shot(img2, 75, "pan_down")
    shot3 = create_camera_shot(img3, 75, "tilt_up")
    shot4 = create_camera_shot(img4, 75, "reveal_wide")
    
    all_shots = [shot1, shot2, shot3, shot4]
    crossfade_len = 12
    
    rendered_frames = []
    for s_idx, shot in enumerate(all_shots):
        if s_idx == 0:
            rendered_frames.extend(shot[:-crossfade_len])
        else:
            prev_shot = all_shots[s_idx - 1]
            # Cross-dissolve transition
            for k in range(crossfade_len):
                alpha = k / float(crossfade_len)
                blend = cv2.addWeighted(prev_shot[-crossfade_len + k], 1.0 - alpha, shot[k], alpha, 0)
                rendered_frames.append(blend)
            if s_idx < len(all_shots) - 1:
                rendered_frames.extend(shot[crossfade_len:-crossfade_len])
            else:
                rendered_frames.extend(shot[crossfade_len:])
                
    # Normalize to exactly 300 frames
    while len(rendered_frames) < TOTAL_FRAMES:
        rendered_frames.append(rendered_frames[-1])
    rendered_frames = rendered_frames[:TOTAL_FRAMES]
    
    print(f"[3/4] Writing {len(rendered_frames)} frames to disk...")
    for idx, f in enumerate(rendered_frames):
        frame_file = RENDER_DIR / f"frame_{idx + 1:04d}.jpg"
        cv2.imwrite(str(frame_file), f, [cv2.IMWRITE_JPEG_QUALITY, 95])
    print("Frame generation completed!")

def assemble_final_video(master_audio_path):
    print("[4/4] Assembling final video with FFmpeg...")
    final_output = OUTPUT_DIR / "master_ai_pixar_short.mp4"
    bg_music = BASE_DIR / "assets" / "audio" / "music" / "adventure_orchestral.mp3"
    
    # Check if bg_music exists
    if bg_music.exists():
        cmd = [
            "ffmpeg", "-y",
            "-r", str(FPS),
            "-i", str(RENDER_DIR / "frame_%04d.jpg"),
            "-i", str(master_audio_path),
            "-i", str(bg_music),
            "-filter_complex",
            "[1:a]volume=1.0[vdiag];[2:a]volume=0.18[vmusic];[vdiag][vmusic]amix=inputs=2:duration=first[aout]",
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-ar", "44100",
            "-ac", "2",
            "-c:a", "aac",
            "-strict", "-2",
            "-b:a", "128k",
            "-shortest",
            str(final_output)
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-r", str(FPS),
            "-i", str(RENDER_DIR / "frame_%04d.jpg"),
            "-i", str(master_audio_path),
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-ar", "44100",
            "-ac", "2",
            "-c:a", "aac",
            "-strict", "-2",
            "-b:a", "128k",
            "-shortest",
            str(final_output)
        ]
        
    subprocess.run(cmd, check=True)
    print(f"SUCCESS: Master video assembled at: {final_output}")
    print(f"File size: {os.path.getsize(final_output) / (1024*1024):.2f} MB")
    return final_output

async def main():
    print("=================================================================")
    print("      GENERATING 100% FREE MASTER AI PIXAR CARTOON SHORT         ")
    print("=================================================================")
    audio_path = await synthesize_neural_dialogue()
    render_cinematic_animation()
    out_video = assemble_final_video(audio_path)
    print("\nALL PHASES COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(main())

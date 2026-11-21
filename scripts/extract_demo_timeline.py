import imageio_ffmpeg, subprocess, os

ff_exe = imageio_ffmpeg.get_ffmpeg_exe()
os.makedirs("output/demo_frames", exist_ok=True)

times = [0.5, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 25.0, 28.0]
for t in times:
    out_p = f"output/demo_frames/frame_{t:04.1f}s.png"
    cmd = [ff_exe, "-ss", str(t), "-i", "demo_video/demo.mp4", "-vframes", "1", "-y", out_p]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Extracted demo frames successfully.")

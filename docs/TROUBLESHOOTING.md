# Autonomous AI Cartoon Studio
## Troubleshooting, Diagnostics & Incident Recovery Manual

---

## 1. Common Production Incidents & Resolution Protocols

### Incident 1: Blender Render Crashes / Out of Memory (OOM)
- **Symptoms:** Headless Blender worker exits with return code != 0 or silent abort midway through frame generation.
- **Root Cause:** Excessive polygon count, oversized 8K texture maps, or VRAM saturation from concurrent AI processes.
- **Automated Recovery:**
  1. Inspect `episodes/in_progress/<episode_id>/render.log` to identify the last successfully rendered frame index.
  2. Free GPU VRAM by issuing `torch.cuda.empty_cache()` to any idle AI workers.
  3. Resume rendering only from the failed frame index using the command:
     ```powershell
     python scripts/blender_headless_runner.py --resume-from-frame <N>
     ```

### Incident 2: Dialogue Audio / Lip-Sync Desynchronization
- **Symptoms:** Mouth movements lag behind or lead spoken audio words by more than 2 frames (66ms).
- **Root Cause:** Variable sample rate in dialogue audio or mismatched framerate (24 fps vs 30 fps timeline).
- **Resolution:**
  1. Force 48,000 Hz 16-bit PCM WAV standardization on all voice stems using `AudioProcessor`.
  2. Confirm project configuration `BLENDER_FPS = 30`.
  3. Re-run `Rhubarb Lip Sync` acoustic alignment to regenerate viseme keyframes.

### Incident 3: YouTube API Quota Exceeded (HTTP 403 `quotaExceeded`)
- **Symptoms:** Video upload fails with `quotaExceeded: The request cannot be completed because you have exceeded your quota.`
- **Resolution:**
  1. The studio automatically catches HTTP 403 and moves the job state from `PUBLISHING` to `QUEUED_FOR_QUOTA_RESET`.
  2. The video file and metadata remain safely staged in `output/` with an immutable SHA-256 hash.
  3. The scheduler sleeps until midnight Pacific Time (PST), at which point YouTube quotas reset, and automatically resumes the upload without human intervention.

### Incident 4: Windows Application Control (WDAC) DLL Blocks
- **Symptoms:** `ImportError: DLL load failed while importing _processors_cy: An Application Control policy has blocked this file.`
- **Resolution:**
  1. The studio defaults to pure-Python libraries and standard `aiosqlite`.
  2. Avoid installing binary `.pyd` files into user roaming directories; use standalone portable binaries (e.g. bundled FFmpeg) that do not trigger AppLocker blocks.

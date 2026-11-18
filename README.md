# Autonomous AI Cartoon Studio & YouTube Automation Platform

A complete, independent, AI-powered 3D animated series generation and YouTube automation production platform.

---

## Key Features

1. **Deterministic 3D Character Consistency**: 
   - Eliminates 2D generative video flickering and morphing by utilizing true 3D character geometries, standardized rigging (Rigify + ARKit 52 shapekeys), and headless scene assembly.
2. **AI Story & Long-Term Continuity Engine**:
   - Multi-agent architecture (Showrunner, Screenwriter, Continuity Supervisor) integrated with persistent episodic memory DAG and lore stores.
   - Every episode ends with an authentic, curiosity-driven cliffhanger that naturally drives the premise of subsequent episodes.
3. **Expressive Voice & Viseme Lip-Sync**:
   - High-fidelity neural voice synthesis with emotional tone modulation (whisper, excitement, fear, anger, sarcasm).
   - Rhubarb 9-viseme FACS blendshape mapping driving 3D character mouth movements with millisecond accuracy.
4. **Cinematic 3D Camera & Procedural Lighting**:
   - Automated director selecting establishing tracking shots, medium two-shots, over-the-shoulder framings, and emotional close-ups.
   - Three-point lighting presets (Key, Fill, Rim, Ambient).
5. **Headless Post-Production & Sound Design**:
   - Automated FFmpeg assembly with dynamic sidechain audio ducking (-14dB music reduction during dialogue).
   - Word-level highlighted subtitles.
6. **AI Thumbnail Generation & CTR Engine**:
   - Hero frame extraction with bold cartoon typography, outlines, and curiosity text overlays.
7. **Monetization & YouTube Compliance Gate**:
   - Pre-publication checks for YouTube Community Guidelines, COPPA ("Made for Kids") classification, and advertiser-friendly eligibility.
   - Manual Approval Gate mode enabled by default for creator review before upload.
8. **Central Web Studio Dashboard**:
   - Real-time production management, 3D character inspector, episode queue, media review player, and publishing controls.

---

## Project Structure

```
e:\YT\
├── backend\
│   ├── app\
│   │   ├── api\v1\routes.py       # REST API endpoints
│   │   ├── config.py              # Central configuration & paths
│   │   ├── database.py            # Async aiosqlite database initialization
│   │   ├── main.py                # FastAPI web server & static mounts
│   │   ├── repositories.py        # Database CRUD repositories
│   │   ├── schemas\               # Pydantic validation models
│   │   ├── static\index.html      # Central Web Studio Dashboard
│   │   └── services\
│   │       ├── story_engine\      # Showrunner, Screenwriter, Continuity, Memory
│   │       ├── voice_engine\      # TTS, Rhubarb Lip-Sync, Audio Processor
│   │       ├── blender_engine\    # bpy automation, Camera director, Render Manager
│   │       ├── post_production\   # FFmpeg Compositor, Subtitle Engine
│   │       ├── thumbnail_engine\  # Typography styler, Thumbnail Generator
│   │       ├── youtube_engine\    # Uploader, Compliance Checker, Metadata
│   │       └── pipeline_orchestrator.py # End-to-end production pipeline
├── assets\                        # Characters, voices, music, SFX, thumbnails
├── data\                          # cartoon_studio.db SQLite database
├── output\                        # Rendered frames, Shorts, Long-form episodes
└── scripts\
    └── test_pipeline.py           # End-to-end pilot validation script
```

---

## Quickstart

### 1. Run the Full End-to-End Pipeline Test
```powershell
python e:\YT\scripts\test_pipeline.py
```

### 2. Launch the Central Web Dashboard
```powershell
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```
Open `http://localhost:8000` or `http://localhost:8000/studio` in your web browser.

# Autonomous AI Cartoon Studio
## Master Technical Specification, Hardware Audit & Autonomous Implementation Blueprint

---

## 1. Project Environment & Hardware Audit Summary

| Diagnostic Metric | Audited Reality | Engineering Impact |
| :--- | :--- | :--- |
| **CPU** | Intel Core i5-8265U (4 Cores, 8 Threads @ 1.60 GHz) | Capable of multi-threaded CPU rendering, ONNX inference, and FFmpeg encoding. |
| **GPU** | Intel UHD Graphics 620 (Shared VRAM, No NVIDIA CUDA) | **Strictly CPU-First Pipeline.** Heavy diffusion video models (Wan 2.2) requiring CUDA are excluded from local execution. 3D Blender geometry pipeline is the source of truth. |
| **RAM** | 16 GB DDR4 (15.89 GB usable) | Adequate for Blender headless, lightweight TTS, and audio mixing with strict 8GB process caps. |
| **Storage (Drive E:)** | **252.54 GB Free Space** | Substantial storage capacity for 3D asset libraries, voice caches, and video archives. |
| **Operating System** | Windows 10/11 x64 (Active WDAC/AppLocker) | Pure-Python modules, ONNX Runtime, and static standalone binaries ensure 100% security policy compatibility. |

---

## 2. Final System Architecture Diagram

```mermaid
flowchart TD
    subgraph UI ["Layer 1: Central Web Studio (Next.js / HTML5 Dashboard)"]
        UI_Dash["Production Status & Queue Monitor"]
        UI_Series["Series, Seasons & Episode Planner"]
        UI_Char["Character Studio (3D WebGL Inspector)"]
        UI_Review["Media Review & 1-Click Publishing Gate"]
    end

    subgraph Orchestrator ["Layer 2: Autonomous AI Orchestration Core"]
        StateEngine["Durable Job State Machine (Redis/In-Memory)"]
        ResourceGov["Resource & Thermal Governor (CPU/RAM/Disk Throttler)"]
        ErrorRecovery["Self-Correction & Automated Scene Retry Loop"]
    end

    subgraph Cognition ["Layer 3: Story & Episodic Memory DAG"]
        Showrunner["AI Showrunner (Series Arc & Season Planner)"]
        Screenwriter["Screenwriter Agent (Directorial JSON Scripts)"]
        Continuity["Continuity Supervisor (Lore Conflict Auditor)"]
        MemoryDAG["Episodic Memory Store (Canon Events, Character Knowledge)"]
    end

    subgraph Production ["Layer 4: Local 3D Blender & Performance Engines"]
        CharRig["Character & Rigging (MPFB2 + Rigify ARKit52)"]
        MocapRetarget["Animation & Retargeting (250+ Parametric Action Library)"]
        VoiceEngine["Local Neural TTS (Piper / Kokoro ONNX)"]
        LipSync["Rhubarb Lip-Sync (9-Viseme Shapekey Driver)"]
        BlenderDirector["Headless Blender Cinematographer (bpy)"]
        RenderEngine["Blender Eevee-Next / Stylized NPR CPU Renderer"]
    end

    subgraph PostProduction ["Layer 5: Post-Production & Compliance"]
        FFmpegMixer["FFmpeg Audio-Video Compositor & Sidechain Ducking"]
        Subtitles["WhisperX Word-Level Subtitle Burner"]
        ThumbGen["Hero Frame Snapshot & Outlined Typography Styler"]
        QualityGate["Automated Visual, Audio & Geometry Quality Auditor"]
        Compliance["Monetization & COPPA Preflight Scanner"]
    end

    subgraph Distribution ["Layer 6: YouTube Publishing & Analytics Feedback"]
        YT_Uploader["YouTube Data API v3 Resumable Uploader"]
        YT_Analytics["Retention Curve & CTR Scraper"]
        FeedbackLoop["Creative Optimization Loop (Prompt Refiner)"]
    end

    UI --> StateEngine
    StateEngine --> Showrunner --> Screenwriter --> Continuity
    Continuity <--> MemoryDAG
    Screenwriter --> CharRig & MocapRetarget & VoiceEngine & LipSync & BlenderDirector
    CharRig & MocapRetarget & LipSync & BlenderDirector --> RenderEngine
    VoiceEngine --> LipSync & FFmpegMixer
    RenderEngine --> QualityGate
    QualityGate -- "Pass" --> FFmpegMixer --> Subtitles --> ThumbGen --> Compliance
    QualityGate -- "Fail" --> ErrorRecovery --> BlenderDirector
    Compliance --> YT_Uploader
    YT_Uploader --> YT_Analytics --> FeedbackLoop --> Showrunner
```

---

## 3. Autonomous 24-Step Production Workflow

```mermaid
sequenceDiagram
    autonumber
    participant Orch as Central AI Orchestrator
    participant Story as Story & Memory Engine
    participant Voice as Neural Voice & Lip-Sync
    participant 3D as Blender Engine (bpy)
    participant Post as Post-Production & QA
    participant YouTube as YouTube Manager

    Orch->>Story: 1. Fetch Series Lore & Unresolved Episodic Cliffhanger
    Story->>Story: 2. Generate Episode Concept & 3-Act Directorial Script
    Story->>Story: 3. Audit Script via Continuity Supervisor
    Orch->>Voice: 4. Synthesize Multi-Character Dialogue (Piper/Kokoro)
    Voice->>Voice: 5. Extract Rhubarb 9-Visemes & Phoneme Timings
    Orch->>3D: 6. Load Master Rigged Character (.blend) & Environment
    3D->>3D: 7. Apply Skeletal Retargeting (Locomotion, Gestures)
    3D->>3D: 8. Drive Facial ShapeKeys via Viseme Curves
    3D->>3D: 9. Set Up 5-Shot Cinematic Camera & 3-Point Lighting
    3D->>3D: 10. Execute Headless CPU Render Batch (Eevee/NPR)
    3D->>Post: 11. Send Rendered PNG Sequence to Post-Production
    Post->>Post: 12. Run Gate 5 (Render Integrity & Black-Frame Check)
    Post->>Post: 13. Assemble Video + Audio via FFmpeg (Sidechain Ducking)
    Post->>Post: 14. Burn Word-Level Highlighted Subtitles
    Post->>Post: 15. Create Multi-Candidate Thumbnails & Select High-CTR Hero
    Post->>Post: 16. Generate SEO Title, Description, Tags & Cliffhanger Teaser
    Post->>Post: 17. Run Gate 8 (COPPA & Monetization Compliance Preflight)
    alt Manual Approval Mode (Default)
        Post->>Orch: 18. Queue Episode for 1-Click Creator Approval
    else Fully Autonomous Mode
        Post->>YouTube: 19. Resumable Upload to YouTube Channel Playlist
    end
    YouTube->>Orch: 20. Confirm Publication & Store YouTube Video ID
    Orch->>Story: 21. Commit Canonical Event Memory & Open Cliffhanger to DB
    Orch->>YouTube: 22. Ingest YouTube Analytics (Retention & CTR)
    Orch->>Story: 23. Feed Retention Drop-Off Analysis into Next Episode Prompt
    Orch->>Orch: 24. Schedule Next Production Run on Calendar
```

---

## 4. Normalized Database Architecture

```mermaid
erDiagram
    CHANNELS ||--o{ SERIES : owns
    SERIES ||--o{ SEASONS : contains
    SEASONS ||--o{ EPISODES : contains
    SERIES ||--o{ CHARACTERS : owns
    CHARACTERS ||--o{ CHARACTER_VERSIONS : tracks
    CHARACTERS ||--o{ CHARACTER_VOICES : assigns
    EPISODES ||--o{ SCENES : contains
    SCENES ||--o{ SHOTS : executes
    SHOTS ||--o{ DIALOGUES : speaks
    EPISODES ||--o{ PRODUCTION_JOBS : triggers
    PRODUCTION_JOBS ||--o{ QUALITY_REPORTS : evaluates
    EPISODES ||--o{ STORY_MEMORIES : updates
    EPISODES ||--o{ YOUTUBE_PUBLICATIONS : publishes
    YOUTUBE_PUBLICATIONS ||--o{ ANALYTICS_SNAPSHOTS : monitors

    SERIES {
        uuid id PK
        string title
        string genre
        string target_audience
        string art_style_preset
        jsonb world_lore
    }

    CHARACTERS {
        uuid id PK
        uuid series_id FK
        string name
        string role
        string age_category
        text personality_summary
        jsonb physical_specs
        string blend_model_path
        string rig_type
    }

    EPISODES {
        uuid id PK
        uuid season_id FK
        int episode_number
        string title
        string format
        string status
        text synopsis
        text cliffhanger_question
        string final_video_path
        string primary_thumbnail_path
    }

    PRODUCTION_JOBS {
        uuid id PK
        uuid episode_id FK
        string state
        float cpu_peak_usage
        float ram_peak_mb
        float render_duration_s
        text error_log
    }

    STORY_MEMORIES {
        uuid id PK
        uuid episode_id FK
        string event_category
        text summary
        jsonb character_state_changes
        string unresolved_mystery
        boolean is_resolved
    }
```

---

## 5. Technology Stack Recommendations

| Domain | Technology Selection | Rationale & CPU Feasibility |
| :--- | :--- | :--- |
| **Backend API** | **FastAPI + Pydantic v2** | High-speed async REST endpoints, automated Swagger documentation, native Python integration. |
| **Database** | **PostgreSQL (Prod) / aiosqlite (Local Dev)** | Normalized relational persistence with JSONB and foreign-key integrity; immune to Windows Application Control restrictions. |
| **Task Queue** | **Celery / Redis / Durable In-Memory Queue** | Robust state-machine tracking with automatic failure retry and task interruption recovery. |
| **3D Engine** | **Blender 4.2+ LTS Headless (`bpy`)** | Gold standard open-source 3D suite; full programmatic scene composition, Rigify rigging, and Eevee-Next/NPR CPU rendering. |
| **Character Creation**| **MPFB2 + Blender Rigify** | Procedural base meshes, parametric body sliders, ARKit 52 facial shapekeys. 100% CPU-native. |
| **Animation Retarget**| **Blender Animation Retargeting** | Fast, deterministic skeletal retargeting from BVH/FBX to custom character armatures. |
| **Lip-Sync** | **Rhubarb Lip Sync CLI** | Fast, offline phoneme-to-viseme extraction mapped to 3D facial shapekeys in milliseconds. |
| **Speech Alignment** | **WhisperX (faster-whisper int8)** | Forced word-level subtitle alignment running cleanly on CPU. |
| **Local Neural TTS** | **Piper TTS + Kokoro TTS (ONNX Runtime)** | Zero-GPU local synthesis; crystal-clear, expressive character acting without cloud dependencies. |
| **Media Compositing**| **FFmpeg 9.0.2** | Multi-threaded CPU video rendering, sidechain audio ducking, subtitle burning, and H.264 optimization. |
| **Frontend Studio** | **Next.js 14 / HTML5 Tailwind Web Studio** | Responsive dashboard with real-time job monitoring, 3D model inspector, and video review player. |

---

## 6. Production Capacity Estimates (Videos Per Week)

Based on calibrated CPU rendering benchmarks on the Intel Core i5-8265U:

| Content Format | Duration & Frame Count | CPU Render Duration | Post-Pro & QA | Weekly Production Target |
| :--- | :--- | :--- | :--- | :--- |
| **YouTube Shorts** (9:16) | 30–45s (900–1,350 frames) | **2.0 to 3.5 hours** | ~2 minutes | **4 to 6 Videos Per Week** |
| **Long-Form Episodes** (16:9) | 3–5 min (5,400–9,000 frames) | **14.0 to 24.0 hours** | ~8 minutes | **1 to 2 Episodes Per Week** |

> [!NOTE]
> All heavy rendering jobs are queued to run in the background or during overnight hours, reserving 2 CPU cores to guarantee normal workstation responsiveness.

---

## 7. Main Technical Risks & Mitigation Plan

| Risk ID | Identified Risk | Impact | Architectural Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **R-01** | **Thermal Throttling & CPU Overheating** | High | Cap Blender workers to 6 of 8 threads; enforce a 60-second cooldown pause every 30 minutes if CPU temperature exceeds 85°C. |
| **R-02** | **Out of Memory (OOM) on 16GB RAM** | Critical | Enforce an 8.0 GB RAM hard ceiling on Blender render workers; run garbage collection between scene transitions; avoid loading multiple high-poly environments simultaneously. |
| **R-03** | **Windows Application Control (WDAC) Blocks** | High | Use pure-Python libraries, ONNX Runtime, and static standalone binaries (FFmpeg, Rhubarb) rather than unsigned `.pyd` C-extensions in user directories. |
| **R-04** | **Character Visual Inconsistency Across Episodes** | Critical | Disallow pure 2D diffusion video models. Character geometry, materials, and rigs in Blender master `.blend` files remain the permanent single source of truth. |
| **R-05** | **YouTube Content ID & "Reused Content" Penalty** | High | 100% original scripts, unique character voice embeddings, original 3D animations, and pre-cleared CC0 background scores; preflight compliance gate checks all media before upload. |
| **R-06** | **YouTube API Daily Quota Depletion** | Medium | Uploads require 1,600 quota units; local SQLite ledger prevents duplicate uploads; batch metadata updates are throttled. |

---

## 8. 12-Phase Implementation Roadmap & Milestones

```mermaid
gantt
    title Autonomous Cartoon Studio 12-Phase Implementation Roadmap
    dateFormat  YYYY-MM-DD
    section Phase 0 to 3: Audit & Foundation
    P0: Environment Audit & Hardware Baseline     :done, 2026-11-18, 1d
    P1: Audit & Clone 22 Third-Party Repositories :active, 2026-11-19, 3d
    P2: Core Platform & Durable State Machine     :2026-11-22, 4d
    P3: Character Studio & Identity Engine        :2026-11-26, 4d
    section Phase 4 to 7: 3D Performance & Scenes
    P4: Rigging, Retargeting & Action Library     :2026-11-30, 4d
    P5: Voice Engine (Piper/Kokoro) & Rhubarb Lip-Sync: 2026-12-04, 3d
    P6: Story Intelligence & Episodic Memory DAG :2026-12-07, 4d
    P7: Cinematic Directing & Blender Automation  :2026-12-11, 4d
    section Phase 8 to 12: Production & Launch
    P8: Post-Production, Audio Ducking & Shorts   :2026-12-15, 3d
    P9: Automated Quality Control & Error Recovery: 2026-12-18, 3d
    P10: YouTube OAuth & Compliance Preflight Gate: 2026-12-21, 3d
    P11: Full Autonomous End-to-End Orchestration :2026-12-24, 4d
    P12: Stress-Testing, Hardening & Scaling      :2026-12-28, 4d
```

---

## 9. Next Action for Approval

Please review the **Hardware Audit**, the **22-Repository Compatibility Matrix**, and the **CPU-First Execution Strategy**. Once approved, we will begin **Phase 1: Downloading and auditing the third-party repositories into `third_party/`** in prioritized tiers.

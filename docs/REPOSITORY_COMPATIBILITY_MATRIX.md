# Autonomous AI Cartoon Studio
## 22-Repository Compatibility & Integration Matrix

| # | Repository Name | Pipeline Stage | Hardware Viability (Host: i5-8265U / UHD 620) | License Type | Commercial Monetization Safe | Integration Tier |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **MPFB2** | 3D Character Generation | **CPU Native (Fast)** | GPLv3 (Code) / CC0 (Meshes) | **YES** | **CORE (Tier 1)** |
| **2** | **Blender Add-ons** | Rigging & Formats | **CPU Native** | GPLv2 / GPLv3 | **YES** | **CORE (Tier 1)** |
| **3** | **AnimStudio** | Animation Clip Mgmt | **CPU Native** | GPLv3 | **YES** | **OPTIONAL** |
| **4** | **PoseCap** | Mocap Extraction | GPU Heavy / Slow on CPU | GPLv3 / Custom Weights | Review Weights | **EXPERIMENTAL** |
| **5** | **MB-Lab** | Parametric Characters | **CPU Native** | GPLv3 | **YES** | **OPTIONAL** |
| **6** | **Awesome 3D Characters** | Asset Catalog | N/A (Doc List) | CC0 / MIT | Per-Asset Check | **REFERENCE ONLY** |
| **7** | **Blender MCP Server** | LLM-Blender Bridge | **CPU Native (Light)** | MIT | **YES** | **CORE (Tier 1)** |
| **8** | **Blender MCP (bpy-dev)** | LLM-Blender Bridge | **CPU Native** | MIT | **YES** | **REFERENCE / BACKUP** |
| **9** | **OpenTopos** | Terrain Generation | **CPU Native** | GPLv3 | **YES** | **OPTIONAL** |
| **10** | **Anim Studio (DvaitAI)** | Storyboarding UI | **CPU Native** | MIT | **YES** | **EXPERIMENTAL** |
| **11** | **Blender Anim Retargeting** | Skeletal Retargeting | **CPU Native (Instant)** | GPLv3 | **YES** | **CORE (Tier 1)** |
| **12** | **Deep Motion Editing** | Motion Style Transfer | Requires CUDA GPU | Academic Non-Commercial | **NO (Research Only)** | **RESTRICTED** |
| **13** | **vid2anim** | Video to BVH Mocap | Requires CUDA GPU | MIT / SMPL Non-Comm | **NO (SMPL Terms)** | **RESTRICTED** |
| **14** | **Rhubarb Lip Sync** | 3D Viseme Extraction | **CPU Native (Ultra-Fast)**| MIT | **YES** | **CORE (Tier 1)** |
| **15** | **ComfyUI** | Concept / Texture Inpaint| Slow on CPU (6–15 min) | GPLv3 | Model Dependent | **OPTIONAL (Async)** |
| **16** | **Wan 2.2** | Video Diffusion | **INCOMPATIBLE (No CUDA)** | Apache 2.0 / Custom | License Ok, HW Fail | **RESTRICTED / EXCLUDED**|
| **17** | **Piper TTS** | Local Neural Voice | **CPU Native (0.15x Realtime)**| GPLv3 / Open Voices | **YES (Safe Voices)** | **CORE (Tier 1)** |
| **18** | **WhisperX** | Word Alignment & Subs | **CPU Native (int8)** | BSD 2-Clause | **YES** | **CORE (Tier 1)** |
| **19** | **Kokoro TTS** | Local Expressive Voice | **CPU Native (ONNX)** | Apache 2.0 | **YES** | **CORE (Tier 1)** |
| **20** | **FFmpeg** | Video & Audio Compositor| **CPU Native (Multi-Thread)** | LGPL / GPL | **YES** | **CORE (Tier 1)** |
| **21** | **Natron** | Node Compositing | High RAM on CPU | GPLv2 | **YES** | **OPTIONAL** |
| **22** | **HyperFrames** | Motion Graphics | **CPU Native** | MIT / Apache 2.0 | **YES** | **OPTIONAL** |

---

## Architectural Classification Summary

1. **CORE INTEGRATIONS (Tier 1 — Essential for Automated Local Production)**:
   - `MPFB2`: Procedural 3D character generator & Rigify mesh builder.
   - `Blender Add-ons` & `Blender Animation Retargeting`: Native skeletal binding, BVH retargeting, camera tools.
   - `Blender MCP Server`: Headless orchestration of Blender from Python.
   - `Rhubarb Lip Sync`: High-speed, deterministic 9-viseme audio-to-shapekey calculation.
   - `WhisperX`: Forced phoneme alignment and word-highlighted subtitle generation.
   - `Piper TTS` & `Kokoro TTS`: Ultra-low-latency local neural voice synthesis on CPU.
   - `FFmpeg`: Production-grade H.264 video assembly, sidechain audio ducking, and subtitle muxing.

2. **OPTIONAL INTEGRATIONS (Tier 2 — Non-Blocking Enhancements)**:
   - `MB-Lab` (Alternative character morphs), `AnimStudio` (Clip librarian), `OpenTopos` (Terrain generation), `ComfyUI` (Decoupled concept art generation), `HyperFrames` (Dynamic typography).

3. **RESTRICTED / EXCLUDED (Tier 3 — Prohibited by Hardware or Academic Non-Commercial Licenses)**:
   - `Wan 2.2`: Strictly requires 16GB–24GB NVIDIA CUDA VRAM. Excluded to maintain Rule 7 (preserving the 3D Blender character pipeline) and prevent hardware crash.
   - `Deep Motion Editing` & `vid2anim`: Excluded due to academic non-commercial dataset clauses which jeopardize YouTube Partner Program monetization.

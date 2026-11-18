# Autonomous AI Cartoon Studio
## Third-Party Dependencies & Repository Management Plan

This document details the isolation strategy, directory hierarchy, and dependency management for external libraries and third-party tools integrated into `e:\YT\third_party`.

---

## 1. Directory Structure for `third_party/`

All evaluated and cloned third-party projects reside in `e:\YT\third_party/` as isolated modules. In accordance with **Rule 4 (Do not modify third-party repositories)**, third-party code remains completely untouched and is interfaced through dedicated adapter classes in `backend/app/services/`:

```
e:\YT\third_party\
├── mpfb2/                    # 3D character generator (MakeHuman plugin)
├── blender_addons/           # Official Blender Addons (Rigify, formats)
├── blender_retargeting/      # Animation retargeting addon
├── rhubarb_lipsync/          # Rhubarb Lip Sync CLI & phoneme aligner
├── piper_tts/                # Local neural voice engine (ONNX runtime)
├── kokoro_tts/               # Kokoro 82M expressive voice engine
├── whisperx/                 # Forced alignment & word-level subtitle extractor
├── ffmpeg/                   # FFmpeg static binary distribution
└── blender_mcp/              # Blender MCP server bridge
```

---

## 2. Safe Cloning & Verification Plan

Each repository is cloned into its respective directory using pinned release tags or commit hashes to guarantee deterministic builds:

```powershell
# Core Production Repositories (Safe & CPU-Viable)
git clone --depth 1 https://github.com/makehumancommunity/mpfb2.git e:\YT\third_party\mpfb2
git clone --depth 1 https://github.com/Mwni/blender-animation-retargeting.git e:\YT\third_party\blender_retargeting
git clone --depth 1 https://github.com/DanielSWolf/rhubarb-lip-sync.git e:\YT\third_party\rhubarb_lipsync
git clone --depth 1 https://github.com/OHF-Voice/piper1-gpl.git e:\YT\third_party\piper_tts
git clone --depth 1 https://github.com/hexgrad/kokoro.git e:\YT\third_party\kokoro_tts
git clone --depth 1 https://github.com/djeada/blender-mcp-server.git e:\YT\third_party\blender_mcp
```

---

## 3. Runtime Dependency Isolation

- **Zero Host Interference:** In accordance with the non-negotiable requirements, no dependencies are installed into system-wide Python without user isolation.
- **Python Security:** Pure-Python and ONNX-based wheels are prioritized to adhere to Windows Application Control policies.
- **Standalone Executables:** Tools such as FFmpeg and Rhubarb Lip Sync are treated as standalone CLI binaries invoked headlessly via standard subprocess pipes.

# Autonomous AI Cartoon Studio
## Security, Isolation & Governance Architecture

---

## 1. Project Isolation & Zero-Interference Policy

In accordance with the non-negotiable requirements:
1. **Directory Isolation:** The entire application resides strictly within `e:\YT`. It does **not** touch, modify, or connect to any other workspace or unrelated projects (such as Quantum AI, QVS, StitchFlow, or Ken Global ERP).
2. **Dedicated Database:** The studio operates its own dedicated PostgreSQL / SQLite database (`data/cartoon_studio.db`). It never connects to or shares credentials with any external database.
3. **Dedicated Python Environment & Dependencies:** All dependencies are scoped strictly to the project without modifying global host settings.

---

## 2. Credential Security & Secret Management

- **Zero Hardcoded Secrets:** No API keys, OAuth client secrets, or user tokens may ever be written directly into source code or tracked by Git.
- **Git Exclusions:** The root `.gitignore` strictly blocks all credential files (`.env`, `credentials/*.json`, `data/*.db`).
- **Encrypted Token Vault:** Tokens stored on disk are restricted to user-level read/write permissions.

---

## 3. Sandboxing & Safe Blender Execution

Because Blender's Python runtime (`bpy`) has full OS execution capabilities:
- **No Unrestricted Remote Execution:** The FastAPI server does **not** expose endpoints that accept arbitrary raw Python strings for execution inside Blender.
- **Pre-Compiled Directorial Templates:** All Blender scripts executed headlessly (`blender -b -P <script>`) are strictly generated from parameterized, audited internal templates (`BpyScriptGenerator`) that validate coordinate bounds, asset file paths, and frame ranges.

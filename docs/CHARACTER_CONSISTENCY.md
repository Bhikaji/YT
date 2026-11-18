# Autonomous AI Cartoon Studio
## Character Identity Permanence & Consistency Engine

---

## 1. The Principle of Geometric Permanence

A recurring character in a successful animated series must **never randomly morph, shift facial proportions, change hair color, or alter vocal timbre between scenes or episodes**. 

While 2D generative diffusion models suffer from constant frame-to-frame hallucination and identity degradation, our studio enforces **100% Geometric Permanence** by establishing master 3D assets inside Blender as the single source of truth:

```
[Master 3D Asset: character_master.blend]
      │
      ├──> Quad Geometry & Mesh Topology (Indexed Vertex Coordinates)
      ├──> Skeletal Armature (Standard Rigify Metarig with IK/FK Controls)
      ├──> Facial Performance Layer (52 FACS / ARKit Standard ShapeKeys)
      ├──> Stylized PBR / NPR Material Node Trees (Permanent Color Palettes)
      └──> Pinned Neural Voice Embedding Vector (128-dim Timbre Signature)
```

---

## 2. Character Identity Profile Specification

Every character created by the system receives a permanent identity profile stored in `database/`:

```json
{
  "character_id": "char_leo_001",
  "name": "Leo",
  "series_id": "series_shadow_island",
  "version": 1,
  "role": "PROTAGONIST",
  "age_category": "TEEN",
  "mesh_hash": "e9b2a74c1f93...",
  "master_blend_path": "assets/characters/leo_master.blend",
  "rig_type": "RIGIFY_ARKit52",
  "physical_specs": {
    "head_to_body_ratio": "1:4.8",
    "hair_style": "sculpted_brown_clumps",
    "eye_color": "emerald_green_radial",
    "facial_features": ["freckles_nose_bridge", "soft_blush_cheeks"],
    "costume_preset": "red_explorer_hoodie_v1"
  },
  "voice_identity": {
    "provider": "piper_kokoro",
    "voice_id": "en_US-leo-expressive",
    "base_pitch_hz": 120,
    "timbre_embedding_hash": "f48c9032..."
  }
}
```

---

## 3. ARKit 52 Standard Facial ShapeKey Mapping

All characters incorporate the standard 52 FACS (Facial Action Coding System) shapekeys to guarantee compatibility with Rhubarb Lip-Sync and emotional acting drivers:

| Category | Primary ShapeKeys | Expressive Function |
| :--- | :--- | :--- |
| **Jaw & Mouth** | `jawOpen`, `mouthClose`, `mouthFunnel`, `mouthPucker`, `mouthSmileLeft`, `mouthSmileRight`, `mouthFrownLeft`, `mouthFrownRight`, `mouthDimpleLeft`, `mouthDimpleRight` | Phoneme lip-synchronization, smiling, smirking, yelling, shouting. |
| **Brows & Forehead**| `browInnerUp`, `browDownLeft`, `browDownRight`, `browOuterUpLeft`, `browOuterUpRight` | Shock, anger, suspicion, curiosity, sadness. |
| **Eyes & Cheeks** | `eyeBlinkLeft`, `eyeBlinkRight`, `eyeWideLeft`, `eyeWideRight`, `eyeSquintLeft`, `eyeSquintRight`, `cheekPuff`, `cheekSquintLeft`, `cheekSquintRight` | Blinking, wide-eyed wonder, terrified dilation, laughing cheek squeeze. |
| **Nose & Tongue** | `noseSneerLeft`, `noseSneerRight`, `tongueOut` | Disgust, playful teasing, subtle breathing. |

---

## 4. Controlled Versioning Protocol

A character's physical model may only be updated when explicitly demanded by the narrative arc (e.g., *Leo acquires an ancient golden gauntlet in Episode 4*).

When this occurs:
1. A new immutable record is created in `character_versions`.
2. The change rationale is linked directly to the triggering `episode_id`.
3. The previous master mesh remains archived to enable flashbacks or continuity verification.

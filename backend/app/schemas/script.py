from typing import List, Optional, Tuple, Dict, Any
from pydantic import BaseModel, Field

class CameraShotCue(BaseModel):
    shot_type: str = "ESTABLISHING"  # ESTABLISHING, MEDIUM_TWO_SHOT, CLOSE_UP, OVER_SHOULDER, TRACKING
    target_character_id: Optional[str] = None
    camera_pos: Tuple[float, float, float] = (0.0, -4.0, 1.6)
    target_focus_pos: Tuple[float, float, float] = (0.0, 0.0, 1.4)
    focal_length_mm: float = 35.0
    shake_intensity: float = 0.0  # Procedural camera shake (0.0 to 1.0)

class CharacterActionCue(BaseModel):
    character_id: str
    action_name: str  # walk, run, jump, idle_suspense, punch, talk_excited
    start_second: float
    end_second: float
    start_pos: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    end_pos: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation_z_deg: float = 0.0
    facial_expression: str = "neutral"  # smile, scared, angry, shocked

class DialogueCue(BaseModel):
    character_id: str
    character_name: str
    text: str
    emotion: str = "neutral"  # whisper, excited, terrified, laughing, sarcastic
    start_second: float

class SoundEffectCue(BaseModel):
    sfx_type: str  # footsteps, cave_drip, dramatic_boom, door_creak, punch_hit
    start_second: float
    volume: float = 0.8

class ScriptScene(BaseModel):
    scene_number: int
    environment: str = "mysterious_ruins"
    lighting_preset: str = "dramatic_sunset"
    duration_seconds: float = 6.0
    camera_shots: List[CameraShotCue] = Field(default_factory=list)
    actions: List[CharacterActionCue] = Field(default_factory=list)
    dialogues: List[DialogueCue] = Field(default_factory=list)
    sound_effects: List[SoundEffectCue] = Field(default_factory=list)

class GeneratedEpisodeScript(BaseModel):
    series_title: str
    episode_number: int
    episode_title: str
    format: str = "SHORT"
    synopsis: str
    cliffhanger_question: str
    next_episode_teaser: str
    scenes: List[ScriptScene] = Field(default_factory=list)
    story_memory_updates: Dict[str, Any] = Field(default_factory=dict)

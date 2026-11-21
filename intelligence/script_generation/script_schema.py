from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class DialogueLine(BaseModel):
    speaker_id: str
    speaker_name: str
    text: str
    emotion: str = "curious"  # happy, sad, angry, surprised, shocked, confused, etc.
    start_second: float
    end_second: float

class SceneAction(BaseModel):
    character_id: str
    action_type: str  # walk, run, point, wave, think, slapstick_react, jump, type, inspect
    gesture: str
    facial_expression: str
    start_second: float
    end_second: float

class ScriptScene(BaseModel):
    scene_id: int
    environment: str  # modern_office, science_lab, classroom, street, mall, space_station, etc.
    start_second: float
    end_second: float
    description: str
    camera_movement: str = "STATIC"  # ZOOM_IN, ZOOM_OUT, PAN_LEFT, PAN_RIGHT, SHAKE, REACTION_CUT
    dialogues: List[DialogueLine] = []
    actions: List[SceneAction] = []
    sound_effects: List[str] = []
    prop_interactions: List[Dict[str, Any]] = []

class StickFigureScript(BaseModel):
    title: str
    topic: str
    category: str
    hook: str  # 0-3s
    situation: str  # 3-7s
    development: str  # 7-14s
    conflict: str  # 14-21s
    payoff: str  # 21-27s
    ending_cta: str  # 27-30s
    total_duration: float = 30.0
    cast: List[Dict[str, Any]]
    scenes: List[ScriptScene]
    quality_score: float = 0.0
    fact_check_verified: bool = True

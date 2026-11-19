import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # e:\YT

class Settings(BaseSettings):
    PROJECT_NAME: str = "Autonomous AI Cartoon Studio"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment & Paths
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"
    ASSETS_DIR: Path = BASE_DIR / "assets"
    OUTPUT_DIR: Path = BASE_DIR / "output"
    SCRIPTS_DIR: Path = BASE_DIR / "scripts"
    
    # Animation Engine Mode:
    # 'LOCAL_DIFFUSION' (100% Free Local Open-Source AI Video on your GPU - LTX-Video / Wan 2.1)
    # 'VEO_AI' (Google Veo 3 / Veo 2 / Gemini AI video generation)
    # 'BLENDER_3D' (Blender 4.2 LTS EEVEE-Next procedural character engine)
    # 'AI_PIXAR' (Pixar Neural Diffusion keyframes)
    ANIMATION_ENGINE_MODE: str = "LOCAL_DIFFUSION"
    LOCAL_DIFFUSION_MODEL: str = "Lightricks/LTX-Video"
    LOCAL_DIFFUSION_DEVICE: str = "cuda"
    
    # Cloud & Remote Options
    VEO_MODEL: str = "veo-3.1-fast-generate-preview"
    VEO_FALLBACK_MODEL: str = "veo-2.0-generate-001"
    VEO_RESOLUTION: str = "720p"
    WAN21_API_URL: Optional[str] = None  # Free Google Colab Gradio endpoint for 100% free unlimited video generation
    
    # Database
    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR / 'data' / 'cartoon_studio.db'}"
    
    # Blender Configuration
    BLENDER_EXECUTABLE_PATH: Optional[str] = str(BASE_DIR / "tools" / "blender" / "Blender Foundation" / "Blender 4.5" / "blender.exe")
    BLENDER_DEFAULT_RENDER_ENGINE: str = "BLENDER_EEVEE_NEXT"  # or CYCLES
    BLENDER_RENDER_SAMPLES: int = 32
    BLENDER_FPS: int = 30
    BLENDER_RESOLUTION_LONG: tuple = (1920, 1080)   # 16:9
    BLENDER_RESOLUTION_SHORT: tuple = (1080, 1920)  # 9:16
    
    # Voice & Audio
    DEFAULT_TTS_PROVIDER: str = "edge_tts"  # 'edge_tts' (free/high quality), 'elevenlabs', 'mock'
    ELEVENLABS_API_KEY: Optional[str] = None
    
    # AI Story & LLM Provider
    GEMINI_API_KEY: Optional[str] = None
    DEFAULT_LLM_MODEL: str = "gemini-1.5-flash"
    
    # YouTube Publishing Settings
    YOUTUBE_CLIENT_SECRETS_FILE: Optional[str] = str(BASE_DIR / "credentials" / "client_secret.json")
    YOUTUBE_OAUTH_TOKEN_FILE: Optional[str] = str(BASE_DIR / "credentials" / "youtube_token.json")
    DEFAULT_PUBLISH_MODE: str = "MANUAL_APPROVAL"  # 'MANUAL_APPROVAL' or 'FULLY_AUTONOMOUS'
    ENABLE_COPPA_STRICT_MODE: bool = True
    
    # Operational Budget & Limits
    MONTHLY_BUDGET_LIMIT_USD: float = 50.00
    COST_TRACKING_ENABLED: bool = True

    class Config:
        env_file = str(BASE_DIR / ".env")
        case_sensitive = True

settings = Settings()

# Ensure required directories exist
for folder in [
    settings.DATA_DIR,
    settings.ASSETS_DIR / "characters",
    settings.ASSETS_DIR / "environments",
    settings.ASSETS_DIR / "actions",
    settings.ASSETS_DIR / "audio" / "voices",
    settings.ASSETS_DIR / "audio" / "music",
    settings.ASSETS_DIR / "audio" / "sfx",
    settings.ASSETS_DIR / "thumbnails",
    settings.OUTPUT_DIR / "episodes",
    settings.OUTPUT_DIR / "shorts",
    settings.OUTPUT_DIR / "renders",
    BASE_DIR / "credentials",
]:
    folder.mkdir(parents=True, exist_ok=True)

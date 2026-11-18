from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.database import init_db
from backend.app.api.v1.routes import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Database tables
    await init_db()
    print(f"[{settings.PROJECT_NAME}] Database initialized at {settings.DATABASE_URL}")
    yield
    # Shutdown
    print(f"[{settings.PROJECT_NAME}] Server shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Autonomous AI 3D Cartoon Studio & YouTube Automation Platform API",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import FileResponse

# Mount Output & Assets folders for direct media streaming/preview
app.mount("/output", StaticFiles(directory=str(settings.OUTPUT_DIR)), name="output")
app.mount("/assets", StaticFiles(directory=str(settings.ASSETS_DIR)), name="assets")
app.mount("/static", StaticFiles(directory=str(settings.BASE_DIR / "backend" / "app" / "static")), name="static")

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
@app.get("/studio")
def root():
    index_file = settings.BASE_DIR / "backend" / "app" / "static" / "index.html"
    return FileResponse(str(index_file))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)

import os
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from routes.analyze import router as analyze_router


def create_app() -> FastAPI:
    app = FastAPI(title="Multimodal Fake News Detection API", version="1.0.0")

    allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    allowed_origins = [o.strip() for o in allowed_origins if o.strip()]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(analyze_router)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()


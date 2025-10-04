from __future__ import annotations

import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.health import router as health_router
from app.routers.suggest import router as suggest_router
from app.routers.chat import router as chat_router


def _get_allowed_origins_from_env() -> List[str]:
    """Read ALLOWED_ORIGINS env variable as a comma-separated list. Defaults to localhost:3000."""
    raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").strip()
    # Split by comma and strip whitespace
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    - Configures CORS using ALLOWED_ORIGINS env (default http://localhost:3000)
    - Registers API routers for health, chat, suggest
    - Provides OpenAPI metadata and tags
    """
    app = FastAPI(
        title="AI Copilot Backend",
        description="FastAPI backend exposing health, suggestions, and OpenAI-integrated chat.",
        version="0.2.0",
        openapi_tags=[
            {"name": "Health", "description": "Service health checks."},
            {"name": "Chat", "description": "Chat with the AI Copilot."},
            {"name": "Suggest", "description": "Get suggested prompts."},
        ],
    )

    # CORS configuration from environment
    allow_origins = _get_allowed_origins_from_env()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers under /api
    app.include_router(health_router, prefix="/api")
    app.include_router(chat_router, prefix="/api")
    app.include_router(suggest_router, prefix="/api")

    return app


# FastAPI expects an 'app' variable as the ASGI application entrypoint.
app = create_app()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.config import get_settings
from src.api.routers.chat import router as chat_router
from src.api.routers.suggest import router as suggest_router

settings = get_settings()

app = FastAPI(
    title="AI Copilot Backend",
    description="Backend API for AI Copilot logic and integration.",
    version="0.1.0",
    openapi_tags=[
        {"name": "Chat", "description": "Chat with the AI Copilot."},
        {"name": "Suggest", "description": "Get suggested prompts."},
        {"name": "Health", "description": "Service health checks."},
    ],
)

# Build allow_origins list by combining configured env list with localhost:3000 for React dev
allow_origins = list(settings.cors_origins)
if "*" not in allow_origins and "http://localhost:3000" not in allow_origins:
    allow_origins.append("http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/api/health",
    tags=["Health"],
    summary="Health check",
    description="Returns a simple JSON payload indicating that the service is running.",
)
def health_check():
    """
    Health check endpoint.

    Returns:
    - JSON object: {"status": "ok"}
    """
    return {"status": "ok"}


# Include routers
app.include_router(chat_router)
app.include_router(suggest_router)

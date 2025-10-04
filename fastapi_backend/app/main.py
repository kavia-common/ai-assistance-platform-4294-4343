from __future__ import annotations

from typing import List

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    - Registers CORS allowing http://localhost:3000 for the React dev server
    - Adds basic /api routes: health, chat, suggest
    - Provides OpenAPI metadata and tags
    """
    app = FastAPI(
        title="AI Copilot Backend",
        description="Clean FastAPI boilerplate with basic /api routes.",
        version="0.1.0",
        openapi_tags=[
            {"name": "Health", "description": "Service health checks."},
            {"name": "Chat", "description": "Simple placeholder chat endpoint."},
            {"name": "Suggest", "description": "Static suggestions list."},
        ],
    )

    # CORS: allow frontend dev origin
    allow_origins = ["http://localhost:3000"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Schemas local to this minimal app
    class ChatIn(BaseModel):
        message: str = Field(..., description="User message to send to the assistant.")

    class ChatOutMessage(BaseModel):
        role: str = Field("assistant", description="Role of the response author.")
        content: str = Field(..., description="Assistant content.")

    class ChatOut(BaseModel):
        message: ChatOutMessage

    @app.get(
        "/api/health",
        tags=["Health"],
        summary="Health check",
        description="Returns a simple JSON payload indicating that the service is running.",
    )
    def health_check():
        """Health check endpoint.
        Returns:
        - JSON object: {"status": "ok"}
        """
        return {"status": "ok"}

    @app.post(
        "/api/chat",
        tags=["Chat"],
        response_model=ChatOut,
        status_code=status.HTTP_200_OK,
        summary="Chat with the assistant (placeholder)",
        description="Accepts a single message and returns a deterministic placeholder assistant reply.",
    )
    def chat_endpoint(payload: ChatIn) -> ChatOut:
        """Placeholder chat endpoint.
        Parameters:
        - payload: ChatIn with { message: string }
        Returns:
        - ChatOut: { "message": {"role": "assistant", "content": "Hello"} }
        """
        # Minimal deterministic placeholder response
        return ChatOut(message=ChatOutMessage(role="assistant", content="Hello"))

    @app.get(
        "/api/suggest",
        tags=["Suggest"],
        response_model=List[str],
        status_code=status.HTTP_200_OK,
        summary="Fetch suggestion prompts",
        description="Returns a static list of suggested prompts to help users get started.",
    )
    def suggest_endpoint() -> List[str]:
        """Get a list of suggested prompts."""
        return ["Try asking about the weather", "Ask for a code review", "Summarize a document"]

    return app


# FastAPI expects an 'app' variable as the ASGI application entrypoint.
app = create_app()

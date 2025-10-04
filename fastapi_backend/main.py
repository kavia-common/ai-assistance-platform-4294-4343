from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """Create and configure the FastAPI application with CORS and routes.
    
    Returns:
        FastAPI: Configured FastAPI app exposing /api/health.
    """
    app = FastAPI(
        title="AI Copilot Backend",
        description="Backend API for AI Copilot logic and integration.",
        version="0.1.0",
        openapi_tags=[
            {"name": "Health", "description": "Service health checks."},
        ],
    )

    # Allow the local React dev server on port 3000 by default.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
        max_age=600,
    )

    @app.get(
        "/api/health",
        tags=["Health"],
        summary="Health check",
        description="Returns 200 OK to indicate the service is running.",
        responses={200: {"description": "Healthy"}},
    )
    # PUBLIC_INTERFACE
    async def health():
        """Health endpoint.
        
        Returns:
            dict: a basic info payload (clients treat any HTTP 200 as 'ok').
        """
        return {"status": "ok"}

    return app


# For local running: uvicorn main:app --port 3001
app = create_app()

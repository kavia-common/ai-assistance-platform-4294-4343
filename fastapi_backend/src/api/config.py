"""
Configuration module for the FastAPI backend.

Loads configuration from environment variables with sensible defaults.
Use an .env file managed by the orchestrator to set values in different environments.

Environment variables:
- BACKEND_PORT: Port to run the backend server on. Default: 8000
- CORS_ORIGINS: Comma-separated list of allowed CORS origins. Default: *
  Notes:
    - If "*" is used, all origins are allowed.
    - The application will ensure "http://localhost:3000" is permitted for local
      React development even if not present in CORS_ORIGINS.
- MODEL_PROVIDER: Placeholder for AI model provider name. Default: "local"
  Examples: "local", "openai", "azure", etc. Not implemented yet, only documented.
- OPENAI_API_KEY: Placeholder for OpenAI provider key (if MODEL_PROVIDER=openai).
  This is only a placeholder for future integration. Do not set or use here.
"""

from __future__ import annotations

import os
from typing import List


class Settings:
    """Application settings loaded from environment variables.

    Attributes:
    - backend_port: int
        Port to run the backend server on (env: BACKEND_PORT, default 8000)
    - cors_origins: list[str]
        Allowed origins for CORS (env: CORS_ORIGINS, default "*").
        Note: main.py ensures "http://localhost:3000" is allowed in addition
        to any configured origins for React dev UX.
    - model_provider: str
        Placeholder selection for future model backends (env: MODEL_PROVIDER, default "local")
    - openai_api_key: Optional[str]
        Placeholder for a future OpenAI integration (env: OPENAI_API_KEY).
        Not used at runtime currently; documented only for future work.
    """

    def __init__(self) -> None:
        # Port used when starting the server (e.g., uvicorn)
        self.backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))

        # CORS origins can be "*" or a comma-separated list of origins
        cors_origins_env = os.getenv("CORS_ORIGINS", "*")
        if cors_origins_env.strip() == "*":
            self.cors_origins: List[str] = ["*"]
        else:
            self.cors_origins = [o.strip() for o in cors_origins_env.split(",") if o.strip()]

        # Placeholder for future provider selection (OpenAI, Azure, etc.)
        self.model_provider: str = os.getenv("MODEL_PROVIDER", "local")

        # Placeholder only; not consumed anywhere until provider integration lands
        # Keep this attribute documented to guide orchestrator/ops on needed env during rollout.
        self.openai_api_key: str | None = os.getenv("OPENAI_API_KEY")


# PUBLIC_INTERFACE
def get_settings() -> Settings:
    """Return a singleton-like Settings instance."""
    # Simple module-level cache without external deps.
    global _settings_instance  # type: ignore
    try:
        return _settings_instance  # type: ignore
    except NameError:
        _settings_local = Settings()
        _settings_instance = _settings_local  # type: ignore
        return _settings_local

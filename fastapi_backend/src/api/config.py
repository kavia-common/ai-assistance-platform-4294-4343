"""
Configuration module for the FastAPI backend.

Loads configuration from environment variables with sensible defaults.
Use an .env file managed by the orchestrator to set values in different environments.

Environment variables:
- BACKEND_PORT: Port to run the backend server on. Default: 8000
- CORS_ORIGINS: Comma-separated list of allowed CORS origins. Default: *
- MODEL_PROVIDER: Placeholder for AI model provider name. Default: "local"
"""

from __future__ import annotations

import os
from typing import List


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self) -> None:
        self.backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
        cors_origins_env = os.getenv("CORS_ORIGINS", "*")
        # Allow "*" or comma-separated list
        if cors_origins_env.strip() == "*":
            self.cors_origins: List[str] = ["*"]
        else:
            self.cors_origins = [o.strip() for o in cors_origins_env.split(",") if o.strip()]
        # Placeholder for future provider selection (OpenAI, etc.)
        self.model_provider: str = os.getenv("MODEL_PROVIDER", "local")


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

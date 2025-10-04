from __future__ import annotations

import os
from typing import List


def get_backend_port() -> int:
    """Get backend port from BACKEND_PORT env, default 3001."""
    raw = os.getenv("BACKEND_PORT", "3001")
    try:
        return int(raw)
    except ValueError:
        return 3001


def get_allowed_origins() -> List[str]:
    """Get allowed CORS origins from ALLOWED_ORIGINS comma-separated env."""
    raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
    return [o.strip() for o in raw.split(",") if o.strip()]


def get_openai_api_key() -> str | None:
    """Return OPENAI_API_KEY or None if unset."""
    return os.getenv("OPENAI_API_KEY")


def get_openai_model() -> str:
    """Return OPENAI_MODEL or a sensible default if unset."""
    # Prefer latest lightweight model if not specified.
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")

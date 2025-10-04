"""
Shared dependencies and utilities for routers and services.
"""

from __future__ import annotations

import uuid
from typing import Optional

from fastapi import Header


# PUBLIC_INTERFACE
async def get_session_id(x_session_id: Optional[str] = Header(default=None, alias="X-Session-ID")) -> str:
    """
    Get or generate a session ID from the X-Session-ID header.

    If the header is absent, a new UUID is generated to represent a session.
    """
    if x_session_id and x_session_id.strip():
        return x_session_id.strip()
    return str(uuid.uuid4())

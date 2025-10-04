from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Health check",
    description="Returns a simple JSON payload indicating that the service is running.",
)
# PUBLIC_INTERFACE
def health_check():
    """Health check endpoint.
    Returns:
    - JSON object: {"status": "ok"}
    """
    return {"status": "ok"}

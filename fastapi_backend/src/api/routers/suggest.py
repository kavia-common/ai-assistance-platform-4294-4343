"""
Suggest router exposing the /api/suggest endpoint.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.api.services.suggest_service import get_suggestions

router = APIRouter(
    prefix="/api",
    tags=["Suggest"],
)


@router.get(
    "/suggest",
    response_model=list[str],
    status_code=status.HTTP_200_OK,
    summary="Fetch suggestion prompts",
    description="Returns a static list of suggested prompts to help users get started.",
)
# PUBLIC_INTERFACE
async def suggest_endpoint() -> List[str]:
    """
    Get a list of suggested prompts.

    Returns:
    - List[str]: Array of suggestion strings.
    """
    try:
        suggestions = get_suggestions()
        return suggestions
    except Exception:
        # Keep a stable shape and code on unexpected failure
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=[])

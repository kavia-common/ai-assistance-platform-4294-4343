from __future__ import annotations

from typing import List
from fastapi import APIRouter, status

router = APIRouter(tags=["Suggest"])


@router.get(
    "/suggest",
    response_model=List[str],
    status_code=status.HTTP_200_OK,
    summary="Fetch suggestion prompts",
    description="Returns a static list of suggested prompts to help users get started.",
)
# PUBLIC_INTERFACE
def suggest_endpoint() -> List[str]:
    """Get a list of suggested prompts."""
    return [
        "Summarize the following text...",
        "Explain this code snippet...",
        "Draft a professional email about...",
        "Generate test cases for the following function...",
    ]

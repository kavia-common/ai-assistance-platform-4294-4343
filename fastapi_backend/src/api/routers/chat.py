"""
Chat router exposing the /api/chat endpoint.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse

from src.api import deps
from src.api.schemas import ChatRequest, ChatResponse, ErrorResponse
from src.api.services.chat_service import process_chat

router = APIRouter(
    prefix="/api",
    tags=["Chat"],
)


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with the AI Copilot",
    description="Send chat history and an optional prompt. Returns a deterministic assistant response.",
    responses={
        200: {"description": "Successful assistant response", "model": ChatResponse},
        400: {"description": "Bad Request", "model": ErrorResponse},
        500: {"description": "Internal Server Error", "model": ErrorResponse},
    },
)
# PUBLIC_INTERFACE
async def chat_endpoint(
    payload: ChatRequest,
    session_id: str = Depends(deps.get_session_id),
    x_session_id_raw: str | None = Header(default=None, alias="X-Session-ID"),
) -> ChatResponse:
    """
    Chat endpoint.

    Parameters:
    - payload: ChatRequest containing messages and optional prompt.
    - X-Session-ID header (optional): Client-provided session ID. A new UUID is generated if not provided.

    Returns:
    - ChatResponse containing the assistant's message.
    """
    try:
        # Basic validation
        if payload is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payload is required")

        return process_chat(session_id=session_id, request=payload)
    except HTTPException:
        # Pass-through for deliberate HTTP errors
        raise
    except Exception:
        # Consistent error shape
        err = ErrorResponse(detail="Unexpected error during chat processing", code="chat_internal_error")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=err.model_dump())

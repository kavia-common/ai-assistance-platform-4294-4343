from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse

from app.models.schemas import ChatRequest, ChatResponse, Message, ErrorResponse
from app.services.openai_service import chat_completion, OpenAIServiceError

router = APIRouter(tags=["Chat"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with the AI Copilot",
    description=(
        "Send chat history and an optional prompt. Returns an assistant response generated via OpenAI. "
        "The request body must include an array of messages with roles user/assistant/system."
    ),
    responses={
        200: {"description": "Successful assistant response"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
        502: {"model": ErrorResponse, "description": "Bad Gateway (OpenAI error)"},
        503: {"model": ErrorResponse, "description": "Service Unavailable (Config/Network)"},
    },
)
# PUBLIC_INTERFACE
def chat_endpoint(payload: ChatRequest, x_session_id: Optional[str] = Header(default=None, alias="X-Session-ID")) -> ChatResponse:
    """Chat endpoint that sends the conversation to OpenAI and responds with a single assistant message.

    Parameters:
    - payload: ChatRequest containing messages and optional prompt.
    - X-Session-ID (header, optional): opaque session identifier for client correlation.

    Returns:
    - ChatResponse: { "message": {"role": "assistant", "content": "..."} }

    Error handling:
    - 503 if OpenAI API key is missing or connection fails
    - 502 for upstream errors or empty responses
    """
    # Prepare messages to send
    messages = payload.messages.copy()

    if payload.prompt:
        # Append the prompt as an extra user message, preserving provided history
        messages.append(Message(role="user", content=payload.prompt))

    try:
        assistant_text = chat_completion(messages)
        return ChatResponse(message=Message(role="assistant", content=assistant_text))
    except OpenAIServiceError as e:
        status_code = e.http_status or 502
        return JSONResponse(
            status_code=status_code,
            content=ErrorResponse(detail=str(e), code=e.code).model_dump(),
        )

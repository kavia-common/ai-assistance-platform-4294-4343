from __future__ import annotations

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class Message(BaseModel):
    """A chat message with role and content."""
    role: Literal["user", "assistant", "system"] = Field(..., description="Role of the speaker (user, assistant, or system).")
    content: str = Field(..., description="Text content of the message.")


class ChatRequest(BaseModel):
    """Incoming chat request with optional prompt and prior messages."""
    messages: List[Message] = Field(..., description="Chat history messages.")
    prompt: Optional[str] = Field(None, description="Optional extra user prompt to append.")


class ChatResponse(BaseModel):
    """Single message response from the assistant."""
    message: Message = Field(..., description="Assistant message returned by the model/service.")


class ErrorResponse(BaseModel):
    """Standard error response wrapper."""
    detail: str = Field(..., description="Human-readable error message.")
    code: Optional[str] = Field(None, description="Optional application-specific error code.")

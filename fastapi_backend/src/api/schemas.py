"""
Pydantic schemas for the AI Copilot backend API.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Role(str, Enum):
    """Role of the message author in chat history."""
    user = "user"
    assistant = "assistant"
    system = "system"


class Message(BaseModel):
    """A chat message with role and content."""
    role: Role = Field(..., description="Role of the speaker (user, assistant, or system).")
    content: str = Field(..., description="Text content of the message.")


class ChatRequest(BaseModel):
    """Incoming chat request with optional prompt and prior messages."""
    messages: List[Message] = Field(default_factory=list, description="Chat history messages.")
    prompt: Optional[str] = Field(default=None, description="Optional extra user prompt to append.")


class ChatResponse(BaseModel):
    """Single message response from the assistant."""
    message: Message = Field(..., description="Assistant message returned by the model/service.")


class ErrorResponse(BaseModel):
    """Standard error response wrapper."""
    detail: str = Field(..., description="Human-readable error message.")
    code: Optional[str] = Field(default=None, description="Optional application-specific error code.")

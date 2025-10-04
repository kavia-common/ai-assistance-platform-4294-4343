"""
Chat service that manages per-session chat history with an in-memory store.

This is a placeholder deterministic implementation that synthesizes an assistant
response by echoing and transforming the latest user input.
"""

from __future__ import annotations

import threading
from typing import Dict, List, Optional

from src.api.schemas import ChatRequest, ChatResponse, Message, Role


class _InMemoryChatStore:
    """Thread-safe in-memory store for session chat histories."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._history: Dict[str, List[Message]] = {}

    def append(self, session_id: str, messages: List[Message]) -> None:
        with self._lock:
            hist = self._history.setdefault(session_id, [])
            hist.extend(messages)

    def get(self, session_id: str) -> List[Message]:
        with self._lock:
            return list(self._history.get(session_id, []))

    def set(self, session_id: str, messages: List[Message]) -> None:
        with self._lock:
            self._history[session_id] = list(messages)


_store = _InMemoryChatStore()


def _deterministic_reply(prompt: Optional[str]) -> str:
    """
    Build a deterministic, friendly assistant reply based on the latest user prompt.
    """
    base = prompt or ""
    base_stripped = base.strip()
    if not base_stripped:
        return "Hello! How can I assist you today?"
    # Simple transformation as a stand-in for a model call
    reply = f"You said: '{base_stripped}'. Here's a helpful summary and next steps:\n" \
            f"- Summary: {base_stripped[:120]}\n" \
            f"- Next: Ask a follow-up or provide more details."
    return reply


# PUBLIC_INTERFACE
def process_chat(session_id: str, request: ChatRequest) -> ChatResponse:
    """
    Process a chat request for a given session and return a deterministic assistant response.

    The function:
    - Updates the in-memory chat history for the session
    - Appends the optional request.prompt as a user message if provided
    - Synthesizes an assistant response deterministically
    - Stores the assistant message in history and returns it
    """
    # Consolidate input messages
    incoming: List[Message] = list(request.messages)
    if request.prompt and request.prompt.strip():
        incoming.append(Message(role=Role.user, content=request.prompt.strip()))

    if incoming:
        _store.append(session_id, incoming)

    # Find latest user content to respond to
    latest_user: Optional[str] = None
    for msg in reversed(_store.get(session_id)):
        if msg.role == Role.user and msg.content.strip():
            latest_user = msg.content.strip()
            break

    assistant_text = _deterministic_reply(latest_user)
    assistant_msg = Message(role=Role.assistant, content=assistant_text)

    # Persist assistant message
    _store.append(session_id, [assistant_msg])

    return ChatResponse(message=assistant_msg)

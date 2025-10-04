"""
Chat service that manages per-session chat history with an in-memory store.

This is a placeholder deterministic implementation that synthesizes an assistant
response by echoing and transforming the latest user input.

Notes on determinism:
- This implementation intentionally avoids any randomness so that the same input
  produces the same output across runs. This keeps the UX stable for development
  and simplifies testing.

TODO (Provider Integration):
- Introduce a BaseProvider interface with a deterministic method signature, e.g.:
    class BaseProvider(Protocol):
        def generate(self, messages: list[Message]) -> str: ...
- Add selection logic based on SETTINGS.MODEL_PROVIDER (e.g., "openai", "local")
- For OpenAI (or other vendors), read API keys from environment variables via
  Settings (e.g., OPENAI_API_KEY), but do NOT hardcode keys in the code.
- Ensure provider-backed generation remains testable and can fall back to this
  deterministic path if configuration is missing or during local development.
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

    This function is intentionally side-effect free and avoids any randomness or
    time-based content so that results are stable for the same inputs.
    """
    base = prompt or ""
    base_stripped = base.strip()
    if not base_stripped:
        # Keep this default greeting stable and consistent.
        return "Hello! How can I assist you today?"
    # Simple transformation as a stand-in for a model call
    reply = (
        f"You said: '{base_stripped}'. Here's a helpful summary and next steps:\n"
        f"- Summary: {base_stripped[:120]}\n"
        f"- Next: Ask a follow-up or provide more details."
    )
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

    TODO (Provider Integration):
    - Inject Settings to read MODEL_PROVIDER and route generation accordingly:
        - If "local": use _deterministic_reply (current behavior)
        - If "openai" or others: delegate to a provider implementing BaseProvider
    - Keep deterministic fallback when provider configuration is missing to ensure
      the app remains usable in dev environments without extra setup.
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

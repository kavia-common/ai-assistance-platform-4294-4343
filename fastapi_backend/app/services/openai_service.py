from __future__ import annotations

from typing import List, Dict, Any

from openai import OpenAI, APIConnectionError, APIStatusError, OpenAIError

from app.utils.config import get_openai_api_key, get_openai_model
from app.models.schemas import Message


class OpenAIServiceError(Exception):
    """Raised when there is an OpenAI-related error that should be handled by the API layer."""
    def __init__(self, message: str, *, code: str | None = None, http_status: int | None = None):
        super().__init__(message)
        self.code = code
        self.http_status = http_status


def _build_client() -> OpenAI:
    """Create an OpenAI client using env configuration."""
    api_key = get_openai_api_key()
    if not api_key:
        # No API key configured; signal service unavailable
        raise OpenAIServiceError("OpenAI API key is not configured", code="OPENAI_CONFIG_MISSING", http_status=503)
    return OpenAI(api_key=api_key)


def _to_openai_messages(messages: List[Message]) -> List[Dict[str, Any]]:
    """Convert our Message models into OpenAI chat format."""
    return [{"role": m.role, "content": m.content} for m in messages]


# PUBLIC_INTERFACE
def chat_completion(messages: List[Message]) -> str:
    """Request a chat completion from OpenAI and return assistant content.

    Raises:
        OpenAIServiceError: if configuration is missing or OpenAI returns an error.
    """
    client = _build_client()
    model = get_openai_model()

    try:
        result = client.chat.completions.create(
            model=model,
            messages=_to_openai_messages(messages),
            temperature=0.2,
        )
        # Extract assistant message content
        choice = result.choices[0]
        if not choice.message or not getattr(choice.message, "content", None):
            raise OpenAIServiceError("Empty response from OpenAI", code="OPENAI_EMPTY_RESPONSE", http_status=502)
        return choice.message.content
    except APIConnectionError as e:
        # Network issues
        raise OpenAIServiceError(f"OpenAI connection error: {e}", code="OPENAI_CONNECTION_ERROR", http_status=503) from e
    except APIStatusError as e:
        # API returned a non-2xx status code
        status = getattr(e, "status_code", 502) or 502
        raise OpenAIServiceError(f"OpenAI API error: {e}", code="OPENAI_API_ERROR", http_status=int(status)) from e
    except OpenAIError as e:
        # Generic OpenAI error
        raise OpenAIServiceError(f"OpenAI error: {e}", code="OPENAI_ERROR", http_status=502) from e
    except Exception as e:
        # Unexpected error
        raise OpenAIServiceError(f"Unexpected OpenAI service error: {e}", code="OPENAI_UNEXPECTED_ERROR", http_status=502) from e

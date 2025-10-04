from fastapi.testclient import TestClient
import pytest

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_chat_success_monkeypatch(client, monkeypatch):
    # Patch the service to avoid calling OpenAI
    from app import services

    def fake_chat_completion(messages):
        return "This is a mocked assistant response."

    # Monkeypatch the service function
    monkeypatch.setattr(services.openai_service, "chat_completion", fake_chat_completion)

    payload = {
        "messages": [{"role": "user", "content": "Hello"}],
    }
    resp = client.post("/api/chat", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"]["role"] == "assistant"
    assert data["message"]["content"] == "This is a mocked assistant response."


def test_chat_missing_api_key_returns_503(client, monkeypatch):
    # Simulate missing API key by raising from service
    from app import services
    from app.services.openai_service import OpenAIServiceError

    def raise_config_error(messages):
        raise OpenAIServiceError("OpenAI API key is not configured", code="OPENAI_CONFIG_MISSING", http_status=503)

    monkeypatch.setattr(services.openai_service, "chat_completion", raise_config_error)

    payload = {
        "messages": [{"role": "user", "content": "Hi"}],
    }
    resp = client.post("/api/chat", json=payload)
    assert resp.status_code == 503
    data = resp.json()
    assert data["detail"]
    assert data.get("code") == "OPENAI_CONFIG_MISSING"

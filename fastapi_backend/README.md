# FastAPI Backend (AI Copilot)

FastAPI backend for the AI Copilot. Provides health check, suggestions, and OpenAI-integrated chat API.

- Framework: FastAPI + Uvicorn
- Default dev port: 3001
- Base API path: /api
- CORS: Configured via `ALLOWED_ORIGINS` (default `http://localhost:3000`)
- Entrypoint: app/main.py (ASGI app variable: `app`)

## Endpoints

- GET /api/health
  - Response: {"status": "ok"}
- GET /api/suggest
  - Response: {"suggestions": ["..."]} (exposed as plain array by the route, typed via response_model)
- POST /api/chat
  - Body (ChatRequest):
    {
      "messages": [{"role":"user|assistant|system", "content":"..."}],
      "prompt": "optional extra user prompt"
    }
  - Response (ChatResponse):
    {"message": {"role": "assistant", "content": "..."}}

## Error handling

- Returns JSON `ErrorResponse` on errors:
  - 503: Missing OpenAI API key or connection issues
  - 502: Upstream OpenAI error or empty response
  - 400/422: Validation errors handled by FastAPI/Pydantic

## Environment variables

- BACKEND_PORT: Port for the backend server (default: 3001)
- ALLOWED_ORIGINS: Comma-separated list of allowed origins for CORS (default: http://localhost:3000)
- OPENAI_API_KEY: API key for OpenAI (required for /api/chat)
- OPENAI_MODEL: Model name (default: gpt-4o-mini)

Note: Environment variables are provided by the orchestrator. Do not commit a .env file.

## Running locally

1) Python 3.11+ recommended
2) Install dependencies:
   pip install -r requirements.txt
3) Run with Uvicorn:
   uvicorn app.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-3001} --reload

Docs:
- Swagger UI: http://localhost:3001/docs
- OpenAPI JSON: http://localhost:3001/openapi.json

## Testing

Run pytest:
  pytest -q fastapi_backend/tests

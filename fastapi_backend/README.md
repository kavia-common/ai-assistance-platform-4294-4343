# AI Copilot FastAPI Backend

## Overview
This is the FastAPI backend for the AI Copilot application. It provides REST endpoints for health checks, chat interactions, and suggestion prompts, intended to be consumed by the React frontend. The current implementation uses a deterministic, local chat service to keep development and testing stable. Future provider integrations (e.g., OpenAI) are anticipated but not yet implemented.

- Framework: FastAPI + Uvicorn
- Default port: 8000
- Base API path: /api
- Key modules:
  - src/api/main.py – App creation, CORS, and health endpoint
  - src/api/routers/chat.py – /api/chat
  - src/api/routers/suggest.py – /api/suggest
  - src/api/services/chat_service.py – Deterministic chat logic with in-memory session history
  - src/api/services/suggest_service.py – Static list of suggestions
  - src/api/config.py – Environment-driven settings

## Getting Started
The backend can be run locally for development, and it is designed to work seamlessly with the React frontend running on localhost:3000. The CORS configuration automatically allows http://localhost:3000 even if not explicitly set via environment variables.

- Install dependencies (Python 3.11+ recommended):
  - pip install -r requirements.txt
- Run the API with Uvicorn:
  - uvicorn src.api.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8000} --reload

Once running, the interactive docs are available at:
- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

Preview system notes:
- This backend is intended to be paired with the React frontend (default dev server at http://localhost:3000). CORS is configured to permit that origin automatically for a smooth local dev experience.
- If your preview system assigns a different port or domain, adjust CORS_ORIGINS accordingly.

## Environment Variables
Environment variables are read in src/api/config.py with sensible defaults:

- BACKEND_PORT: Port for the backend server.
  - Default: 8000
- CORS_ORIGINS: Comma-separated list of allowed origins for CORS, or "*" to allow all.
  - Default: *
  - Note: Even if you do not set this, http://localhost:3000 will be allowed by default to support React dev.
  - Examples:
    - CORS_ORIGINS="http://localhost:3000,http://localhost:5173"
    - CORS_ORIGINS="*"
- MODEL_PROVIDER: Placeholder for future provider selection.
  - Default: local
  - Examples: local, openai, azure (not implemented yet)
- OPENAI_API_KEY: Placeholder for future OpenAI integration.
  - Default: unset
  - Not used at runtime in the current implementation. Do not set unless future provider integration has been added.

Example .env (for future use, optional today):
```
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:3000
MODEL_PROVIDER=local
OPENAI_API_KEY=your_openai_key_here
```

## API Endpoints
Base path: /api

### Health
- GET /api/health
- Purpose: Simple health check.
- Response example:
```
{
  "status": "ok"
}
```

### Chat
- POST /api/chat
- Purpose: Send chat history and an optional prompt. Returns a deterministic assistant response.
- Headers (optional):
  - X-Session-ID: A client-provided session identifier. If omitted, the backend generates a UUID per request context for history grouping.
- Request body schema (ChatRequest):
```
{
  "messages": [
    { "role": "user", "content": "Hello there" }
  ],
  "prompt": "Tell me something helpful"
}
```
- Response body schema (ChatResponse):
```
{
  "message": {
    "role": "assistant",
    "content": "You said: 'Tell me something helpful'. Here's a helpful summary and next steps:\n- Summary: Tell me something helpful\n- Next: Ask a follow-up or provide more details."
  }
}
```
- Notes:
  - The response is deterministic. If no user content is found, a default greeting is returned: "Hello! How can I assist you today?"

### Suggest
- GET /api/suggest
- Purpose: Fetch a static list of suggested prompts for users.
- Response example:
```
[
  "Summarize the following text...",
  "Draft an email requesting a project status update.",
  "Explain this code snippet in simple terms.",
  "Generate test cases for this function.",
  "Brainstorm 5 ideas to improve user onboarding."
]
```

## CORS Configuration
CORS is configured in src/api/main.py using Starlette’s CORSMiddleware. The configuration merges environment-specified origins with http://localhost:3000 to facilitate React development. Behavior:
- If CORS_ORIGINS="*", all origins are permitted.
- If CORS_ORIGINS is unset or a list, the backend ensures http://localhost:3000 is included.
- Allowed methods and headers: "*"
- Credentials allowed: true

Common local setup:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000 (auto-permitted)

If your frontend runs elsewhere (e.g., different port or domain), set CORS_ORIGINS accordingly:
- CORS_ORIGINS="http://localhost:5173,http://mydomain.test:8080"

## Development Tips and Troubleshooting
- Live reload: Use --reload with Uvicorn for local development.
- OpenAPI generation: A helper script exists at src/api/generate_openapi.py that writes the schema to fastapi_backend/interfaces/openapi.json. You can run it from the fastapi_backend directory when needed.
- Default behavior: The chat service is deterministic and does not call external providers. MODEL_PROVIDER and OPENAI_API_KEY are placeholders until provider integrations are implemented.
- Session behavior: If you omit X-Session-ID, the backend generates a UUID. Provide a stable X-Session-ID from the client to maintain a persistent in-memory conversation history for that session during the backend process lifetime.
- CORS errors from the browser:
  - Ensure the backend is running and reachable at the configured BACKEND_PORT.
  - If using a non-default frontend origin, verify it’s included in CORS_ORIGINS or set CORS_ORIGINS="*".
  - Confirm that the frontend uses the correct backend base URL (e.g., http://localhost:8000).
- Port conflicts:
  - If 8000 is in use, choose a different BACKEND_PORT and pass --port or set the env var.
- Production considerations:
  - The in-memory store is for development only. It does not persist across process restarts and is not shared between instances. Replace with a persistent store or provider-backed service for production use.
  - Review and restrict CORS_ORIGINS for production to specific trusted domains.

## Running Commands Summary
- Install: pip install -r requirements.txt
- Run (dev): uvicorn src.api.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8000} --reload
- Docs: http://localhost:8000/docs
- Health: curl http://localhost:8000/api/health
- Chat example:
  - curl -X POST http://localhost:8000/api/chat \
    -H "Content-Type: application/json" \
    -H "X-Session-ID: test-session-123" \
    -d '{"messages":[{"role":"user","content":"Hello"}],"prompt":"Tell me something helpful"}'

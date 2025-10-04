# FastAPI Backend (Clean Boilerplate)

This is a minimal FastAPI backend scaffolded for the AI Copilot project.

- Framework: FastAPI + Uvicorn
- Default dev port: 3001
- Base API path: /api
- CORS: Allows http://localhost:3000 (React dev server)
- Entrypoint: app/main.py (ASGI app variable: `app`)

## Endpoints

- GET /api/health
  - Response: {"status": "ok"}
- POST /api/chat
  - Body: {"message": "Hello"}
  - Response: {"message": {"role": "assistant", "content": "Hello"}}
- GET /api/suggest
  - Response: ["Try asking about the weather", "Ask for a code review", "Summarize a document"]

## Running locally

1) Install dependencies (Python 3.11+ recommended):
   - pip install -r requirements.txt

2) Run with Uvicorn on port 3001:
   - uvicorn app.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-3001} --reload

Docs and schema:
- Swagger UI: http://localhost:3001/docs
- OpenAPI JSON: http://localhost:3001/openapi.json

## Environment

- BACKEND_PORT (optional): Port for the backend server.
  - Default in docs/commands: 3001

Note: Environment variables are provided by the orchestrator. Do not commit a .env file.

## Notes

- This is a fresh boilerplate and intentionally minimal.
- It is designed to pair with the React frontend at http://localhost:3000.
- CORS is configured to allow http://localhost:3000 only by default.

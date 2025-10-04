# FastAPI Backend (Minimal)

This backend exposes GET /api/health on port 3001 and enables CORS from the React dev server (http://localhost:3000).

## Run locally

1) Create a virtualenv and install FastAPI and Uvicorn:

   pip install fastapi uvicorn

2) Start the server on port 3001:

   uvicorn main:app --host 0.0.0.0 --port 3001

3) Test:
   - GET http://localhost:3001/api/health should return 200 with {"status":"ok"}.
   - OpenAPI: http://localhost:3001/docs

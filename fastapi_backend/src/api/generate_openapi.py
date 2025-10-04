import json
import sys
from pathlib import Path

# Ensure module imports work regardless of where this script is executed from
# Resolve project root as the fastapi_backend directory that contains 'src' and 'interfaces'
CURRENT_FILE = Path(__file__).resolve()
FASTAPI_BACKEND_DIR = CURRENT_FILE.parents[3]  # .../fastapi_backend
SRC_DIR = FASTAPI_BACKEND_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.api.main import app  # type: ignore  # noqa: E402

# Get the OpenAPI schema
openapi_schema = app.openapi()

# Write to file inside the fastapi_backend/interfaces folder
output_dir = FASTAPI_BACKEND_DIR / "interfaces"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "openapi.json"

with open(output_path, "w") as f:
    json.dump(openapi_schema, f, indent=2)

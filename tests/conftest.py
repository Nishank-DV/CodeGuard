import os
import sys
from pathlib import Path


API_ROOT = Path(__file__).resolve().parents[1]
if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))

# Ensure tests have valid defaults even when local .env is missing or incomplete.
os.environ.setdefault("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
os.environ.setdefault("CORS_ALLOW_METHODS", "GET,POST,PATCH,DELETE,OPTIONS")
os.environ.setdefault("CORS_ALLOW_HEADERS", "Authorization,Content-Type,Accept,Origin,X-API-Key")

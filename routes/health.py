from fastapi import APIRouter, HTTPException
from datetime import datetime
from schemas.analysis import HealthResponse
from config import settings
from database.session import get_connection

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.utcnow()
    )

@router.get("/ready", response_model=dict)
async def readiness_check():
    """Readiness check endpoint."""
    db_ok = True
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
    except Exception:
        db_ok = False

    return {
        "status": "ready" if db_ok else "degraded",
        "database": "ok" if db_ok else "error",
    }


@router.get("/diagnostics", response_model=dict)
async def diagnostics_check():
    """Operational diagnostics without leaking sensitive configuration."""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "max_code_length": settings.max_code_length,
        "max_upload_bytes": settings.max_upload_bytes,
        "allowed_upload_extensions": settings.allowed_upload_extensions,
        "timestamp": datetime.utcnow().isoformat(),
    }

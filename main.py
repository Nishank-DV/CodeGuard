import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database.session import init_db
from security.auth import validate_auth_configuration
from routes.health import router as health_router
from routes.analysis import router as analysis_router
from routes.scans import router as scans_router
from routes.auth import router as auth_router


logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    init_db()
    validate_auth_configuration()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug
    )
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    @app.middleware("http")
    async def request_size_guard(request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and content_length.isdigit():
            if int(content_length) > settings.max_request_bytes:
                return JSONResponse(
                    status_code=413,
                    content={
                        "success": False,
                        "error": "Request too large",
                        "message": f"Max request size is {settings.max_request_bytes} bytes",
                    },
                )
        return await call_next(request)
    
    # Routes
    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(analysis_router)
    app.include_router(scans_router)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled API exception on %s", request.url.path)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "message": "An unexpected error occurred. Check server logs for details.",
            },
        )
    
    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "status": "running"
        }
    
    # API documentation will be available at:
    # /docs (Swagger UI)
    # /redoc (ReDoc)
    
    return app

# Create the app instance
app = create_app()

try:
    from pydantic_settings import BaseSettings
except ModuleNotFoundError:  # pragma: no cover - compatibility fallback
    from pydantic.v1 import BaseSettings
from typing import Annotated, Optional

from pydantic import field_validator
from pydantic_settings import NoDecode, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # App
    app_name: str = "CodeGuard API"
    app_version: str = "0.5.0"
    debug: bool = False
    environment: str = "development"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS
    cors_origins: Annotated[list[str], NoDecode] = ["http://localhost:5173", "http://localhost:3000"]
    cors_allow_credentials: bool = True
    cors_allow_methods: Annotated[list[str], NoDecode] = ["GET", "POST", "PATCH", "DELETE", "OPTIONS"]
    cors_allow_headers: Annotated[list[str], NoDecode] = ["Authorization", "Content-Type", "Accept", "Origin", "X-API-Key"]

    # Phase 4.1 auth and RBAC
    auth_enabled: bool = True
    auth_header_name: str = "X-API-Key"
    auth_api_keys: str = "admin:dev-admin-key,analyst:dev-analyst-key,viewer:dev-viewer-key"
    
    # Database
    database_url: Optional[str] = None
    sqlite_db_path: str = "./data/codeguard.db"

    # Request hardening
    max_code_length: int = 100000
    max_upload_bytes: int = 200000
    max_batch_files: int = 20
    max_request_bytes: int = 1500000
    allowed_upload_extensions: Annotated[list[str], NoDecode] = [".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".php", ".rs", ".cpp", ".c", ".h"]
    
    # Logging
    log_level: str = "INFO"

    @field_validator("cors_origins", "cors_allow_methods", "cors_allow_headers", "allowed_upload_extensions", mode="before")
    @classmethod
    def _split_csv_to_list(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

settings = Settings()

import re
from pathlib import Path

from fastapi import HTTPException, status

from config import settings


def sanitize_filename(filename: str | None) -> str:
    if not filename:
        return "uploaded_file"
    safe = Path(filename).name
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", safe)
    return safe[:120] or "uploaded_file"


def validate_extension(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext not in settings.allowed_upload_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File extension not allowed: {ext}",
        )
    return ext


def decode_utf8_content(raw: bytes) -> str:
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only UTF-8 text source files are supported",
        )

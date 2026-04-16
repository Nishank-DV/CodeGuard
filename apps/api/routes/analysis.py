import logging
import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from config import settings
from security.auth import require_roles
from schemas.analysis import BatchFileResult, BatchScanResponse, BatchScanResult, CodeAnalysisRequest, AnalysisResponse
from services.analysis_service import AnalysisService
from services.persistence.scan_store import ScanStore
from services.upload_validation import decode_utf8_content, sanitize_filename, validate_extension

router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"],
    dependencies=[Depends(require_roles("analyst", "admin"))],
)


logger = logging.getLogger(__name__)
SUPPORTED_LANGUAGES = {"python", "javascript", "typescript", "js", "ts"}


def _normalize_language(language: str) -> str:
    language = language.lower().strip()
    if language in {"js", "typescript", "ts"}:
        return "javascript"
    return language


def _language_from_extension(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    mapping = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "javascript",
        ".jsx": "javascript",
        ".tsx": "javascript",
    }
    lang = mapping.get(ext)
    if not lang:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file extension: {ext}",
        )
    return lang


async def _analyze_and_store_single(code: str, language: str, filename: str | None = None):
    started = time.perf_counter()
    result = AnalysisService.analyze_code(code, language)
    duration_ms = int((time.perf_counter() - started) * 1000)
    ScanStore.store_scan(result=result, code=code, filename=filename, duration_ms=duration_ms)
    return result, duration_ms


def _validate_analysis_request(request: CodeAnalysisRequest) -> str:
    if not request.code or not request.code.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code cannot be empty"
        )

    if len(request.code) > settings.max_code_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Code exceeds max allowed length ({settings.max_code_length} characters)"
        )

    normalized_language = _normalize_language(request.language)
    if normalized_language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported language: {request.language}"
        )

    return normalized_language

@router.post("", response_model=AnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    """
    Analyze source code for security vulnerabilities.
    
    Args:
        request: CodeAnalysisRequest containing code and language
        
    Returns:
        AnalysisResponse with vulnerability findings
    """
    try:
        normalized_language = _validate_analysis_request(request)

        safe_filename = sanitize_filename(request.filename) if request.filename else None
        result, _ = await _analyze_and_store_single(request.code, normalized_language, safe_filename)
        
        return AnalysisResponse(
            success=True,
            data=result,
            message=f"Analysis complete. Found {result.total_issues} vulnerabilities."
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception("Analysis failed for language=%s", request.language)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Analysis failed due to an internal error"
        )


@router.post("/live", response_model=AnalysisResponse)
async def analyze_code_live(request: CodeAnalysisRequest):
    """Analyze code for live editor feedback without persisting the scan."""
    try:
        normalized_language = _validate_analysis_request(request)
        result = AnalysisService.analyze_code(request.code, normalized_language)
        return AnalysisResponse(
            success=True,
            data=result,
            message=f"Live analysis complete. Found {result.total_issues} vulnerabilities.",
        )
    except HTTPException as e:
        raise e
    except Exception:
        logger.exception("Live analysis failed for language=%s", request.language)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Live analysis failed due to an internal error",
        )


@router.post("/file", response_model=AnalysisResponse)
async def analyze_uploaded_file(file: UploadFile = File(...)):
    """Analyze an uploaded source file with strict validation.

    Files are treated as plain text only and never executed.
    """
    filename = sanitize_filename(file.filename)
    validate_extension(filename)

    raw = await file.read(settings.max_upload_bytes + 1)
    if len(raw) > settings.max_upload_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds max size ({settings.max_upload_bytes} bytes)",
        )

    content = decode_utf8_content(raw)

    language = _language_from_extension(filename)
    request = CodeAnalysisRequest(code=content, language=language, filename=filename)
    return await analyze_code(request)


@router.post("/batch-files", response_model=BatchScanResponse)
async def analyze_batch_files(
    files: list[UploadFile] = File(...),
    continue_on_error: bool = Query(default=True),
):
    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No files uploaded")
    if len(files) > settings.max_batch_files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Too many files. Max batch size is {settings.max_batch_files}",
        )

    batch_id = str(uuid4())
    items: list[BatchFileResult] = []
    lang_breakdown: dict[str, int] = {}
    total_issues = 0
    total_risk = 0.0

    for uploaded in files:
        filename = sanitize_filename(uploaded.filename)
        started = time.perf_counter()
        try:
            validate_extension(filename)
            raw = await uploaded.read(settings.max_upload_bytes + 1)
            if len(raw) > settings.max_upload_bytes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File exceeds max size ({settings.max_upload_bytes} bytes)",
                )
            content = decode_utf8_content(raw)
            language = _language_from_extension(filename)

            result, duration_ms = await _analyze_and_store_single(content, language, filename)
            lang_breakdown[language] = lang_breakdown.get(language, 0) + 1
            total_issues += result.total_issues
            total_risk += result.risk_score
            items.append(
                BatchFileResult(
                    filename=filename,
                    language=language,
                    success=True,
                    duration_ms=duration_ms,
                    issues_found=result.total_issues,
                    risk_score=result.risk_score,
                    analysis_id=result.id,
                )
            )
        except Exception as exc:
            duration_ms = int((time.perf_counter() - started) * 1000)
            message = exc.detail if isinstance(exc, HTTPException) else "Batch file analysis failed"
            items.append(
                BatchFileResult(
                    filename=filename,
                    language="unknown",
                    success=False,
                    duration_ms=duration_ms,
                    issues_found=0,
                    risk_score=0.0,
                    error=str(message),
                )
            )
            if not continue_on_error:
                break

    successful = [i for i in items if i.success]
    result = BatchScanResult(
        batch_id=batch_id,
        processed_files=len(items),
        successful_files=len(successful),
        failed_files=len(items) - len(successful),
        total_issues=total_issues,
        avg_risk_score=(total_risk / len(successful)) if successful else 0.0,
        language_breakdown=lang_breakdown,
        files=items,
        scanned_at=datetime.utcnow(),
    )

    return BatchScanResponse(
        success=True,
        data=result,
        message=f"Batch analysis complete. Processed {len(items)} files.",
    )

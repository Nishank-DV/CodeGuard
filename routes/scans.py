from datetime import datetime
from typing import Optional
import re

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from security.auth import require_roles
from security.auth import resolve_role_from_key

from database.session import get_db
from repositories.scan_repository import ScanRepository
from schemas.scans import (
    FindingStatusResponse,
    FindingStatusUpdateRequest,
    ScanDetailResponse,
    ScanListItem,
    ScanListResponse,
    ScanSummaryResponse,
)
from services.analytics.scan_analytics import ScanAnalyticsService
from services.remediation.status_manager import RemediationStatusManager
from services.reports.report_generator import ReportGenerator


router = APIRouter(prefix="/scans", tags=["Scans"])


@router.get("", response_model=ScanListResponse)
async def list_scans(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    language: Optional[str] = Query(default=None),
    min_risk_score: Optional[float] = Query(default=None, ge=0, le=100),
    sort_by: str = Query(default="scanned_at"),
    sort_dir: str = Query(default="desc"),
    _=Depends(require_roles("viewer", "analyst", "admin")),
    db=Depends(get_db),
):
    repo = ScanRepository(db)
    rows, total = repo.list_scans(
        page=page,
        page_size=page_size,
        language=language,
        min_risk_score=min_risk_score,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )
    items = [
        ScanListItem(
            id=row["id"],
            filename=row["filename"],
            language=row["language"],
            scanned_at=datetime.fromisoformat(row["scanned_at"]),
            duration_ms=row["duration_ms"],
            total_issues=row["total_issues"],
            critical_count=row["critical_count"],
            high_count=row["high_count"],
            medium_count=row["medium_count"],
            low_count=row["low_count"],
            info_count=row["info_count"],
            risk_score=row["risk_score"],
            finding_summary=row["finding_summary"],
        )
        for row in rows
    ]
    return ScanListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/summary", response_model=ScanSummaryResponse)
async def scans_summary(_=Depends(require_roles("viewer", "analyst", "admin"))):
    data = ScanAnalyticsService.get_summary()
    return ScanSummaryResponse(
        total_scans=data["total_scans"],
        total_vulnerabilities=data["total_vulnerabilities"],
        average_risk_score=data["average_risk_score"],
        most_common_language=data["most_common_language"],
        highest_risk_scan_id=data["highest_risk_scan_id"],
        highest_risk_score=data["highest_risk_score"],
        top_cwe_ids=data["top_cwe_ids"],
        top_finding_titles=data.get("top_finding_titles", []),
        severity_distribution=data["severity_distribution"],
        language_distribution=data.get("language_distribution", {}),
        avg_findings_per_scan=data["avg_findings_per_scan"],
        scans_last_7_days=data["scans_last_7_days"],
        open_findings=data["open_findings"],
        reviewing_findings=data["reviewing_findings"],
        resolved_findings=data["resolved_findings"],
        ignored_findings=data["ignored_findings"],
        generated_at=datetime.fromisoformat(data["generated_at"]),
    )


@router.get("/{scan_id}", response_model=ScanDetailResponse)
async def get_scan(scan_id: str, _=Depends(require_roles("viewer", "analyst", "admin")), db=Depends(get_db)):
    repo = ScanRepository(db)
    row = repo.get_scan(scan_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")

    return ScanDetailResponse(
        id=row["id"],
        code_hash=row["code_hash"],
        filename=row["filename"],
        language=row["language"],
        scanned_at=datetime.fromisoformat(row["scanned_at"]),
        duration_ms=row["duration_ms"],
        total_issues=row["total_issues"],
        critical_count=row["critical_count"],
        high_count=row["high_count"],
        medium_count=row["medium_count"],
        low_count=row["low_count"],
        info_count=row["info_count"],
        risk_score=row["risk_score"],
        finding_summary=row["finding_summary"],
        findings=row["findings"],
    )


@router.delete("/{scan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scan(scan_id: str, _=Depends(require_roles("admin")), db=Depends(get_db)):
    repo = ScanRepository(db)
    deleted = repo.delete_scan(scan_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{scan_id}/report")
async def download_scan_report(
    scan_id: str,
    format: str = Query(default="json", pattern="^(json|md)$"),
    api_key: Optional[str] = Query(default=None),
    _=Depends(require_roles("viewer", "analyst", "admin")),
    db=Depends(get_db),
):
    # Query-string key support keeps report downloads usable via window.open in demo mode.
    if api_key:
        if not resolve_role_from_key(api_key):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

    repo = ScanRepository(db)
    row = repo.get_scan(scan_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")

    content, media_type = ReportGenerator.generate(row, report_format=format)
    ts = datetime.fromisoformat(row["scanned_at"]).strftime("%Y%m%d-%H%M%S")
    base_name = row.get("filename") or row.get("id")
    safe_base = re.sub(r"[^A-Za-z0-9._-]", "_", base_name)[:80]
    filename = f"codeguard-report-{safe_base}-{ts}.{format}"
    return Response(
        content=content,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff",
        },
    )


@router.patch("/{scan_id}/findings/{finding_id}", response_model=FindingStatusResponse)
async def update_finding_status(
    scan_id: str,
    finding_id: str,
    request: FindingStatusUpdateRequest,
    _=Depends(require_roles("analyst", "admin")),
):
    updated = RemediationStatusManager.update_finding_status(
        scan_id=scan_id,
        finding_id=finding_id,
        status=request.status,
        remediation_notes=request.remediation_notes,
    )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding or scan not found")

    return FindingStatusResponse(
        scan_id=updated["scan_id"],
        finding_id=updated["finding_id"],
        status=updated["status"],
        remediation_notes=updated["remediation_notes"],
        updated_at=datetime.fromisoformat(updated["updated_at"]),
    )

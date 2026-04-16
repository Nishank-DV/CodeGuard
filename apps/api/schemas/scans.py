from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

from schemas.analysis import Vulnerability


FindingStatus = Literal["open", "reviewing", "resolved", "ignored"]


class ScanListItem(BaseModel):
    id: str
    filename: Optional[str] = None
    language: str
    scanned_at: datetime
    duration_ms: int
    total_issues: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    risk_score: float
    finding_summary: str


class ScanDetailResponse(BaseModel):
    id: str
    code_hash: str
    filename: Optional[str] = None
    language: str
    scanned_at: datetime
    duration_ms: int
    total_issues: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    risk_score: float
    finding_summary: str
    findings: list[Vulnerability]


class ScanListResponse(BaseModel):
    items: list[ScanListItem]
    total: int
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)


class ScanSummaryResponse(BaseModel):
    total_scans: int
    total_vulnerabilities: int
    average_risk_score: float
    most_common_language: Optional[str] = None
    highest_risk_scan_id: Optional[str] = None
    highest_risk_score: float
    top_cwe_ids: list[str]
    top_finding_titles: list[str]
    severity_distribution: dict[str, int]
    language_distribution: dict[str, int]
    avg_findings_per_scan: float
    scans_last_7_days: int
    open_findings: int
    reviewing_findings: int
    resolved_findings: int
    ignored_findings: int
    generated_at: datetime


class FindingStatusUpdateRequest(BaseModel):
    status: FindingStatus
    remediation_notes: Optional[str] = Field(default=None, max_length=2000)


class FindingStatusResponse(BaseModel):
    scan_id: str
    finding_id: str
    status: FindingStatus
    remediation_notes: Optional[str] = None
    updated_at: datetime

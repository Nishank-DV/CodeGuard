from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


@dataclass
class ScanRecord:
    id: str
    code_hash: str
    filename: Optional[str]
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
    findings_json: str


@dataclass
class FindingStatusRecord:
    scan_id: str
    finding_id: str
    status: str
    remediation_notes: Optional[str]
    updated_at: datetime


@dataclass
class ScanSummaryRecord:
    total_scans: int
    total_vulnerabilities: int
    average_risk_score: float
    most_common_language: Optional[str]
    highest_risk_scan_id: Optional[str]
    highest_risk_score: float
    top_cwe_ids: list[str]
    severity_distribution: dict[str, int]
    avg_findings_per_scan: float
    scans_last_7_days: int
    open_findings: int
    resolved_findings: int
    ignored_findings: int
    reviewing_findings: int
    generated_at: datetime

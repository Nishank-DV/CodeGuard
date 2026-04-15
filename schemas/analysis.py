from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class Vulnerability(BaseModel):
    """Represents a detected vulnerability with Phase 3 enhancements."""
    id: str
    title: str
    description: str
    severity: Literal["critical", "high", "medium", "low", "info"]
    cwe_id: str
    owasp_category: str
    line_number: int
    column_number: Optional[int] = None
    code_snippet: Optional[str] = None
    fix_suggestion: Optional[str] = None
    secure_fix_code: Optional[str] = None
    confidence: float = Field(ge=0.0, le=1.0)
    rule_id: Optional[str] = None
    
    # Phase 3 enhancements
    confidence_reason: Optional[str] = None  # e.g., "exact_match", "contextual_match"
    priority_score: int = Field(ge=0, le=100, default=50)
    exploitability: Literal["low", "medium", "high"] = Field(default="medium")
    remediation_priority: Literal["critical", "high", "medium", "low"] = Field(default="medium")
    business_impact: Optional[str] = None
    detailed_remediation: Optional[str] = None

    # Phase 4 remediation workflow
    status: Literal["open", "reviewing", "resolved", "ignored"] = Field(default="open")
    remediation_notes: Optional[str] = Field(default=None, max_length=2000)


class AnalysisResult(BaseModel):
    """Result of code analysis with Phase 3 metadata."""
    id: str
    language: str
    vulnerabilities: list[Vulnerability]
    total_issues: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    risk_score: float = Field(ge=0.0, le=100.0)
    scanned_at: datetime
    deduplication_info: Optional[dict] = None


class CodeAnalysisRequest(BaseModel):
    """Request payload for code analysis."""
    code: str = Field(..., min_length=1, max_length=100000)
    language: str
    filename: Optional[str] = None


class AnalysisResponse(BaseModel):
    """API response for analysis endpoint."""
    success: bool
    data: Optional[AnalysisResult] = None
    error: Optional[str] = None
    message: str


class BatchFileResult(BaseModel):
    filename: str
    language: str
    success: bool
    duration_ms: int
    issues_found: int
    risk_score: float
    analysis_id: Optional[str] = None
    error: Optional[str] = None


class BatchScanResult(BaseModel):
    batch_id: str
    processed_files: int
    successful_files: int
    failed_files: int
    total_issues: int
    avg_risk_score: float
    language_breakdown: dict[str, int]
    files: list[BatchFileResult]
    scanned_at: datetime


class BatchScanResponse(BaseModel):
    success: bool
    data: Optional[BatchScanResult] = None
    error: Optional[str] = None
    message: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: datetime

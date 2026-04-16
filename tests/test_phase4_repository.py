import sqlite3
from datetime import datetime

from repositories.scan_repository import ScanRepository
from schemas.analysis import AnalysisResult, Vulnerability


def _setup_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE scans (
            id TEXT PRIMARY KEY,
            code_hash TEXT NOT NULL,
            filename TEXT,
            language TEXT NOT NULL,
            scanned_at TEXT NOT NULL,
            duration_ms INTEGER NOT NULL,
            total_issues INTEGER NOT NULL,
            critical_count INTEGER NOT NULL,
            high_count INTEGER NOT NULL,
            medium_count INTEGER NOT NULL,
            low_count INTEGER NOT NULL,
            info_count INTEGER NOT NULL,
            risk_score REAL NOT NULL,
            finding_summary TEXT,
            findings_json TEXT NOT NULL
        );
        CREATE TABLE finding_statuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id TEXT NOT NULL,
            finding_id TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            remediation_notes TEXT,
            updated_at TEXT NOT NULL,
            UNIQUE(scan_id, finding_id),
            FOREIGN KEY(scan_id) REFERENCES scans(id) ON DELETE CASCADE
        );
        """
    )
    return conn


def _sample_result(scan_id: str = "scan-1") -> AnalysisResult:
    vuln = Vulnerability(
        id="finding-1",
        title="Use of eval()",
        description="eval usage",
        severity="critical",
        cwe_id="CWE-95",
        owasp_category="A03:2021 - Injection",
        line_number=10,
        code_snippet="eval(user_input)",
        fix_suggestion="avoid eval",
        secure_fix_code="ast.literal_eval",
        confidence=0.9,
        confidence_reason="exact_match",
        priority_score=95,
        exploitability="high",
        remediation_priority="critical",
        business_impact="arbitrary_code_execution",
        detailed_remediation="Use safe parser",
    )
    return AnalysisResult(
        id=scan_id,
        language="python",
        vulnerabilities=[vuln],
        total_issues=1,
        critical_count=1,
        high_count=0,
        medium_count=0,
        low_count=0,
        info_count=0,
        risk_score=90.0,
        scanned_at=datetime.utcnow(),
        deduplication_info={"total_merged": 0},
    )


def test_scan_create_list_get_and_delete():
    conn = _setup_conn()
    repo = ScanRepository(conn)
    result = _sample_result()

    repo.create_scan(result, code_hash="abc", filename="app.py", duration_ms=123)

    rows, total = repo.list_scans(page=1, page_size=10)
    assert total == 1
    assert len(rows) == 1

    detail = repo.get_scan("scan-1")
    assert detail is not None
    assert detail["id"] == "scan-1"
    assert len(detail["findings"]) == 1
    assert detail["findings"][0]["status"] == "open"

    deleted = repo.delete_scan("scan-1")
    assert deleted is True

    rows, total = repo.list_scans(page=1, page_size=10)
    assert total == 0
    assert len(rows) == 0


def test_update_finding_status_and_summary():
    conn = _setup_conn()
    repo = ScanRepository(conn)
    result = _sample_result("scan-2")
    repo.create_scan(result, code_hash="hash", filename="main.py", duration_ms=88)

    updated = repo.update_finding_status("scan-2", "finding-1", "resolved", "Patched")
    assert updated is not None
    assert updated["status"] == "resolved"
    assert updated["remediation_notes"] == "Patched"

    summary = repo.summary()
    assert summary["total_scans"] == 1
    assert summary["total_vulnerabilities"] == 1
    assert summary["resolved_findings"] == 1
    assert "CWE-95" in summary["top_cwe_ids"]

from services.reports.report_generator import ReportGenerator


def _sample_scan() -> dict:
    return {
        "id": "scan-123",
        "filename": "demo.py",
        "language": "python",
        "scanned_at": "2026-04-01T00:00:00",
        "duration_ms": 100,
        "total_issues": 1,
        "critical_count": 1,
        "high_count": 0,
        "medium_count": 0,
        "low_count": 0,
        "info_count": 0,
        "risk_score": 88.5,
        "findings": [
            {
                "id": "finding-1",
                "title": "Use of eval()",
                "severity": "critical",
                "cwe_id": "CWE-95",
                "owasp_category": "A03:2021 - Injection",
                "line_number": 4,
                "priority_score": 92,
                "exploitability": "high",
                "status": "open",
                "confidence": 0.95,
                "confidence_reason": "exact_match",
                "business_impact": "arbitrary_code_execution",
                "description": "dangerous code execution",
                "fix_suggestion": "Use ast.literal_eval",
                "detailed_remediation": "Avoid eval",
            }
        ],
    }


def test_generate_json_report():
    report, media_type = ReportGenerator.generate(_sample_scan(), report_format="json")
    assert media_type == "application/json"
    assert "scan-123" in report
    assert "Use of eval()" in report


def test_generate_markdown_report():
    report, media_type = ReportGenerator.generate(_sample_scan(), report_format="md")
    assert media_type == "text/markdown"
    assert "# CodeGuard Scan Report" in report
    assert "Use of eval()" in report
    assert "Priority Overview" in report

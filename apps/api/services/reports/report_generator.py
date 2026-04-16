from datetime import datetime
from typing import Literal

from config import settings


class ReportGenerator:
    @staticmethod
    def generate(scan: dict, report_format: Literal["json", "md"] = "json") -> tuple[str, str]:
        if report_format == "md":
            return ReportGenerator._markdown(scan), "text/markdown"
        return ReportGenerator._json(scan), "application/json"

    @staticmethod
    def _json(scan: dict) -> str:
        import json

        findings = scan.get("findings", [])
        status_counts = ReportGenerator._status_counts(findings)

        payload = {
            "generated_at": datetime.utcnow().isoformat(),
            "tool": {
                "name": settings.app_name,
                "version": settings.app_version,
            },
            "executive_summary": {
                "risk_score": scan.get("risk_score", 0),
                "total_issues": scan.get("total_issues", 0),
                "critical_or_high": int(scan.get("critical_count", 0)) + int(scan.get("high_count", 0)),
                "workflow_status": status_counts,
            },
            "scan": scan,
        }
        return json.dumps(payload, indent=2, ensure_ascii=True)

    @staticmethod
    def _markdown(scan: dict) -> str:
        findings = scan.get("findings", [])
        status_counts = ReportGenerator._status_counts(findings)
        lines = [
            "# CodeGuard Scan Report",
            "",
            f"Generated: {datetime.utcnow().isoformat()} UTC",
            f"Tool Version: {settings.app_version}",
            "",
            "## Executive Summary",
            f"- Risk Score: {scan.get('risk_score')}",
            f"- Total Issues: {scan.get('total_issues')}",
            f"- Critical or High: {int(scan.get('critical_count', 0)) + int(scan.get('high_count', 0))}",
            f"- Workflow Open: {status_counts['open']}",
            f"- Workflow Reviewing: {status_counts['reviewing']}",
            f"- Workflow Resolved: {status_counts['resolved']}",
            f"- Workflow Ignored: {status_counts['ignored']}",
            "",
            "## Scan Metadata",
            f"- Scan ID: {scan.get('id')}",
            f"- Filename: {scan.get('filename') or 'N/A'}",
            f"- Language: {scan.get('language')}",
            f"- Scanned At: {scan.get('scanned_at')}",
            f"- Duration: {scan.get('duration_ms')} ms",
            "",
            "## Summary",
            f"- Total Issues: {scan.get('total_issues')}",
            f"- Critical: {scan.get('critical_count')}",
            f"- High: {scan.get('high_count')}",
            f"- Medium: {scan.get('medium_count')}",
            f"- Low: {scan.get('low_count')}",
            f"- Info: {scan.get('info_count')}",
            f"- Risk Score: {scan.get('risk_score')}",
            "",
            "## Findings",
        ]

        if not findings:
            lines.append("No vulnerabilities detected.")
        else:
            for idx, finding in enumerate(findings, start=1):
                lines.extend(
                    [
                        f"### {idx}. {finding.get('title')} ({finding.get('severity', '').upper()})",
                        f"- Finding ID: {finding.get('id')}",
                        f"- CWE: {finding.get('cwe_id')}",
                        f"- OWASP: {finding.get('owasp_category')}",
                        f"- Line: {finding.get('line_number')}",
                        f"- Priority Score: {finding.get('priority_score')}",
                        f"- Exploitability: {finding.get('exploitability')}",
                        f"- Status: {finding.get('status', 'open')}",
                        f"- Confidence: {finding.get('confidence')}",
                        f"- Reason: {finding.get('confidence_reason')}",
                        f"- Business Impact: {finding.get('business_impact')}",
                        "",
                        "**Description**",
                        finding.get("description", ""),
                        "",
                        "**Fix Suggestion**",
                        finding.get("fix_suggestion", ""),
                        "",
                        "**Detailed Remediation**",
                        finding.get("detailed_remediation", ""),
                        "",
                    ]
                )

        lines.extend(["## Priority Overview", ""])
        lines.append("Findings are sorted by priority_score descending in CodeGuard UI.")
        return "\n".join(lines)

    @staticmethod
    def _status_counts(findings: list[dict]) -> dict[str, int]:
        counts = {"open": 0, "reviewing": 0, "resolved": 0, "ignored": 0}
        for finding in findings:
            status = finding.get("status", "open")
            if status in counts:
                counts[status] += 1
        return counts

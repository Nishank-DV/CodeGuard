import json
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Optional

from schemas.analysis import AnalysisResult, Vulnerability


class ScanRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create_scan(self, result: AnalysisResult, code_hash: str, filename: Optional[str], duration_ms: int) -> None:
        findings_json = json.dumps([v.model_dump() for v in result.vulnerabilities])
        summary = self._build_finding_summary(result.vulnerabilities)

        self.conn.execute(
            """
            INSERT INTO scans (
                id, code_hash, filename, language, scanned_at, duration_ms,
                total_issues, critical_count, high_count, medium_count, low_count, info_count,
                risk_score, finding_summary, findings_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                result.id,
                code_hash,
                filename,
                result.language,
                result.scanned_at.isoformat(),
                duration_ms,
                result.total_issues,
                result.critical_count,
                result.high_count,
                result.medium_count,
                result.low_count,
                result.info_count,
                result.risk_score,
                summary,
                findings_json,
            ),
        )

        now = datetime.utcnow().isoformat()
        for finding in result.vulnerabilities:
            self.conn.execute(
                """
                INSERT OR IGNORE INTO finding_statuses (
                    scan_id, finding_id, status, remediation_notes, updated_at
                ) VALUES (?, ?, 'open', NULL, ?)
                """,
                (result.id, finding.id, now),
            )

        self.conn.commit()

    def list_scans(
        self,
        page: int = 1,
        page_size: int = 20,
        language: Optional[str] = None,
        min_risk_score: Optional[float] = None,
        sort_by: str = "scanned_at",
        sort_dir: str = "desc",
    ) -> tuple[list[dict[str, Any]], int]:
        allowed_sort = {"scanned_at", "risk_score", "total_issues"}
        if sort_by not in allowed_sort:
            sort_by = "scanned_at"
        if sort_dir.lower() not in {"asc", "desc"}:
            sort_dir = "desc"

        where_clauses = []
        params: list[Any] = []
        if language:
            where_clauses.append("language = ?")
            params.append(language.lower())
        if min_risk_score is not None:
            where_clauses.append("risk_score >= ?")
            params.append(min_risk_score)

        where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

        count_row = self.conn.execute(
            f"SELECT COUNT(1) AS total FROM scans {where_sql}",
            tuple(params),
        ).fetchone()
        total = int(count_row["total"] if count_row else 0)

        offset = (page - 1) * page_size
        rows = self.conn.execute(
            f"""
            SELECT id, filename, language, scanned_at, duration_ms,
                   total_issues, critical_count, high_count, medium_count, low_count, info_count,
                   risk_score, finding_summary
            FROM scans
            {where_sql}
            ORDER BY {sort_by} {sort_dir.upper()}
            LIMIT ? OFFSET ?
            """,
            tuple(params + [page_size, offset]),
        ).fetchall()

        return [dict(row) for row in rows], total

    def get_scan(self, scan_id: str) -> Optional[dict[str, Any]]:
        row = self.conn.execute(
            """
            SELECT * FROM scans WHERE id = ?
            """,
            (scan_id,),
        ).fetchone()
        if not row:
            return None

        scan_data = dict(row)
        findings = json.loads(scan_data["findings_json"])
        statuses = self._get_statuses_for_scan(scan_id)
        for item in findings:
            status = statuses.get(item.get("id"))
            if status:
                item["status"] = status["status"]
                item["remediation_notes"] = status.get("remediation_notes")

        scan_data["findings"] = findings
        return scan_data

    def delete_scan(self, scan_id: str) -> bool:
        cur = self.conn.execute("DELETE FROM scans WHERE id = ?", (scan_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def update_finding_status(
        self, scan_id: str, finding_id: str, status: str, remediation_notes: Optional[str]
    ) -> Optional[dict[str, Any]]:
        now = datetime.utcnow().isoformat()
        self.conn.execute(
            """
            INSERT INTO finding_statuses (scan_id, finding_id, status, remediation_notes, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(scan_id, finding_id)
            DO UPDATE SET status=excluded.status,
                          remediation_notes=excluded.remediation_notes,
                          updated_at=excluded.updated_at
            """,
            (scan_id, finding_id, status, remediation_notes, now),
        )

        row = self.conn.execute(
            """
            SELECT scan_id, finding_id, status, remediation_notes, updated_at
            FROM finding_statuses WHERE scan_id = ? AND finding_id = ?
            """,
            (scan_id, finding_id),
        ).fetchone()
        self.conn.commit()
        if not row:
            return None
        return dict(row)

    def summary(self) -> dict[str, Any]:
        base = self.conn.execute(
            """
            SELECT
                COUNT(*) AS total_scans,
                COALESCE(SUM(total_issues), 0) AS total_vulnerabilities,
                COALESCE(AVG(risk_score), 0) AS average_risk_score,
                COALESCE(AVG(total_issues), 0) AS avg_findings_per_scan,
                COALESCE(SUM(critical_count), 0) AS critical_total,
                COALESCE(SUM(high_count), 0) AS high_total,
                COALESCE(SUM(medium_count), 0) AS medium_total,
                COALESCE(SUM(low_count), 0) AS low_total,
                COALESCE(SUM(info_count), 0) AS info_total
            FROM scans
            """
        ).fetchone()

        language_row = self.conn.execute(
            """
            SELECT language, COUNT(*) AS c
            FROM scans
            GROUP BY language
            ORDER BY c DESC
            LIMIT 1
            """
        ).fetchone()

        high_risk = self.conn.execute(
            """
            SELECT id, risk_score FROM scans ORDER BY risk_score DESC LIMIT 1
            """
        ).fetchone()

        window_start = (datetime.utcnow() - timedelta(days=7)).isoformat()
        weekly = self.conn.execute(
            "SELECT COUNT(*) AS c FROM scans WHERE scanned_at >= ?",
            (window_start,),
        ).fetchone()

        status_rows = self.conn.execute(
            """
            SELECT status, COUNT(*) AS c
            FROM finding_statuses
            GROUP BY status
            """
        ).fetchall()
        status_map = {row["status"]: row["c"] for row in status_rows}

        top_cwes = self._top_cwe_ids(limit=5)
        top_titles = self._top_finding_titles(limit=5)
        language_distribution = self._language_distribution()

        return {
            "total_scans": int(base["total_scans"]),
            "total_vulnerabilities": int(base["total_vulnerabilities"]),
            "average_risk_score": float(base["average_risk_score"]),
            "most_common_language": language_row["language"] if language_row else None,
            "highest_risk_scan_id": high_risk["id"] if high_risk else None,
            "highest_risk_score": float(high_risk["risk_score"]) if high_risk else 0.0,
            "top_cwe_ids": top_cwes,
            "top_finding_titles": top_titles,
            "severity_distribution": {
                "critical": int(base["critical_total"]),
                "high": int(base["high_total"]),
                "medium": int(base["medium_total"]),
                "low": int(base["low_total"]),
                "info": int(base["info_total"]),
            },
            "language_distribution": language_distribution,
            "avg_findings_per_scan": float(base["avg_findings_per_scan"]),
            "scans_last_7_days": int(weekly["c"] if weekly else 0),
            "open_findings": int(status_map.get("open", 0)),
            "reviewing_findings": int(status_map.get("reviewing", 0)),
            "resolved_findings": int(status_map.get("resolved", 0)),
            "ignored_findings": int(status_map.get("ignored", 0)),
            "generated_at": datetime.utcnow().isoformat(),
        }

    def _get_statuses_for_scan(self, scan_id: str) -> dict[str, dict[str, Any]]:
        rows = self.conn.execute(
            """
            SELECT finding_id, status, remediation_notes, updated_at
            FROM finding_statuses
            WHERE scan_id = ?
            """,
            (scan_id,),
        ).fetchall()
        return {
            row["finding_id"]: {
                "status": row["status"],
                "remediation_notes": row["remediation_notes"],
                "updated_at": row["updated_at"],
            }
            for row in rows
        }

    def _top_cwe_ids(self, limit: int = 5) -> list[str]:
        rows = self.conn.execute("SELECT findings_json FROM scans").fetchall()
        cwe_count: dict[str, int] = {}
        for row in rows:
            try:
                findings = json.loads(row["findings_json"])
            except json.JSONDecodeError:
                continue
            for finding in findings:
                cwe = finding.get("cwe_id")
                if cwe:
                    cwe_count[cwe] = cwe_count.get(cwe, 0) + 1

        sorted_cwes = sorted(cwe_count.items(), key=lambda x: x[1], reverse=True)
        return [cwe for cwe, _ in sorted_cwes[:limit]]

    def _top_finding_titles(self, limit: int = 5) -> list[str]:
        rows = self.conn.execute("SELECT findings_json FROM scans").fetchall()
        title_count: dict[str, int] = {}
        for row in rows:
            try:
                findings = json.loads(row["findings_json"])
            except json.JSONDecodeError:
                continue
            for finding in findings:
                title = finding.get("title")
                if title:
                    title_count[title] = title_count.get(title, 0) + 1

        sorted_titles = sorted(title_count.items(), key=lambda x: x[1], reverse=True)
        return [title for title, _ in sorted_titles[:limit]]

    def _language_distribution(self) -> dict[str, int]:
        rows = self.conn.execute(
            """
            SELECT language, COUNT(*) AS c
            FROM scans
            GROUP BY language
            ORDER BY c DESC
            """
        ).fetchall()
        return {row["language"]: int(row["c"]) for row in rows}

    @staticmethod
    def _build_finding_summary(findings: list[Vulnerability]) -> str:
        if not findings:
            return "No vulnerabilities detected"
        top = [f"{f.severity.upper()}: {f.title}" for f in findings[:3]]
        return " | ".join(top)

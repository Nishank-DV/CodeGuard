import sqlite3
from pathlib import Path
from typing import Generator

from config import settings


DB_PATH = Path(settings.sqlite_db_path)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    conn = get_connection()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS scans (
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

            CREATE INDEX IF NOT EXISTS idx_scans_scanned_at ON scans(scanned_at DESC);
            CREATE INDEX IF NOT EXISTS idx_scans_language ON scans(language);
            CREATE INDEX IF NOT EXISTS idx_scans_risk_score ON scans(risk_score DESC);

            CREATE TABLE IF NOT EXISTS finding_statuses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id TEXT NOT NULL,
                finding_id TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'open',
                remediation_notes TEXT,
                updated_at TEXT NOT NULL,
                UNIQUE(scan_id, finding_id),
                FOREIGN KEY(scan_id) REFERENCES scans(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_finding_status_scan_id ON finding_statuses(scan_id);
            """
        )
        conn.commit()
    finally:
        conn.close()

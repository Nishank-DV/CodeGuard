import hashlib
from typing import Optional

from database.session import get_connection
from repositories.scan_repository import ScanRepository
from schemas.analysis import AnalysisResult


class ScanStore:
    @staticmethod
    def store_scan(result: AnalysisResult, code: str, filename: Optional[str], duration_ms: int) -> None:
        code_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
        with get_connection() as conn:
            repo = ScanRepository(conn)
            repo.create_scan(result, code_hash=code_hash, filename=filename, duration_ms=duration_ms)

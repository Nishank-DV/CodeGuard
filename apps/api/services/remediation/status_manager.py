from typing import Optional

from database.session import get_connection
from repositories.scan_repository import ScanRepository


class RemediationStatusManager:
    @staticmethod
    def update_finding_status(scan_id: str, finding_id: str, status: str, remediation_notes: Optional[str]) -> Optional[dict]:
        with get_connection() as conn:
            repo = ScanRepository(conn)
            return repo.update_finding_status(scan_id, finding_id, status, remediation_notes)

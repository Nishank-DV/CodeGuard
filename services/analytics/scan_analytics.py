from database.session import get_connection
from repositories.scan_repository import ScanRepository


class ScanAnalyticsService:
    @staticmethod
    def get_summary() -> dict:
        with get_connection() as conn:
            repo = ScanRepository(conn)
            return repo.summary()

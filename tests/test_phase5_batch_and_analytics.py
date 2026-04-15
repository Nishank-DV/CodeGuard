from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def _headers(key: str = "dev-analyst-key") -> dict[str, str]:
    return {"X-API-Key": key}


def test_batch_scan_handles_partial_failures():
    files = [
        (
            "files",
            ("safe.py", b"print('hello')\n", "text/plain"),
        ),
        (
            "files",
            ("bad.txt", b"not code", "text/plain"),
        ),
    ]

    response = client.post(
        "/analyze/batch-files?continue_on_error=true",
        headers=_headers(),
        files=files,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True

    data = payload["data"]
    assert data["processed_files"] == 2
    assert data["successful_files"] == 1
    assert data["failed_files"] == 1
    assert len(data["files"]) == 2

    failed_items = [item for item in data["files"] if not item["success"]]
    assert failed_items
    assert "File extension not allowed" in failed_items[0]["error"]


def test_summary_exposes_phase5_analytics_fields():
    create = client.post(
        "/analyze",
        headers=_headers(),
        json={"code": "eval(user_input)", "language": "python", "filename": "phase5.py"},
    )
    assert create.status_code == 200

    response = client.get("/scans/summary", headers=_headers())
    assert response.status_code == 200

    data = response.json()
    assert "top_finding_titles" in data
    assert "language_distribution" in data
    assert isinstance(data["top_finding_titles"], list)
    assert isinstance(data["language_distribution"], dict)


def test_live_analysis_does_not_persist_scan_records():
    before_summary = client.get("/scans/summary", headers=_headers())
    assert before_summary.status_code == 200
    before_total_scans = before_summary.json()["total_scans"]

    live = client.post(
        "/analyze/live",
        headers=_headers(),
        json={"code": "eval(user_input)", "language": "python", "filename": "typing_live.py"},
    )
    assert live.status_code == 200
    live_payload = live.json()
    assert live_payload["success"] is True
    assert live_payload["data"]["total_issues"] >= 1

    after_summary = client.get("/scans/summary", headers=_headers())
    assert after_summary.status_code == 200
    after_total_scans = after_summary.json()["total_scans"]

    assert after_total_scans == before_total_scans


def test_report_download_accepts_query_key_for_window_open_flow():
    create = client.post(
        "/analyze",
        headers=_headers(),
        json={"code": "eval(user_input)", "language": "python", "filename": "report_flow.py"},
    )
    assert create.status_code == 200
    scan_id = create.json()["data"]["id"]

    response = client.get(f"/scans/{scan_id}/report?format=md&api_key=dev-analyst-key")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/markdown")
    assert "no-store" in response.headers.get("cache-control", "")
    assert response.headers.get("x-content-type-options") == "nosniff"

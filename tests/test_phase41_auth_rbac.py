from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def _headers(key: str) -> dict[str, str]:
    return {"X-API-Key": key}


def test_missing_api_key_denied():
    response = client.get("/scans")
    assert response.status_code == 401


def test_invalid_api_key_denied():
    response = client.get("/scans", headers=_headers("bad-key"))
    assert response.status_code == 401


def test_viewer_can_read_but_cannot_modify():
    response = client.get("/scans", headers=_headers("dev-viewer-key"))
    assert response.status_code == 200

    response = client.post(
        "/analyze",
        headers=_headers("dev-viewer-key"),
        json={"code": "eval(user_input)", "language": "python"},
    )
    assert response.status_code == 403


def test_analyst_can_analyze_and_update_status_but_not_delete():
    create = client.post(
        "/analyze",
        headers=_headers("dev-analyst-key"),
        json={"code": "eval(user_input)", "language": "python", "filename": "rbac.py"},
    )
    assert create.status_code == 200
    payload = create.json()["data"]
    scan_id = payload["id"]
    finding_id = payload["vulnerabilities"][0]["id"]

    patch = client.patch(
        f"/scans/{scan_id}/findings/{finding_id}",
        headers=_headers("dev-analyst-key"),
        json={"status": "reviewing", "remediation_notes": "triaged"},
    )
    assert patch.status_code == 200

    delete = client.delete(f"/scans/{scan_id}", headers=_headers("dev-analyst-key"))
    assert delete.status_code == 403


def test_admin_can_delete_scan():
    create = client.post(
        "/analyze",
        headers=_headers("dev-admin-key"),
        json={"code": "eval(user_input)", "language": "python", "filename": "admin.py"},
    )
    assert create.status_code == 200
    scan_id = create.json()["data"]["id"]

    delete = client.delete(f"/scans/{scan_id}", headers=_headers("dev-admin-key"))
    assert delete.status_code == 204


def test_whoami_endpoint():
    response = client.get("/auth/whoami", headers=_headers("dev-analyst-key"))
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "analyst"
    assert data["auth_enabled"] is True

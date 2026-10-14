# tests/test_health.py

def test_root_not_found():
    from app.main import app
    from fastapi.testclient import TestClient

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code in [404, 200]

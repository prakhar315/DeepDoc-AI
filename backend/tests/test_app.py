from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_empty_query():
    response = client.post("/search", json={
        "query": "",
        "top_k": 3,
        "department": "HR"
    })
    assert response.status_code == 200
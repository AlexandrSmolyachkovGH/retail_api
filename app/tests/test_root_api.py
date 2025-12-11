from fastapi.testclient import TestClient


def test_root_success(client: TestClient) -> None:
    response = client.get("/")
    data = response.json()

    assert "title" in data
    assert "description" in data
    assert "paths" in data
    assert data["paths"]["health-check"] == "/health"


def test_health_success(client: TestClient) -> None:
    response = client.get("/health")
    data = response.json()

    assert response.status_code == 200
    assert data == {"status": "UP"}

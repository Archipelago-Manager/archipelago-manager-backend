from fastapi.testclient import TestClient


def test_create_game(client: TestClient):
    response = client.post(
            '/games/', json={"name": "test"}
            )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "test"
    assert data["id"] is not None

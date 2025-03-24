from fastapi.testclient import TestClient
from sqlmodel import Session
from app.tests.utils.hub import create_random_hub


def test_create_hub(client: TestClient):
    response = client.post(
            '/hubs/', json={"name": "test", "description": "test description"}
            )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "test"
    assert data["description"] == "test description"
    assert data["id"] is not None


def test_read_hubs(client: TestClient, session: Session):
    hub1 = create_random_hub(session)
    hub2 = create_random_hub(session, description=False)
    response = client.get("/hubs/")
    data = response.json()

    assert response.status_code == 200
    assert data[0]["name"] == hub1.name
    assert data[0]["description"] == hub1.description
    assert data[1]["name"] == hub2.name
    assert data[1]["description"] is None
    assert data[0]["id"] is not None
    assert data[1]["id"] is not None

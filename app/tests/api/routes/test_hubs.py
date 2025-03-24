from fastapi.testclient import TestClient
from sqlmodel import Session
from app.tests.utils.creators import create_random_hub


def test_create_hub(client: TestClient):
    response = client.post(
            '/hubs/', json={"name": "test", "description": "test description"}
            )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "test"
    assert data["description"] == "test description"


def test_create_hub_already_exists(client: TestClient, session: Session):
    hub = create_random_hub(session)
    response = client.post(
            '/hubs/',
            json={"name": hub.name, "description": "test description"}
            )
    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "A hub with this name already exists"


def test_create_hub_without_name(client: TestClient, session: Session):
    response = client.post(
            '/hubs/', json={"name": "", "description": "test description"}
            )
    data = response.json()

    assert response.status_code == 422
    assert data["detail"][0]["msg"] == \
           "String should have at least 1 character"


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


def test_read_hub(client: TestClient, session: Session):
    hub = create_random_hub(session)
    response = client.get(f"/hubs/{hub.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == hub.name
    assert data["description"] == hub.description


def test_read_hub_not_found(client: TestClient, session: Session):
    hub = create_random_hub(session)
    response = client.get(f"/hubs/{hub.id+1}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "Hub not found"


def test_read_hub_from_name(client: TestClient, session: Session):
    hub = create_random_hub(session)
    response = client.get(f"/hubs/get_from_name/{hub.name}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == hub.name
    assert data["description"] == hub.description


def test_read_hub_from_name_not_found(client: TestClient,
                                      session: Session):
    hub = create_random_hub(session)
    response = client.get(f"/hubs/get_from_name/{hub.name + '404'}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "Hub not found"

from fastapi.testclient import TestClient
from app.models.hubs import Hub
from sqlmodel import Session
from app.tests.utils.hub import create_random_game, create_random_user


def test_create_user(client: TestClient, hub: Hub):
    response = client.post(
            f"/hubs/{hub.id}/users/", json={"name": "test"}
            )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "test"
    assert data["user_id"] is not None


def test_read_users(client: TestClient, hub: Hub, session: Session):
    user1 = create_random_user(hub, session)
    user2 = create_random_user(hub, session)
    response = client.get(f"/hubs/{hub.id}/users/")
    data = response.json()

    assert response.status_code == 200
    assert data[0]["name"] == user1.name
    assert data[1]["name"] == user2.name
    assert data[0]["user_id"] == user1.user_id
    assert data[1]["user_id"] == user2.user_id


def test_read_user(client: TestClient, hub: Hub, session: Session):
    user = create_random_user(hub, session)
    response = client.get(f"/hubs/{hub.id}/users/{user.user_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == user.name
    assert data["user_id"] == user.user_id


def test_read_user_user_not_found(client: TestClient,
                                  hub: Hub, session: Session):
    user = create_random_user(hub, session)
    response = client.get(f"/hubs/{hub.id}/users/{user.user_id+1}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "User not found"


def test_read_user_hub_not_found(client: TestClient,
                                 hub: Hub, session: Session):
    user = create_random_user(hub, session)
    response = client.get(f"/hubs/{hub.id+1}/users/{user.user_id}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "Hub not found"


def test_read_user_games(client: TestClient,
                         hub: Hub, session: Session):
    game = create_random_game(hub, session)
    user = create_random_user(hub, session)
    response = client.post(
            f"/hubs/{hub.id}/games/{game.game_id}/add/{user.user_id}"
            )
    assert response.status_code == 200

    response = client.get(f"/hubs/{hub.id}/users/{user.user_id}/games")
    data = response.json()

    assert response.status_code == 200
    assert data[0]["name"] == game.name
    assert data[0]["game_id"] == game.game_id

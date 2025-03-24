from fastapi.testclient import TestClient
from app.models.hubs import Hub
from sqlmodel import Session
from app.tests.utils.hub import create_random_game


def test_create_game(client: TestClient, hub: Hub):
    response = client.post(
            f"/hubs/{hub.id}/games/", json={"name": "test"}
            )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "test"
    assert data["game_id"] is not None


def test_read_games(client: TestClient, hub: Hub, session: Session):
    game1 = create_random_game(hub, session)
    game2 = create_random_game(hub, session)
    response = client.get(f"/hubs/{hub.id}/games/")
    data = response.json()

    assert response.status_code == 200
    assert data[0]["name"] == game1.name
    assert data[1]["name"] == game2.name
    assert data[0]["game_id"] is not None
    assert data[1]["game_id"] is not None


def test_read_game(client: TestClient, hub: Hub, session: Session):
    game = create_random_game(hub, session)
    response = client.get(f"/hubs/{hub.id}/games/{game.game_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == game.name
    assert data["game_id"] is not None


def test_read_game_not_found(client: TestClient, hub: Hub, session: Session):
    game = create_random_game(hub, session)
    response = client.get(f"/hubs/{hub.id}/games/{game.game_id+1}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "Game not found"

from fastapi.testclient import TestClient
from app.models.hubs import Hub
from sqlmodel import Session
from app.tests.utils.creators import create_random_game, create_random_user


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


def test_read_game_game_not_found(client: TestClient,
                                  hub: Hub, session: Session):
    game = create_random_game(hub, session)
    response = client.get(f"/hubs/{hub.id}/games/{game.game_id+1}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "Game not found"


def test_read_game_hub_not_found(client: TestClient,
                                 hub: Hub, session: Session):
    game = create_random_game(hub, session)
    response = client.get(f"/hubs/{hub.id+1}/games/{game.game_id}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "Hub not found"


def test_add_user_to_game(client: TestClient,
                          hub: Hub, session: Session):
    game = create_random_game(hub, session)
    user = create_random_user(hub, session)
    response = client.post(
            f"/hubs/{hub.id}/games/{game.game_id}/add/{user.user_id}"
            )
    data = response.json()

    assert response.status_code == 200
    assert data["users"][0]["name"] == user.name
    assert data["users"][0]["user_id"] == user.user_id
    assert data["name"] == game.name
    assert data["game_id"] == game.game_id


def test_add_user_to_game_not_found(client: TestClient,
                                    hub: Hub, session: Session):
    game = create_random_game(hub, session)
    user = create_random_user(hub, session)
    input_matrix = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    error_matrix = ["Hub", "Game", "User"]
    test_matrix = zip(error_matrix, input_matrix)
    for error, (hub_add, game_add, user_add) in test_matrix:
        hub_id = hub.id + hub_add
        game_id = game.id + game_add
        user_id = user.id + user_add
        response = client.post(
                f"/hubs/{hub_id}/games/{game_id}/add/{user_id}"
                )
        data = response.json()

        assert response.status_code == 404
        assert data["detail"] == f"{error} not found"


def test_add_existing_user_to_game(client: TestClient,
                                   hub: Hub, session: Session):
    game = create_random_game(hub, session)
    user = create_random_user(hub, session)
    response1 = client.post(
            f"/hubs/{hub.id}/games/{game.game_id}/add/{user.user_id}"
            )
    assert response1.status_code == 200
    response2 = client.post(
            f"/hubs/{hub.id}/games/{game.game_id}/add/{user.user_id}"
            )
    data = response2.json()

    assert response2.status_code == 400
    assert data["detail"] == "User already in game"

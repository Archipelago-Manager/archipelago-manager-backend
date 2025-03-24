from sqlmodel import Session
from app.tests.utils.utils import random_lower_string
from app.models.hubs import Hub, HubCreate
from app.models.games import Game, GameCreateInternal


def create_random_hub(session: Session, description=True) -> Hub:
    name = random_lower_string()
    if description:
        description = random_lower_string()
        hub = Hub.model_validate(HubCreate(name=name, description=description))
    else:
        hub = Hub.model_validate(HubCreate(name=name))
    session.add(hub)
    session.commit()
    session.refresh(hub)
    return hub


def create_random_game(hub: Hub,
                       session: Session, description=True) -> Game:
    name = random_lower_string()
    hub_max_game_id = hub.max_game_id + 1
    db_game = Game.model_validate(GameCreateInternal(
        name=name,
        hub_id=hub.id,
        game_id=hub_max_game_id
        ))
    hub.max_game_id = hub_max_game_id
    session.add(db_game)
    session.commit()
    session.refresh(db_game)
    return db_game

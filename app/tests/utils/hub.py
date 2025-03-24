from sqlmodel import Session
from app.tests.utils.utils import random_lower_string
from app.models.hubs import Hub, HubCreate
from app.models.games import Game, GameCreate


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


def create_random_game(hub_id: int,
                       session: Session, description=True) -> Game:
    name = random_lower_string()
    game = Game.model_validate(GameCreate(name=name, description=description,
                                          hub_id=hub_id))
    session.add(game)
    session.commit()
    session.refresh(game)
    return game

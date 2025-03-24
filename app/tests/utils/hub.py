from sqlmodel import Session
from app.tests.utils.utils import random_lower_string
from app.models.hubs import Hub, HubCreate
from app.models.games import Game, GameCreateInternal
from app.models.users import User


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
    new_max_hub_game_id = hub.max_game_id + 1
    db_game = Game.model_validate(GameCreateInternal(
        name=name,
        hub_id=hub.id,
        game_id=new_max_hub_game_id
        ))
    hub.max_game_id = new_max_hub_game_id
    session.add(db_game)
    session.commit()
    session.refresh(db_game)
    return db_game


def create_random_user(hub: Hub, session: Session) -> User:
    name = random_lower_string()
    new_hub_max_user_id = hub.max_user_id + 1
    db_user = User.model_validate(User(
        name=name,
        hub_id=hub.id,
        user_id=new_hub_max_user_id
        ))
    hub.max_user_id = new_hub_max_user_id
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

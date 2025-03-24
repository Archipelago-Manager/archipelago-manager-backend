from asyncio import sleep
from typing import Annotated, List
from fastapi import APIRouter, Query, HTTPException, BackgroundTasks, Depends
from sqlmodel import select
from app.api.deps import SessionDep
from app.models.games import (
        Game,
        GameCreate,
        GameCreateInternal,
        GamePublic,
        GamePublicWithUsers
)
from app.models.users import User
from app.models.hubs import Hub
from app.api.utils import get_and_verify_hub

router = APIRouter(prefix="/hubs/{hub_id}/games", tags=["games"])


async def start_node_and_get_address(game: Game, session: SessionDep):
    await sleep(5)  # Mock API call to node to set up a server node
    game.node_port = 38281
    game.node_address = "localhost"
    session.add(game)
    session.commit()


@router.post("/", response_model=GamePublic)
async def create_game(game: GameCreate, session: SessionDep,
                      background_tasks: BackgroundTasks,
                      hub: Annotated[Hub, Depends(get_and_verify_hub)]
                      ):
    new_max_hub_game_id = hub.max_game_id + 1
    db_game = Game.model_validate(GameCreateInternal(
        name=game.name,
        hub_id=hub.id,
        game_id=new_max_hub_game_id
        ))
    hub.max_game_id = new_max_hub_game_id
    session.add(db_game)
    session.add(hub)
    session.commit()
    session.refresh(db_game)

    background_tasks.add_task(start_node_and_get_address, db_game, session)
    return db_game


@router.get("/", response_model=List[GamePublic])
def read_games(session: SessionDep,
               hub: Annotated[Hub, Depends(get_and_verify_hub)],
               offset: int = 0,
               limit: Annotated[int, Query(le=100)] = 25
               ):
    games = session.exec(select(Game).where(Game.hub_id == hub.id)
                         .offset(offset).limit(limit)).all()
    return games


@router.get("/{game_id}", response_model=GamePublicWithUsers)
def read_game(
        game_id: int,
        session: SessionDep,
        hub: Annotated[Hub, Depends(get_and_verify_hub)]
        ):
    statement = select(Game).where(Game.hub_id == hub.id,
                                   Game.game_id == game_id)
    game = session.exec(statement).one_or_none()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.post("/{game_id}/add/{user_id}", response_model=GamePublicWithUsers)
def add_user_to_game(
        game_id: int, user_id: int, session: SessionDep,
        hub: Annotated[Hub, Depends(get_and_verify_hub)]
        ):
    statement = select(Game).where(Game.hub_id == hub.id,
                                   Game.game_id == game_id)
    game = session.exec(statement).one_or_none()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user in game.users:
        raise HTTPException(status_code=400, detail="User already in game")
    game.users.append(user)
    session.add(game)
    session.commit()

    return game

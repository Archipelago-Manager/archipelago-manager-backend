from typing import Annotated, List
from fastapi import APIRouter, Query, HTTPException
from app.api.deps import SessionDep
from app.models.games import Game, GameCreate, GamePublic, GamePublicWithUsers
from app.models.users import User
from sqlmodel import select

router = APIRouter(prefix="/games", tags=["games"])


@router.post("/", response_model=GamePublic)
def create_game(game: GameCreate, session: SessionDep):
    db_game = Game.model_validate(game)
    session.add(db_game)
    session.commit()
    session.refresh(db_game)
    return db_game


@router.get("/", response_model=List[GamePublic])
def read_games(session: SessionDep,
               offset: int = 0,
               limit: Annotated[int, Query(le=100)] = 25
               ):
    games = session.exec(select(Game).offset(offset).limit(limit)).all()
    return games


@router.post("/{game_id}/add/{user_id}", response_model=GamePublicWithUsers)
def add_user_to_game(game_id: int, user_id: int, session: SessionDep):
    game = session.get(Game, game_id)
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

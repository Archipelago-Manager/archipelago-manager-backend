from typing import Annotated, List
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlmodel import select
from app.api.deps import SessionDep
from app.models.users import User, UserCreate, UserPublic, UserCreateInternal
from app.models.games import GamePublic
from app.models.hubs import Hub
from app.api.utils import get_and_verify_hub

router = APIRouter(prefix="/hubs/{hub_id}/users", tags=["users"])


@router.post("/", response_model=UserPublic)
def create_user(
        user: UserCreate, session: SessionDep,
        hub: Annotated[Hub, Depends(get_and_verify_hub)]
        ):
    new_hub_max_user_id = hub.max_user_id + 1
    db_user = User.model_validate(UserCreateInternal(
        name=user.name,
        hub_id=hub.id,
        user_id=new_hub_max_user_id
        ))
    hub.max_user_id = new_hub_max_user_id
    session.add(db_user)
    session.add(hub)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=List[UserPublic])
def read_users(session: SessionDep,
               hub: Annotated[Hub, Depends(get_and_verify_hub)],
               offset: int = 0,
               limit: Annotated[int, Query(le=100)] = 25
               ):
    users = session.exec(select(User).where(User.hub_id == hub.id)
                         .offset(offset).limit(limit)).all()
    return users


@router.get("/{user_id}", response_model=UserPublic)
def read_user(
        user_id: int,
        session: SessionDep,
        hub: Annotated[Hub, Depends(get_and_verify_hub)]
        ):
    statement = select(User).where(User.hub_id == hub.id,
                                   User.user_id == user_id)
    user = session.exec(statement).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}/games", response_model=List[GamePublic])
def read_user_games(
        user_id: int,
        session: SessionDep,
        hub: Annotated[Hub, Depends(get_and_verify_hub)]
        ):
    statement = select(User).where(User.hub_id == hub.id,
                                   User.user_id == user_id)
    user = session.exec(statement).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.games

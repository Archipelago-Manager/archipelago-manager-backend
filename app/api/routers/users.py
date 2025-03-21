from typing import Annotated, List
from fastapi import APIRouter, Query
from app.api.deps import SessionDep
from app.models.users import User, UserCreate, UserPublic
from sqlmodel import select

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=List[UserPublic])
def read_users(session: SessionDep,
               offset: int = 0,
               limit: Annotated[int, Query(le=100)] = 25
               ):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

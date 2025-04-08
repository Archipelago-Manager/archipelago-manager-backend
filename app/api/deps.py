from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from app.db import session_handler

SessionDep = Annotated[Session, Depends(session_handler.get_session)]

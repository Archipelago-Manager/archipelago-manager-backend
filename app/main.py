from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import create_db_and_tables
from app.api.routers import users, games, hubs
from app.models.configs import YamlFile
from app.models.users import User, UserPublic
from app.models.games import Game, GamePublicWithUsers 
from app.models.hubs import Hub, HubPrivate
from app.models.accounts import Account
from app import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(hubs.router)
app.include_router(users.router)
app.include_router(games.router)

GamePublicWithUsers.model_rebuild()
HubPrivate.model_rebuild()

from fastapi import FastAPI
from app.db import create_db_and_tables
from app.api.routers import users, games
from app.models.configs import YamlFile
from app.models.users import User, UserPublic
from app.models.games import Game, GamePublicWithUsers
from app import models

app = FastAPI()

app.include_router(users.router)
app.include_router(games.router)

GamePublicWithUsers.model_rebuild()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

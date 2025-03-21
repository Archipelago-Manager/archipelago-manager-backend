from fastapi import FastAPI
from app.db import create_db_and_tables
from app.api.routers import users
from app.models.configs import YamlFile
from app.models.games import Game
from app.models.users import User

app = FastAPI()

app.include_router(users.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

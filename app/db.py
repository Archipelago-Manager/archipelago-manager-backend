from sqlmodel import create_engine, SQLModel, Session
import logging
from sqlalchemy import Engine
from app.core.config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if settings.DB_BACKEND == "sqlite":
    connect_args = {"check_same_thread": False}
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI),
                           connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


class SessionHandler():
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_session(self) -> Session:
        with Session(self.engine) as session:
            yield session

    def set_engine(self, engine: Engine):
        self.engine = engine


session_handler = SessionHandler(engine)

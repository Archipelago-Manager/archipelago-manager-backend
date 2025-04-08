import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.db import session_handler
from app.tests.utils.creators import create_random_hub


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    session_handler.set_engine(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    client = TestClient(app)
    yield client


@pytest.fixture(name="hub")
def hub_fixture(session: Session):
    hub = create_random_hub(session)
    yield hub

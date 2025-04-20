import pytest
import shutil
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.db import session_handler
from app.tests.utils.creators import create_random_hub
from app.core.config import settings


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


settings.STORAGE_TYPE = "local"
settings.LOCAL_STORAGE_ROOT_FOLDER = "test_fs"
settings.ENVIRONMENT = "test"


def remove_test_fs():
    shutil.rmtree(settings.LOCAL_STORAGE_ROOT_FOLDER)


@pytest.fixture(autouse=True, scope="session")
def remove_fs(request):
    request.addfinalizer(remove_test_fs)

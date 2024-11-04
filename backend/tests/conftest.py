import pytest
from sqlmodel.pool import StaticPool
from sqlmodel import (
    Session, SQLModel, create_engine
)
from fastapi.testclient import (
    TestClient
)

# import main app, models and get_session
from src import app
from src.db import get_session
from src.apps.auth.models import User



# fixtures

@pytest.fixture(name='session')
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name='client')
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

# in actual tests, session fixture must come before client fixture
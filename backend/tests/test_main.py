import pytest  
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src import app
from src.db import get_session, SessionDep


@pytest.fixture(name="session")  
def session_fixture():  
    engine = create_engine(
        "sqlite:///test_db.db", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session  


def test_main_app(session: Session):  
    def get_session_override():
        return session  

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)


    response = client.get('/test')
    app.dependency_overrides.clear()
    data = response.json()

    assert response.status_code == 200
    assert data['message'] == "Hello World test"

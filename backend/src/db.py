from sqlmodel import (
    create_engine,
    SQLModel,
    Session
)
from src import config
from typing import Annotated
from fastapi import Depends



SQLALCHEMY_DATABASE_URL = config.DATABASE_URL
connection_args = {
    "check_same_thread": False
}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connection_args)


# app -> on startup event
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
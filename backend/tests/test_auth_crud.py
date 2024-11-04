from sqlmodel import select
from src.apps.auth.models import User
from src.apps.auth.utils import generateOtp
from src.apps.auth.crud import (
    get_all
)

def test_user_table_is_empty(session):
    statement = select(User)
    results = session.exec(statement).all()
    assert results == []


def test_user_create(session):
    user1 = User(email='test1@test.com', password='123', vcode=generateOtp())
    session.add(user1)
    session.commit()

    statement = select(User)
    results = session.exec(statement).all()
    assert len(results) == 1
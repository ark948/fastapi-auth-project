from sqlmodel import select
from src.apps.auth.models import User
from src.apps.auth.utils import generateOtp
from src.apps.auth.crud import (
    get_all,
    create,
    show,
    update,
    delete,
    get_user_from_email
)

def test_user_table_is_empty(session):
    statement = select(User)
    results = session.exec(statement).all()
    assert results == []


def test_crud_get_all(session):
    user1 = User(email='test1@test.com', password='123', vcode=generateOtp())
    user2 = User(email='test2@test.com', password='123', vcode=generateOtp())
    session.add(user1)
    session.add(user2)
    session.commit()

    results = get_all(session)

    assert results[0].id == 1
    assert results[0].email == 'test1@test.com'
    assert results[1].id == 2
    assert results[1].email == 'test2@test.com'
    assert type(results) == list


def test_crud_create(session):
    user = User(email='test1@test.com', password='123', vcode=generateOtp())
    result = create(user, session)

    db_user = session.get(User, 1)
    assert db_user.email == user.email
    assert result == db_user
    assert type(result) == User


def test_crud_show(session):
    user = User(email='test1@test.com', password='123', vcode=generateOtp())
    session.add(user)
    session.commit()

    db_user = show(1, session)
    assert user.email == db_user.email
    assert db_user == user
    assert type(db_user) == User


def test_crud_update(session):
    user = User(email='test1@test.com', password='123', vcode=generateOtp())
    session.add(user)
    session.commit()

    db_user = show(1, session)
    assert user == db_user

    user = User(first_name='Neal', last_name='Goldman')
    updateMessage = update(1, user, session)

    assert updateMessage['message'] == "User with 1 updated."

    db_user = show(1, session)
    assert db_user.first_name == 'Neal'
    assert db_user.last_name == 'Goldman'
    assert db_user.email == 'test1@test.com'
    assert type(updateMessage) == dict


def test_crud_delete(session):
    user = User(email='test1@test.com', password='123', vcode=generateOtp())
    session.add(user)
    session.commit()

    db_user = show(1, session)
    assert user == db_user

    message = delete(1, session)
    assert message['ok'] == True

    users_list = get_all(session)
    assert users_list == []
    assert type(message) == dict


def test_crud_get_user_from_email(session):
    user = User(email='test1@test.com', password='123', vcode=generateOtp())
    session.add(user)
    session.commit()

    db_user = show(1, session)
    assert user == db_user    

    userFromEmail = get_user_from_email('test1@test.com', session)
    assert userFromEmail == db_user
    assert userFromEmail == user
    assert userFromEmail.id == db_user.id
    assert type(userFromEmail) == User
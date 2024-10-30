from fastapi import HTTPException, status
from src.auth.schemas import CreateUser
from src.auth.models import User
from src.db import SessionDep
from sqlmodel import select
from src.utils.hash import hash_plain_password


def create(request: CreateUser, db: SessionDep):
    hashed_password = hash_plain_password(request.password)
    new_user = User(email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(id: int, session: SessionDep):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} was not found.")
    return user


def get_user_from_email(email: str, session: SessionDep):
    statement = select(User).where(User.email == email)
    results = session.exec(statement)
    for user in results:
        return user
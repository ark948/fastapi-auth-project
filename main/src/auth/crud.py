from fastapi import HTTPException, status
from src.auth.schemas import CreateUser
from src.auth.models import User
from src.db import SessionDep


def create(request: CreateUser, db: SessionDep):
    new_user = User(email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(id: int, session: SessionDep):
    user = session.get(User, id)
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} was not found.")
    return user
from fastapi import HTTPException, status
from src.apps.auth.schemas import CreateUser
from src.apps.auth.models import User
from src.db import SessionDep
from sqlmodel import select
from src.utils.hash import hash_plain_password, verify_password

def get_all(session: SessionDep):
    statement = select(User)
    results = session.exec(statement)
    return results


def create(request: CreateUser, db: SessionDep):
    new_user = User(email=request.email, password=hash_plain_password(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(id: int, session: SessionDep):
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with {id} was not found."
        )
    return user

def update(id: int, new_email: str, old_password: str, new_password: str, session: SessionDep):
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with {id} was not found."
        )
    if verify_password(old_password, user.password):
        if new_password:
            user.password = hash_plain_password(new_password)
        if new_email:
            user.email = new_email
        return {"message": f"User with {id} updated."}
    

def delete(id: int, session: SessionDep):
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with {id} was not found."
        )
    session.delete(user)
    session.commit()
    return {"message": f"User with {id} deleted."}


def get_user_from_email(email: str, db: SessionDep) -> User:
    statement = select(User).where(User.email == email)
    results = db.exec(statement)
    for user in results:
        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with {email} was not found.")
        return user
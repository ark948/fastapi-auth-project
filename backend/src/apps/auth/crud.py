from fastapi import HTTPException, status
from src.apps.auth.schemas import CreateUser, UpdateUserSQLModel
from src.apps.auth.models import User
from src.db import SessionDep
from sqlmodel import select
from src.apps.auth.hash import hash_plain_password, verify_password

def get_all(session: SessionDep):
    statement = select(User)
    results = session.exec(statement)
    return results


def create(request: CreateUser, db: SessionDep):
    new_user = User(
        email=request.email,
        first_name=request.first_name,
        last_name=request.last_name,
        password=hash_plain_password(request.password),
        is_active=request.is_active
        )
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

def update(id: int, request: UpdateUserSQLModel, session: SessionDep):
    db_user = session.get(User, id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with {id} was not found."
        )
    user_data = request.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
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
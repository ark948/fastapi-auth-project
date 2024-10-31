from datetime import timedelta
from src.apps.auth.schemas import ShowUser, CreateUser
from src.apps.auth import crud
from src import config
from src.db import SessionDep
from fastapi.security import OAuth2PasswordRequestForm
from src.apps.auth.tokens import Token, create_access_token
from src.apps.auth.oauth2 import authenticate_user
from typing import Annotated, List
from src.apps.auth.models import User
from fastapi import (
    APIRouter,
    status,
    HTTPException,
    Depends
)


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.get('/get-all-users', response_model=List[ShowUser])
def get_all_users(session: SessionDep):
    return crud.get_all(session)


@router.post('/create', response_model=CreateUser)
def create_user(request: CreateUser, session: SessionDep) -> User:
    return crud.create(request, session)


@router.get('/{id}', response_model=ShowUser)
def get_user(id: int, session: SessionDep) -> User:
    return crud.show(id, session)


@router.put('/{id}')
def update_user(id: int, session: SessionDep) -> dict:
    return crud.update(id, session)


@router.delete('/{id}')
def delete_user(id: int, session: SessionDep) -> dict:
    return crud.delete(id, session)


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
    ) -> Token:
    user = authenticate_user(email=form_data.username, password=form_data.password, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(config.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
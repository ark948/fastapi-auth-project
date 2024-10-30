from src.auth.schemas import ShowUser, CreateUser
from src.auth import crud
from src.db import SessionDep
from fastapi import (
    APIRouter,
)


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/create', response_model=CreateUser)
def create_user(request: CreateUser, session: SessionDep):
    return crud.create(request, session)


@router.get('/{id}', response_model=ShowUser)
def get_user(id: int, session: SessionDep):
    return crud.show(id, session)
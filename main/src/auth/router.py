from src.auth.schemas import UserSchema
from src.auth.models import User
from src.db import SessionDep
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status
)



router = APIRouter(
    prefix='/auth'
)


@router.post('/create', response_model=UserSchema)
def create_user(request: UserSchema, session: SessionDep):
    new_user = User(email=request.email, password=request.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
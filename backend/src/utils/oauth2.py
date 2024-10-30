from fastapi import (Depends, HTTPException, status)
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from src.auth import crud as user_crud
from src.utils.tokens import TokenData
from src.db import SessionDep
from src import config
from src.utils.hash import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES


def get_user(email: str, session: SessionDep):
    return user_crud.get_user_from_email(email, session)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


def authenticate_user(email: str, password: str, session: SessionDep):
    user = get_user(email=email, session=session)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
from fastapi import (Depends, HTTPException, status)
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from src.auth import crud as user_crud
from src.auth.schemas import TokenData
from src.db import SessionDep
from src import config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES


# tokenUrl will be the URL that frontend will send username and password...
# to get a token


# get_current_usre -> get_user -> user_crud
# login_for_access -> authenticate_user


def get_user(email: str, session: SessionDep):
    return user_crud.get_user_from_email(email=email, session=session)


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
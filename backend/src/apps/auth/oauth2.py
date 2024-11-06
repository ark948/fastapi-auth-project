# local imports
from src.apps.auth.models import User
from src.apps.auth.tokens import TokenData
from src.db import SessionDep
from src.apps.auth.crud import get_user_from_email
from src.apps.auth.hash import verify_password
from src.apps.auth.constants import (
    SECRET_KEY, ALGORITHM
)

# other imports
from fastapi import (
    Depends, HTTPException, status
)
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jwt.exceptions import InvalidTokenError
import jwt

from sqlmodel import select


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_user(email: str, session: SessionDep):
    return get_user_from_email(email, session)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(email=token_data.email, session=session)
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
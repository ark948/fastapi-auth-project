from enum import Enum
from pydantic import BaseModel, ConfigDict

# get user
# create user


class ShowUser(BaseModel):
    email: str
    model_config = ConfigDict(form_attributes=True)


class CreateUser(BaseModel):
    email: str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

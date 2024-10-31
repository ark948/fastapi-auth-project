from pydantic import BaseModel, ConfigDict
from typing import Optional


class ShowUser(BaseModel):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = False
    model_config = ConfigDict(form_attributes=True)


class CreateUser(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str
    is_active: bool = False
    model_config = ConfigDict(form_attributes=True)


from sqlmodel import SQLModel


class GetUserSQLModel(SQLModel):
    id: int

class UpdateUserSQLModel(SQLModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None
    is_active: bool | None = None
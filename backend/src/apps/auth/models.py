from sqlmodel import Field, SQLModel
from typing import Optional


class UserBase(SQLModel):
    email: str = Field(index=True)
    password: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
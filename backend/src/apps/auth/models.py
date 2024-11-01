from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, Required


class UserBase(SQLModel):
    email: str = Field(index=True)
    password: str
    is_active: bool = Field(default=False)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    vcode: str = Field(default=None)

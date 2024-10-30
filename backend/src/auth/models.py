from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str = Field(index=True)
    password: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
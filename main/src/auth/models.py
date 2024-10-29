from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class UserBase(SQLModel):
    email: str = Field(index=True)
    password: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
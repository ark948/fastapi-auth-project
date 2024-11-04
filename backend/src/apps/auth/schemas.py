from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

# EmailStr --> pip install email-validator


class ShowUser(BaseModel):
    id: int
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = False
    vcode: str
    model_config = ConfigDict(form_attributes=True)


class CreateUser(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str
    is_active: bool = False
    model_config = ConfigDict(form_attributes=True)


class VerifyUser(BaseModel):
    vcode: str

from pydantic import BaseModel, ConfigDict
from typing import Optional


class ShowUser(BaseModel):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    model_config = ConfigDict(form_attributes=True)


class CreateUser(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str
    is_active: int = False
    model_config = ConfigDict(form_attributes=True)


class UpdateUser(BaseModel):
    email: str
    first_name: str
    last_name: str
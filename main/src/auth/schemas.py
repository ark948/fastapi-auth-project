from enum import Enum
from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    """
    User Schema
    """
    email: str
    password: str
    # model_config = ConfigDict(form_attributes=True)
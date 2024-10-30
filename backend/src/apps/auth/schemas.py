from pydantic import BaseModel, ConfigDict


class ShowUser(BaseModel):
    id: int
    email: str
    model_config = ConfigDict(form_attributes=True)


class CreateUser(BaseModel):
    email: str
    password: str

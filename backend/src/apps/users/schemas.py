from pydantic import BaseModel, EmailStr




class RegisterUser(BaseModel):
    email: EmailStr
    password: str
    repeat_password: str
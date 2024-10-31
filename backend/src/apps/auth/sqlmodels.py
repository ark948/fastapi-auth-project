from sqlmodel import SQLModel



class UpdateUserSQLModel(SQLModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None
    is_active: bool | None = None
from contextlib import asynccontextmanager
from typing import Annotated

# fastapi imports
from fastapi.staticfiles import StaticFiles
from fastapi import (
    FastAPI, Request, Depends
)

# local imports
from src.db import create_db_and_tables
from src.apps.pages.router import router as pages_router
from src.apps.auth.router import router as auth_router
from src.apps.auth.oauth2 import oauth2_scheme
from src.apps.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\t  --> Server started.")
    create_db_and_tables()
    yield
    print("\t  --> Server shutting down.")


app = FastAPI(lifespan=lifespan)


app.include_router(auth_router)
app.include_router(pages_router)
app.include_router(users_router)



# test this route to check if pytest works
@app.get('/test')
def test_route(request: Request) -> dict:
    return {"message": "Hello World test"}


# demonstration purposes (authorize button must appear)
@app.get('/auth-req')
def secure_route(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    return {'token': token}


app.mount('/static', StaticFiles(directory='static'), name='static')
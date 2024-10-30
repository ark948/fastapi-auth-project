from contextlib import asynccontextmanager
from typing import Annotated

# fastapi imports
from fastapi import (FastAPI, Request, Depends)
from fastapi.staticfiles import StaticFiles

# local imports
from src.db import create_db_and_tables
from src.pages.router import router as pages_router
from src.auth.router import router as auth_router
from src.utils.oauth2 import oauth2_scheme


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--> Server started.")
    create_db_and_tables()
    yield
    print("--> Server shutting down.")


app = FastAPI(lifespan=lifespan)


app.include_router(auth_router)
app.include_router(pages_router)


# test this route to check if pytest works
@app.get('/test')
def test_route(request: Request):
    return 'hello world'


# demonstration purposes (authorize button must appear)
@app.get('/auth-req')
def secure_route(token: Annotated[str, Depends(oauth2_scheme)]):
    return {'token': token}


app.mount('/static', StaticFiles(directory='static'), name='static')
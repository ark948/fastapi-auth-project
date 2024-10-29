from contextlib import asynccontextmanager

# fastapi imports
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# local imports
from src.db import create_db_and_tables
from src.pages.router import router as pages_router
from src.auth.router import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--> Server started.")
    create_db_and_tables()
    yield
    print("--> Server shutting down.")


app = FastAPI(lifespan=lifespan)


app.include_router(auth_router)
app.include_router(pages_router)


app.mount('/static', StaticFiles(directory='static'), name='static')
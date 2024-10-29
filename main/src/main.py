from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.pages.router import router as pages_router


app = FastAPI()


app.include_router(pages_router)


app.mount('/static', StaticFiles(directory='static'), name='static')
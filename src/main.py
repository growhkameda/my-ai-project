# src/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.backend.database import init_db
from src.backend.models import User  # noqa: F401 - テーブル登録のため
from src.backend.routers import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


@app.get("/")
def read_root():
    return {"Hello": "World", "Status": "OK"}
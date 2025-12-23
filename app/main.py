from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.api import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Flash Card"}

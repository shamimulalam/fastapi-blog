from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends
from sentry_sdk.session import Session

from app.database import create_db_and_tables, engine, get_session

from .api import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    yield
    print("Finished up...")
    engine.dispose()


app = FastAPI(lifespan=lifespan)

sessionDep = Annotated[Session, Depends(get_session)]

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Flash Card"}

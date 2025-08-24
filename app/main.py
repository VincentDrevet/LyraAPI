from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.routers import broker
from contextlib import asynccontextmanager
from app.db.database import Base, engine
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.models import device
    from app.models import acl
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(broker.router)

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
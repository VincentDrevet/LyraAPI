from fastapi import FastAPI
from app.routers import devices
from contextlib import asynccontextmanager
from app.db.database import Base, engine
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)



app.include_router(devices.router)
import asyncio
import os

from fastapi import FastAPI

from app.broker import connect_rabbitmq
from app.consumer import start_consumer
from app.db import Base, engine
from app.models import Task
from app.routers.tasks import router as tasks_router

app = FastAPI()

REGION = os.getenv("REGION", "local")


@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)
    await connect_rabbitmq(app)
    asyncio.create_task(start_consumer())


@app.get("/health")
def health():
    return {"region": REGION, "status": "ok"}


app.include_router(tasks_router)
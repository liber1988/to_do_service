import os

from fastapi import FastAPI

from app.broker import connect_broker
from app.db import Base, engine
from app.models import Task
from app.routers.tasks import router as tasks_router

app = FastAPI()

REGION = os.getenv("REGION", "local")


@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)

    connection, channel = await connect_broker()
    app.state.rabbit_connection = connection
    app.state.rabbit_channel = channel


@app.on_event("shutdown")
async def on_shutdown():
    connection = getattr(app.state, "rabbit_connection", None)
    if connection is not None:
        await connection.close()


@app.get("/health")
def health():
    return {"region": REGION, "status": "ok"}


app.include_router(tasks_router)
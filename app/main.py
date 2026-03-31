from fastapi import FastAPI
import os
from app.db import Base, engine
from app.models import Task
from app.routers.tasks import router as tasks_router
app = FastAPI()
REGION = os.getenv("REGION", "local")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {
        "region": REGION,
        "status": "ok",
        }

app.include_router(tasks_router)
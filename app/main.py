from fastapi import FastAPI

from app.db import Base, engine
from app.models import Task
from app.routers.tasks import router as tasks_router
app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(tasks_router)
from fastapi import FastAPI

from app.db import Base, engine
from app.models import Task

app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}
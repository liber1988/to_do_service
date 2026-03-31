import uuid

from pydantic import BaseModel


class ReplicatedTaskCreate(BaseModel):
    task_id: uuid.UUID
    title: str
    description: str | None = None
    deleted: bool = False


class ReplicatedTaskDelete(BaseModel):
    task_id: uuid.UUID
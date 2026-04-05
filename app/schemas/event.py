import uuid

from pydantic import BaseModel


class TaskCreatedEvent(BaseModel):
    event_id: str
    event_type: str = "task.created"
    task_id: uuid.UUID
    title: str
    description: str | None = None


class TaskDeletedEvent(BaseModel):
    event_id: str
    event_type: str = "task.deleted"
    task_id: uuid.UUID
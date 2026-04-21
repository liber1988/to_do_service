import uuid

from pydantic import BaseModel


class TaskCreatedEvent(BaseModel):
    event_id: str
    event_type: str = "task.created"
    source_region: str
    task_id: uuid.UUID
    title: str
    description: str | None = None


class TaskDeletedEvent(BaseModel):
    event_id: str
    event_type: str = "task.deleted"
    source_region: str
    task_id: uuid.UUID
import uuid
from uuid6 import uuid7

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.broker import publish_event
from app.crud.task import create_task, delete_task, get_tasks
from app.dependencies import get_db
from app.schemas.event import TaskCreatedEvent, TaskDeletedEvent
from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(
    task_in: TaskCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    task = create_task(db=db, task_in=task_in)

    event = TaskCreatedEvent(
        event_id=str(uuid7()),
        task_id=task.task_id,
        title=task.title,
        description=task.description,
    )

    await publish_event(
        channel=request.app.state.rabbit_channel,
        routing_key="task.created",
        payload=event.model_dump(mode="json"),
    )

    return task


@router.get("", response_model=TaskListResponse)
def get_tasks_endpoint(
    db: Session = Depends(get_db),
):
    tasks = get_tasks(db=db)
    return {"items": tasks}


@router.delete("/{task_id}", response_model=TaskResponse)
async def delete_task_endpoint(
    task_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
):
    task = delete_task(db=db, task_id=task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    event = TaskDeletedEvent(
        event_id=str(uuid7()),
        task_id=task.task_id,
    )

    await publish_event(
        channel=request.app.state.rabbit_channel,
        routing_key="task.deleted",
        payload=event.model_dump(mode="json"),
    )

    return task
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.task import (
    create_task,
    create_task_from_replication,
    delete_task,
    delete_task_from_replication,
    get_tasks,
)
from app.dependencies import get_db
from app.replication import replicate_create_task, replicate_delete_task
from app.schemas.replication import ReplicatedTaskCreate, ReplicatedTaskDelete
from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse

router = APIRouter(tags=["tasks"])


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
):
    task = create_task(db=db, task_in=task_in)

    replicate_create_task(
        task_id=str(task.task_id),
        title=task.title,
        description=task.description,
    )

    return task


@router.get("/tasks", response_model=TaskListResponse)
def get_tasks_endpoint(
    db: Session = Depends(get_db),
):
    tasks = get_tasks(db=db)
    return {"items": tasks}


@router.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_task_endpoint(
    task_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    task = delete_task(db=db, task_id=task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    replicate_delete_task(task_id=str(task.task_id))

    return task


@router.post(
    "/internal/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def replicate_task_create_endpoint(
    task_in: ReplicatedTaskCreate,
    db: Session = Depends(get_db),
):
    task = create_task_from_replication(db=db, task_in=task_in)
    return task


@router.post("/internal/tasks/delete", response_model=TaskResponse)
def replicate_task_delete_endpoint(
    task_in: ReplicatedTaskDelete,
    db: Session = Depends(get_db),
):
    task = delete_task_from_replication(db=db, task_id=task_in.task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found on replica",
        )

    return task
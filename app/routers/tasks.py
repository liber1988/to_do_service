import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.task import create_task, delete_task, get_tasks
from app.dependencies import get_db
from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
):
    return create_task(db=db, task_in=task_in)


@router.get("", response_model=TaskListResponse)
def get_tasks_endpoint(
    db: Session = Depends(get_db),
):
    tasks = get_tasks(db=db)
    return {"items": tasks}


@router.delete("/{task_id}", response_model=TaskResponse)
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

    return task
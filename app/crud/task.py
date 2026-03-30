import uuid

from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate


def create_task(db: Session, task_in: TaskCreate) -> Task:
    task = Task(
        title=task_in.title,
        description=task_in.description,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(db: Session) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.deleted == False)  # noqa: E712
        .order_by(Task.updated_at.desc())
        .all()
    )


def delete_task(db: Session, task_id: uuid.UUID) -> Task | None:
    task = db.query(Task).filter(Task.task_id == task_id).first()

    if task is None:
        return None

    task.deleted = True
    db.commit()
    db.refresh(task)
    return task
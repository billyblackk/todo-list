from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.task import Task as TaskModel
from app.schemas.task import Task, TaskCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[Task])
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).all()
    return tasks


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    task = TaskModel(
        title=task_in.title, description=task_in.description, is_done=task_in.is_done
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

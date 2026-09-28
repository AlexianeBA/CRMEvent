from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from crmevent.core.security import get_current_user
from crmevent.db.base import get_db
from crmevent.schemas.task import TaskCreate, TaskRead, TaskStatus, TaskUpdate
from crmevent.services import task as service


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return service.create_task(db, data, current_user)


@router.get("/", response_model=list[TaskRead])
def list_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    assigned_user_id: int | None = Query(default=None, gt=0),
    task_status: TaskStatus | None = Query(default=None, alias="status"),
):
    return service.get_tasks(db, current_user, assigned_user_id, task_status.value if task_status else None)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return service.get_task(db, task_id, current_user)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return service.update_task(db, task_id, data, current_user)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service.delete_task(db, task_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

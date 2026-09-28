from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from crmevent.models.event import Event
from crmevent.models.opportunity import Opportunity
from crmevent.models.notification import Notification
from crmevent.models.task import Task
from crmevent.models.users import Users
from crmevent.schemas.notification import NotificationCreate
from crmevent.schemas.task import TaskCreate, TaskUpdate
from crmevent.services.notification import create_notification


TASK_TRANSITIONS = {
    "todo": {"in_progress", "done", "canceled"},
    "in_progress": {"todo", "done", "canceled"},
    "done": set(),
    "canceled": set(),
}


def _get_active_user(db: Session, user_id: int):
    user = db.query(Users).filter(Users.id == user_id, Users.is_active == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur assigné introuvable ou inactif")
    return user


def _validate_relations(db: Session, opportunity_id: int | None, event_id: int | None):
    if opportunity_id is None and event_id is None:
        raise HTTPException(
            status_code=422,
            detail="La tâche doit être liée à une opportunité ou à un événement",
        )
    opportunity = None
    event = None
    if opportunity_id is not None:
        opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunité introuvable")
    if event_id is not None:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Événement introuvable")
    if opportunity and event and event.opportunity_id != opportunity.id:
        raise HTTPException(status_code=422, detail="L'événement n'appartient pas à l'opportunité sélectionnée")


def _notify_assignment(db: Session, task: Task):
    create_notification(db, NotificationCreate(
        user_id=task.assigned_user_id,
        title="Nouvelle tâche assignée",
        message=f"La tâche « {task.title} » vous a été assignée.",
        type="task_assigned",
        severity="info",
        target_url=f"/tasks/{task.id}",
        deduplication_key=f"task-assigned:{task.id}:{task.assigned_user_id}",
        scheduled_at=task.due_at,
    ))


def _archive_task_notifications(db: Session, task_id: int, user_id: int, notification_type: str | None = None):
    query = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.target_url == f"/tasks/{task_id}",
        Notification.archived_at.is_(None),
    )
    if notification_type:
        query = query.filter(Notification.type == notification_type)
    query.update({Notification.archived_at: datetime.now(timezone.utc)}, synchronize_session=False)
    db.commit()


def create_task(db: Session, data: TaskCreate, current_user: Users):
    _get_active_user(db, data.assigned_user_id)
    _validate_relations(db, data.opportunity_id, data.event_id)
    task = Task(**data.model_dump(mode="python"), status="todo", created_by_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    _notify_assignment(db, task)
    return task


def get_tasks(db: Session, current_user: Users, assigned_user_id: int | None = None, status: str | None = None):
    query = db.query(Task)
    if current_user.role not in {"admin", "manager"}:
        query = query.filter(Task.assigned_user_id == current_user.id)
    elif assigned_user_id is not None:
        query = query.filter(Task.assigned_user_id == assigned_user_id)
    if status is not None:
        query = query.filter(Task.status == status)
    return query.order_by(Task.due_at.asc()).all()


def get_task(db: Session, task_id: int, current_user: Users):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    allowed = current_user.role in {"admin", "manager"} or current_user.id in {task.assigned_user_id, task.created_by_id}
    if not allowed:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    return task


def update_task(db: Session, task_id: int, data: TaskUpdate, current_user: Users):
    task = get_task(db, task_id, current_user)
    payload = data.model_dump(exclude_unset=True)
    can_manage = current_user.role in {"admin", "manager"} or current_user.id == task.created_by_id
    if not can_manage and set(payload) - {"status"}:
        raise HTTPException(status_code=403, detail="Vous pouvez uniquement modifier le statut de cette tâche")
    if task.status in {"done", "canceled"}:
        raise HTTPException(status_code=400, detail="Une tâche terminée ou annulée ne peut plus être modifiée")

    previous_assignee = task.assigned_user_id
    if "assigned_user_id" in payload:
        _get_active_user(db, payload["assigned_user_id"])
    if "due_at" in payload:
        due_at = payload["due_at"]
        now = datetime.now(due_at.tzinfo) if due_at.tzinfo else datetime.now()
        if due_at <= now:
            raise HTTPException(status_code=422, detail="L'échéance doit être dans le futur")
    next_opportunity = payload.get("opportunity_id", task.opportunity_id)
    next_event = payload.get("event_id", task.event_id)
    if "opportunity_id" in payload or "event_id" in payload:
        _validate_relations(db, next_opportunity, next_event)
    if "status" in payload:
        new_status = payload.pop("status").value
        if new_status not in TASK_TRANSITIONS.get(task.status, set()):
            raise HTTPException(status_code=400, detail=f"Transition de tâche invalide : {task.status} → {new_status}")
        task.status = new_status
    for key, value in payload.items():
        setattr(task, key, value)
    task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    if task.assigned_user_id != previous_assignee:
        _archive_task_notifications(db, task.id, previous_assignee, "task_assigned")
        _notify_assignment(db, task)
    if "due_at" in payload or task.status in {"done", "canceled"}:
        _archive_task_notifications(db, task.id, task.assigned_user_id, "task_due")
    return task


def delete_task(db: Session, task_id: int, current_user: Users):
    task = get_task(db, task_id, current_user)
    if current_user.role not in {"admin", "manager"} and current_user.id != task.created_by_id:
        raise HTTPException(status_code=403, detail="Vous ne pouvez pas supprimer cette tâche")
    _archive_task_notifications(db, task.id, task.assigned_user_id)
    db.delete(task)
    db.commit()

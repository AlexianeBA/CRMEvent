import logging
import os
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from crmevent.models.activity import Activity
from crmevent.models.event import Event
from crmevent.models.history import HistoryEntry
from crmevent.models.invoice import Invoice
from crmevent.models.notification import Notification
from crmevent.models.opportunity import Opportunity
from crmevent.models.quote import Quote
from crmevent.models.task import Task
from crmevent.models.users import Users
from crmevent.schemas.notification import NotificationCreate
from crmevent.services.email import send_email


EVENT_REMINDER_HOURS = 24
OPPORTUNITY_INACTIVE_DAYS = 7
QUOTE_UNANSWERED_DAYS = 7
INVOICE_DUE_WARNING_DAYS = 3
TASK_DUE_WARNING_HOURS = 24
logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _as_utc(value) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def create_notification(db: Session, data: NotificationCreate):
    existing = db.query(Notification).filter(
        Notification.user_id == data.user_id,
        Notification.deduplication_key == data.deduplication_key,
    ).first()
    if existing:
        _deliver_notification_email(db, existing)
        return existing

    notification = Notification(**data.model_dump(mode="python"))
    db.add(notification)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return db.query(Notification).filter(
            Notification.user_id == data.user_id,
            Notification.deduplication_key == data.deduplication_key,
        ).one()
    db.refresh(notification)
    _deliver_notification_email(db, notification)
    return notification


def _deliver_notification_email(db: Session, notification: Notification):
    enabled = os.getenv("NOTIFICATION_EMAIL_ENABLED", "false").lower() in {"1", "true", "yes", "on"}
    severities = {item.strip() for item in os.getenv("NOTIFICATION_EMAIL_SEVERITIES", "warning,error").split(",")}
    if not enabled or notification.emailed_at or notification.severity not in severities:
        return
    user = db.query(Users).filter(Users.id == notification.user_id, Users.is_active == 1).first()
    if not user:
        return
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")
    target = f"{frontend_url}{notification.target_url}" if notification.target_url else frontend_url
    try:
        send_email(
            recipient=user.email,
            subject=f"CRMEvent — {notification.title}",
            body=f"Bonjour,\n\n{notification.message}\n\nConsulter : {target}\n\nL'équipe CRMEvent",
        )
    except HTTPException:
        logger.exception("Échec de l'envoi email pour la notification %s", notification.id)
        return
    notification.emailed_at = _utc_now()
    db.commit()
    db.refresh(notification)


def get_notifications(db: Session, user_id: int, is_read: bool | None = None, skip: int = 0, limit: int = 50):
    query = db.query(Notification).filter(Notification.user_id == user_id, Notification.archived_at.is_(None))
    if is_read is not None:
        query = query.filter(Notification.is_read.is_(is_read))
    return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()


def get_notification(db: Session, notification_id: int, user_id: int):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id,
        Notification.archived_at.is_(None),
    ).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification introuvable")
    return notification


def mark_notification_as_read(db: Session, notification_id: int, user_id: int):
    notification = get_notification(db, notification_id, user_id)
    if not notification.is_read:
        notification.is_read = True
        notification.read_at = _utc_now()
        db.commit()
        db.refresh(notification)
    return notification


def mark_notification_as_unread(db: Session, notification_id: int, user_id: int):
    notification = get_notification(db, notification_id, user_id)
    if notification.is_read:
        notification.is_read = False
        notification.read_at = None
        db.commit()
        db.refresh(notification)
    return notification


def archive_notification(db: Session, notification_id: int, user_id: int):
    notification = get_notification(db, notification_id, user_id)
    notification.archived_at = _utc_now()
    db.commit()


def mark_all_notifications_as_read(db: Session, user_id: int) -> int:
    count = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read.is_(False),
        Notification.archived_at.is_(None),
    ).update({Notification.is_read: True, Notification.read_at: _utc_now()}, synchronize_session=False)
    db.commit()
    return count


def count_unread_notifications(db: Session, user_id: int):
    count = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read.is_(False),
        Notification.archived_at.is_(None),
    ).count()
    return {"unread_count": count}


def count_notifications_by_type(db: Session, user_id: int):
    counts = db.query(Notification.type, func.count(Notification.id)).filter(
        Notification.user_id == user_id,
        Notification.archived_at.is_(None),
    ).group_by(Notification.type).all()
    return {type_: count for type_, count in counts}


def _create_event_notifications(db: Session, user_id: int, now: datetime):
    limit = now + timedelta(hours=EVENT_REMINDER_HOURS)
    for event in db.query(Event).filter(Event.assigned_user_id == user_id, Event.status == "scheduled").all():
        event_date = _as_utc(event.date)
        if event_date and now.date() <= event_date.date() <= limit.date():
            create_notification(db, NotificationCreate(
                user_id=user_id, title="Événement à venir",
                message=f"« {event.title} » est prévu le {event_date.strftime('%d/%m/%Y à %H:%M')}.",
                type="event_upcoming", severity="info", target_url=f"/events/{event.id}",
                deduplication_key=f"event-upcoming:{event.id}", scheduled_at=event_date,
            ))


def _create_opportunity_notifications(db: Session, user_id: int, now: datetime):
    threshold = now - timedelta(days=OPPORTUNITY_INACTIVE_DAYS)
    opportunities = db.query(Opportunity).filter(
        Opportunity.commercial_id == user_id,
        Opportunity.status.notin_(("closed_won", "closed_lost")),
    ).all()
    for opportunity in opportunities:
        latest_activity = db.query(Activity).filter(Activity.opportunity_id == opportunity.id).order_by(Activity.updated_at.desc()).first()
        last_update = _as_utc(latest_activity.updated_at if latest_activity else opportunity.updated_at)
        if last_update and last_update <= threshold:
            marker = last_update.strftime("%Y%m%d%H%M%S")
            create_notification(db, NotificationCreate(
                user_id=user_id, title="Opportunité sans activité récente",
                message=f"Aucune activité récente n'a été enregistrée pour « {opportunity.title} ».",
                type="opportunity_inactive", severity="warning", target_url=f"/opportunities/{opportunity.id}",
                deduplication_key=f"opportunity-inactive:{opportunity.id}:{marker}",
            ))


def _create_quote_notifications(db: Session, user_id: int, now: datetime):
    threshold = now - timedelta(days=QUOTE_UNANSWERED_DAYS)
    for quote in db.query(Quote).filter(Quote.assigned_user_id == user_id, Quote.status == "sent").all():
        history = db.query(HistoryEntry).filter(
            HistoryEntry.quote_id == quote.id,
            HistoryEntry.action == "status_changed",
        ).order_by(HistoryEntry.created_at.desc()).first()
        sent_at = _as_utc(history.created_at if history else None)
        if sent_at and sent_at <= threshold:
            create_notification(db, NotificationCreate(
                user_id=user_id, title="Devis sans réponse",
                message=f"Le devis {quote.number} est envoyé depuis plus de {QUOTE_UNANSWERED_DAYS} jours.",
                type="quote_unanswered", severity="warning", target_url=f"/quotes/{quote.id}",
                deduplication_key=f"quote-unanswered:{quote.id}:{sent_at.strftime('%Y%m%d%H%M%S')}",
            ))


def _create_invoice_notifications(db: Session, user_id: int, now: datetime):
    invoices = db.query(Invoice).filter(
        Invoice.assigned_user_id == user_id,
        Invoice.status.in_(("sent", "overdue")),
    ).all()
    for invoice in invoices:
        due_at = _as_utc(invoice.due_date)
        if not due_at:
            continue
        if due_at < now:
            if invoice.status != "overdue":
                invoice.status = "overdue"
                db.commit()
            create_notification(db, NotificationCreate(
                user_id=user_id, title="Facture en retard",
                message=f"La facture {invoice.number} est arrivée à échéance.",
                type="invoice_overdue", severity="error", target_url=f"/invoices/{invoice.id}",
                deduplication_key=f"invoice-overdue:{invoice.id}", scheduled_at=due_at,
            ))
        elif due_at <= now + timedelta(days=INVOICE_DUE_WARNING_DAYS):
            create_notification(db, NotificationCreate(
                user_id=user_id, title="Facture bientôt échue",
                message=f"La facture {invoice.number} arrive à échéance le {due_at.strftime('%d/%m/%Y')}.",
                type="invoice_due", severity="warning", target_url=f"/invoices/{invoice.id}",
                deduplication_key=f"invoice-due:{invoice.id}", scheduled_at=due_at,
            ))


def _create_task_notifications(db: Session, user_id: int, now: datetime):
    limit = now + timedelta(hours=TASK_DUE_WARNING_HOURS)
    tasks = db.query(Task).filter(
        Task.assigned_user_id == user_id,
        Task.status.in_(("todo", "in_progress")),
    ).all()
    for task in tasks:
        due_at = _as_utc(task.due_at)
        if due_at and due_at <= limit:
            overdue = due_at < now
            create_notification(db, NotificationCreate(
                user_id=user_id,
                title="Tâche en retard" if overdue else "Tâche bientôt échue",
                message=f"La tâche « {task.title} » est arrivée à échéance." if overdue else f"La tâche « {task.title} » arrive bientôt à échéance.",
                type="task_due",
                severity="error" if overdue else "warning",
                target_url=f"/tasks/{task.id}",
                deduplication_key=f"task-due:{task.id}:{due_at.strftime('%Y%m%d%H%M%S')}:{'overdue' if overdue else 'soon'}",
                scheduled_at=due_at,
            ))


def synchronize_notifications(db: Session, user_id: int):
    now = _utc_now()
    _create_event_notifications(db, user_id, now)
    _create_opportunity_notifications(db, user_id, now)
    _create_quote_notifications(db, user_id, now)
    _create_invoice_notifications(db, user_id, now)
    _create_task_notifications(db, user_id, now)
    return count_unread_notifications(db, user_id)

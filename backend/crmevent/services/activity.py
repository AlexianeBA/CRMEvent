from sqlalchemy.orm import Session
from fastapi import HTTPException
from crmevent.models.activity import Activity
from crmevent.schemas.activity import ActivityCreate, ActivityUpdate, ActivityStatus
from crmevent.services.opportunity import get_opportunity
from datetime import datetime, timezone
from crmevent.services.workflow import ensure_transition_allowed, ACTIVITY_TRANSITIONS
from crmevent.services.email import send_email


def create_activity(db: Session, data: ActivityCreate):
    now = datetime.now(timezone.utc).isoformat()
    payload = data.model_dump()
    payload.update({"status": "draft", "created_at": now, "updated_at": now})
    get_opportunity(db, data.opportunity_id)
    activity = Activity(**payload)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity

def get_activities(db: Session):
    return db.query(Activity).all()

def get_activities_by_opportunity(db: Session, opportunity_id: int):
    return db.query(Activity).filter(Activity.opportunity_id == opportunity_id).order_by(Activity.created_at.desc()).all()


def get_activity(db: Session, activity_id: int):
    return db.query(Activity).filter(Activity.id == activity_id).first()

def update_activity(db: Session, activity_id: int, data: ActivityUpdate):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()

    if not activity:
        raise HTTPException(
            status_code=404,
            detail=f"Activity {activity_id} not found"
        )

    if activity.status in {"done", "canceled"}:
        raise HTTPException(
            status_code=400,
            detail="Cannot update an activity that is done or canceled"
        )

    payload = data.model_dump(exclude_unset=True)

    next_type = payload.get("type", activity.type)
    next_subject = payload.get("email_subject", activity.email_subject)
    if next_type == "email" and not next_subject:
        raise HTTPException(status_code=422, detail="L'objet est obligatoire pour une activité email")
    if next_subject and any(char in next_subject for char in ("\r", "\n")):
        raise HTTPException(status_code=422, detail="L'objet ne peut pas contenir de retour à la ligne")
    if activity.status == "planned" and next_type not in {"call", "meeting"}:
        raise HTTPException(
            status_code=422,
            detail="Une activité planifiée doit être un appel ou une réunion",
        )
    if payload.get("scheduled_at") is not None and next_type not in {"call", "meeting"}:
        raise HTTPException(
            status_code=422,
            detail="Seuls les appels et les réunions peuvent avoir une date planifiée",
        )
    if "scheduled_at" in payload and payload["scheduled_at"] is not None:
        payload["scheduled_at"] = payload["scheduled_at"].isoformat()

    if "opportunity_id" in payload:
        raise HTTPException(
            status_code=400,
            detail="Cannot change the opportunity of an activity"
        )
    
    if "status" in payload:
        new_status = payload.pop("status").value

        ensure_transition_allowed(
            ACTIVITY_TRANSITIONS,
            activity.status,
            new_status,
            "Activity",
        )

        activity.status = new_status

    for key, value in payload.items():
        setattr(activity, key, value)

    activity.updated_at = datetime.now(timezone.utc).isoformat()

    db.commit()
    db.refresh(activity)
    return activity

def update_activity_status(
    db: Session,
    activity_id: int,
    status: ActivityStatus,
    scheduled_at: datetime | None = None,
):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()

    if not activity:
        raise HTTPException(status_code=404, detail=f"Activity {activity_id} not found")

    if activity.status in {"done", "canceled"}:
        raise HTTPException(status_code=400, detail="Cannot update an activity that is done or canceled")

    ensure_transition_allowed(ACTIVITY_TRANSITIONS, activity.status, status.value, "Activity")

    if status == ActivityStatus.planned:
        if activity.type not in {"call", "meeting"}:
            raise HTTPException(
                status_code=422,
                detail="Seuls les appels et les réunions peuvent être planifiés",
            )
        if scheduled_at is None:
            raise HTTPException(status_code=422, detail="La date de planification est obligatoire")

        scheduled_value = scheduled_at
        now = datetime.now(scheduled_value.tzinfo) if scheduled_value.tzinfo else datetime.now()
        if scheduled_value <= now:
            raise HTTPException(status_code=422, detail="La date de planification doit être dans le futur")
        activity.scheduled_at = scheduled_value.isoformat()

    activity.status = status.value
    activity.updated_at = datetime.now(timezone.utc).isoformat()
    db.commit()
    db.refresh(activity)
    return activity

def delete_activity(db: Session, activity: Activity):
    db.delete(activity)
    db.commit()


def send_activity_email(db: Session, activity_id: int, current_user):
    activity = get_activity(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail=f"Activity {activity_id} not found")
    if activity.type != "email":
        raise HTTPException(status_code=422, detail="Cette activité n'est pas un email")
    if activity.status in {"done", "canceled"}:
        raise HTTPException(status_code=400, detail="Cet email est déjà terminé ou annulé")
    if not activity.email_subject:
        raise HTTPException(status_code=422, detail="L'objet de l'email est obligatoire")

    contact = activity.opportunity.contact
    if not contact or not contact.email:
        raise HTTPException(status_code=422, detail="Le contact ne possède pas d'adresse email")

    send_email(
        recipient=contact.email,
        subject=activity.email_subject,
        body=activity.content,
        reply_to=current_user.email,
    )

    activity.status = "done"
    activity.updated_at = datetime.now(timezone.utc).isoformat()
    db.commit()
    db.refresh(activity)
    return activity, contact.email

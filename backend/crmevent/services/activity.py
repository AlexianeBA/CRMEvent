from sqlalchemy.orm import Session
from fastapi import HTTPException
from crmevent.models.activity import Activity
from crmevent.schemas.activity import ActivityCreate, ActivityUpdate, ActivityStatus
from crmevent.services.opportunity import get_opportunity

from crmevent.services.workflow import ensure_transition_allowed, ACTIVITY_TRANSITIONS


def create_activity(db: Session, data: ActivityCreate):
    get_opportunity(db, data.opportunity_id)
    activity = Activity(**data.model_dump())
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

    db.commit()
    db.refresh(activity)
    return activity

def update_activity_status(db: Session, activity_id: int, status: ActivityStatus):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()

    if not activity:
        raise HTTPException(status_code=404, detail=f"Activity {activity_id} not found")

    if activity.status in {"done", "canceled"}:
        raise HTTPException(status_code=400, detail="Cannot update an activity that is done or canceled")

    ensure_transition_allowed(ACTIVITY_TRANSITIONS, activity.status, status.value, "Activity")
    activity.status = status.value
    db.commit()
    db.refresh(activity)
    return activity

def delete_activity(db: Session, activity: Activity):
    db.delete(activity)
    db.commit()
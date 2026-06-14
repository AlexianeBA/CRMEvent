from sqlalchemy.orm import Session
from crmevent.models.activity import Activity
from crmevent.schemas.activity import ActivityCreate, ActivityUpdate
from crmevent.services.opportunity import get_opportunity

def create_activity(db: Session, data: ActivityCreate):
    get_opportunity(db, data.opportunity_id)
    activity = Activity(**data.dict())
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
    if activity:
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(activity, key, value)
        db.commit()
        db.refresh(activity)
        return activity
    return None
def delete_activity(db: Session, activity: Activity):
    db.delete(activity)
    db.commit()
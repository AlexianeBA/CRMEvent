from sqlalchemy.orm import Session
from crmevent.models.activity import Activity
from crmevent.schemas.activity import ActivityCreate

def create_activity(db: Session, data: ActivityCreate):
    activity = Activity(**data.dict())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity

def get_activities(db: Session):
    return db.query(Activity).all()

def get_activities_by_opportunity(db: Session, opportunity_id: int):
    return db.query(Activity).filter(Activity.opportunity_id == opportunity_id).all()


def get_activity(db: Session, activity_id: int):
    return db.query(Activity).filter(Activity.id == activity_id).first()
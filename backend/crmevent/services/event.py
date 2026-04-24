from sqlalchemy import or_
from sqlalchemy.orm import Session

from crmevent.models.event import Event
from crmevent.schemas.event import EventCreate


def create_event(db: Session, data: EventCreate):
    payload = data.dict()

    # Schema has "name", model expects "title"
    if "name" in payload:
        payload["title"] = payload.pop("name")

    event = Event(**payload)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_event(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()


def get_events(
    db: Session,
    company_id: int | None = None,
    opportunity_id: int | None = None,
    assigned_user_id: int | None = None,
    q: str | None = None,
):
    query = db.query(Event)

    if company_id is not None:
        query = query.filter(Event.company_id == company_id)
    if opportunity_id is not None:
        query = query.filter(Event.opportunity_id == opportunity_id)
    if assigned_user_id is not None:
        query = query.filter(Event.assigned_user_id == assigned_user_id)
    if q:
        search = f"%{q}%"
        query = query.filter(
            or_(
                Event.title.ilike(search),
                Event.description.ilike(search),
                Event.location.ilike(search),
            )
        )

    return query.all()
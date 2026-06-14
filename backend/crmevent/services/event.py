from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException


from crmevent.models.event import Event
from crmevent.schemas.event import EventCreate, EventUpdate
from crmevent.services.company import get_company
from crmevent.services.opportunity import get_opportunity
from crmevent.services.contact import get_contact
from crmevent.models.users import Users



def create_event(db: Session, data: EventCreate):
    if not get_company(db, data.company_id):
        raise HTTPException(status_code=404, detail=f"Company {data.company_id} not found")

    if not get_opportunity(db, data.opportunity_id):
        raise HTTPException(status_code=404, detail=f"Opportunity {data.opportunity_id} not found")

    user = db.query(Users).filter(Users.id == data.assigned_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {data.assigned_user_id} not found")

    if data.contact_id is not None and not get_contact(db, data.contact_id):
        raise HTTPException(status_code=404, detail=f"Contact {data.contact_id} not found")

    event = Event(**data.model_dump())
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

def update_event(db: Session, event: Event, data: EventUpdate):
    payload = data.model_dump(exclude_unset=True)

    if "company_id" in payload and not get_company(db, payload["company_id"]):
        raise HTTPException(status_code=404, detail=f"Company {payload['company_id']} not found")

    if "opportunity_id" in payload and not get_opportunity(db, payload["opportunity_id"]):
        raise HTTPException(status_code=404, detail=f"Opportunity {payload['opportunity_id']} not found")

    if "assigned_user_id" in payload:
        user = db.query(Users).filter(Users.id == payload["assigned_user_id"]).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User {payload['assigned_user_id']} not found")

    if "contact_id" in payload and payload["contact_id"] is not None and not get_contact(db, payload["contact_id"]):
        raise HTTPException(status_code=404, detail=f"Contact {payload['contact_id']} not found")

    for key, value in payload.items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event

def delete_event(db: Session, event: Event):
    db.delete(event)
    db.commit()
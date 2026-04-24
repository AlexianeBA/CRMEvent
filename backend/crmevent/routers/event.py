from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from crmevent.db.base import get_db
from crmevent.schemas.event import EventCreate, EventRead
from crmevent.services import event as service

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventRead)
def create(data: EventCreate, db: Session = Depends(get_db)):
    return service.create_event(db, data)


@router.get("/{event_id}", response_model=EventRead)
def get(event_id: int, db: Session = Depends(get_db)):
    event = service.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Not found")
    return event


@router.get("/", response_model=list[EventRead])
def list_all(
    db: Session = Depends(get_db),
    company_id: int | None = Query(default=None),
    opportunity_id: int | None = Query(default=None),
    assigned_user_id: int | None = Query(default=None),
    q: str | None = Query(default=None, description="Recherche nom, description, location"),
):
    return service.get_events(
        db,
        company_id=company_id,
        opportunity_id=opportunity_id,
        assigned_user_id=assigned_user_id,
        q=q,
    )
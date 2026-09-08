from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from crmevent.db.base import get_db
from crmevent.schemas.event import EventCreate, EventRead, EventUpdate, EventStatus
from crmevent.services import event as service
from crmevent.core.security import get_current_user, require_roles
from crmevent.services.history import record_history, status_label

router = APIRouter(prefix="/events", tags=["events"], dependencies=[Depends(get_current_user)])


@router.post("/", response_model=EventRead)
def create(data: EventCreate, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager", "commercial"))):
    event = service.create_event(db, data)
    record_history(db, current_user, "created", "event", event.id, event.title,
                   f"Événement « {event.title} » créé en brouillon", company_id=event.company_id,
                   contact_id=event.contact_id, opportunity_id=event.opportunity_id, event_id=event.id)
    return event


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

@router.patch("/{event_id}", response_model=EventRead)
def update(event_id: int, data: EventUpdate, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager", "commercial"))):
    event = service.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Not found")
    event = service.update_event(db, event, data)
    record_history(db, current_user, "updated", "event", event.id, event.title,
                   f"Événement « {event.title} » modifié", company_id=event.company_id,
                   contact_id=event.contact_id, opportunity_id=event.opportunity_id, event_id=event.id)
    return event

@router.patch("/{event_id}/status", response_model=EventRead)
def update_status(event_id: int, status: EventStatus, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager", "commercial"))):
    event = service.update_event_status(db, event_id, status)
    record_history(db, current_user, "status_changed", "event", event.id, event.title,
                   f"Statut de l'événement passé à « {status_label(status)} »", company_id=event.company_id,
                   contact_id=event.contact_id, opportunity_id=event.opportunity_id, event_id=event.id)
    return event


@router.delete("/{event_id}", response_model=dict)
def delete(event_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager"))):
    event = service.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Not found")
    context = dict(company_id=event.company_id, contact_id=event.contact_id,
                   opportunity_id=event.opportunity_id, event_id=event.id)
    label = event.title
    service.delete_event(db, event)
    record_history(db, current_user, "deleted", "event", event_id, label,
                   f"Événement « {label} » supprimé", **context)
    return {"detail": f"Event {event_id} deleted successfully"}

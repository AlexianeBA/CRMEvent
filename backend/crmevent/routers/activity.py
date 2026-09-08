from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from crmevent.db.base import get_db
from crmevent.schemas.activity import ActivityCreate, ActivityRead, ActivityUpdate, ActivityStatus
from crmevent.services import activity as service
from crmevent.core.security import get_current_user, require_roles
from crmevent.services.history import record_history, status_label
from crmevent.services.opportunity import get_opportunity


router = APIRouter(prefix="/activities", tags=["activities"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=ActivityRead)
def create(data: ActivityCreate, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager", "commercial"))):
    activity = service.create_activity(db, data)
    opportunity = get_opportunity(db, activity.opportunity_id)
    record_history(db, current_user, "created", "opportunity", opportunity.id, opportunity.title,
                   f"Activité « {activity.type} » ajoutée : {activity.content}",
                   company_id=opportunity.company_id, contact_id=opportunity.contact_id,
                   opportunity_id=opportunity.id)
    return activity

@router.get("/", response_model=list[ActivityRead])
def list_by_opportunity(
    db: Session = Depends(get_db),
    opportunity_id: int = Query(..., description="ID de l'opportunité"),
):
    return service.get_activities_by_opportunity(db, opportunity_id)


@router.get("/{activity_id}", response_model=ActivityRead)
def get(activity_id: int, db: Session = Depends(get_db)):
    activity = service.get_activity(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Not found")
    return activity

@router.patch("/{activity_id}", response_model=ActivityRead)
def patch(activity_id: int, data: ActivityUpdate, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager", "commercial"))):
    activity = service.update_activity(db, activity_id, data)
    if not activity:
        raise HTTPException(status_code=404, detail="Not found")
    opportunity = get_opportunity(db, activity.opportunity_id)
    record_history(db, current_user, "updated", "opportunity", opportunity.id, opportunity.title,
                   f"Activité « {activity.type} » modifiée", company_id=opportunity.company_id,
                   contact_id=opportunity.contact_id, opportunity_id=opportunity.id)
    return activity

@router.patch("/{activity_id}/status", response_model=ActivityRead)
def update_status(
    activity_id: int,
    status: ActivityStatus,
    scheduled_at: datetime | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user = Depends(require_roles("admin", "manager", "commercial")),
):
    activity = service.update_activity_status(db, activity_id, status, scheduled_at)
    if not activity:
        raise HTTPException(status_code=404, detail="Not found")
    opportunity = get_opportunity(db, activity.opportunity_id)
    record_history(db, current_user, "status_changed", "opportunity", opportunity.id, opportunity.title,
                   f"Activité passée à « {status_label(status)} »"
                   + (f" pour le {activity.scheduled_at}" if status == ActivityStatus.planned else ""),
                   company_id=opportunity.company_id,
                   contact_id=opportunity.contact_id, opportunity_id=opportunity.id)
    return activity

@router.delete("/{activity_id}", response_model=dict)
def delete(activity_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager"))):
    activity = service.get_activity(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Not found")
    opportunity = get_opportunity(db, activity.opportunity_id)
    content = activity.content
    service.delete_activity(db, activity)
    record_history(db, current_user, "deleted", "opportunity", opportunity.id, opportunity.title,
                   f"Activité supprimée : {content}", company_id=opportunity.company_id,
                   contact_id=opportunity.contact_id, opportunity_id=opportunity.id)
    return {"detail": f"Activity {activity_id} deleted successfully"}

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from crmevent.db.base import get_db
from crmevent.schemas.activity import ActivityCreate, ActivityRead, ActivityUpdate
from crmevent.services import activity as service
from crmevent.core.security import get_current_user


router = APIRouter(prefix="/activities", tags=["activities"])

@router.post("/", response_model=ActivityRead)
def create(data: ActivityCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.create_activity(db, data)

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
def patch(activity_id: int, data: ActivityUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    activity = service.update_activity(db, activity_id, data)
    if not activity:
        raise HTTPException(status_code=404, detail="Not found")
    return activity

@router.patch("/{activity_id}/status", response_model=ActivityRead)
def update_status(activity_id: int, status: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    activity = service.update_activity_status(db, activity_id, status)
    if not activity:
        raise HTTPException(status_code=404, detail="Not found")
    return activity

@router.delete("/{activity_id}", response_model=dict)
def delete(activity_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    activity = service.get_activity(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Not found")
    service.delete_activity(db, activity)
    return {"detail": f"Activity {activity_id} deleted successfully"}

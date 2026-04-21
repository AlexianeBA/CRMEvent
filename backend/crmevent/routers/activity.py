from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from crmevent.db.base import get_db
from crmevent.schemas.activity import ActivityCreate, ActivityRead
from crmevent.services import activity as service


router = APIRouter(prefix="/activities", tags=["activities"])

@router.post("/", response_model=ActivityRead)
def create(data: ActivityCreate, db: Session = Depends(get_db)):
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

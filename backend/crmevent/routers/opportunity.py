from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from crmevent.db.base import get_db
from crmevent.schemas.opportunity import OpportunityCreate, OpportunityRead,OpportunityStatus, OpportunityStatusUpdate
from crmevent.services import opportunity as service

router = APIRouter(prefix="/opportunities", tags=["opportunities"])

@router.post("/", response_model=OpportunityRead)
def create(data: OpportunityCreate, db: Session = Depends(get_db)):
    return service.create_opportunity(db, data)

@router.get("/", response_model=list[OpportunityRead])
def list_all(
    db: Session = Depends(get_db),
    company_id: int | None = Query(default=None),
    contact_id: int | None = Query(default=None),
    status: OpportunityStatus | None = Query(default=None),
    commercial_id: int | None = Query(default=None),
):
    return service.get_opportunities(
        db,
        company_id=company_id,
        contact_id=contact_id,
        status=status,
        commercial_id=commercial_id,
    )

@router.get("/{opportunity_id}", response_model=OpportunityRead)
def get(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = service.get_opportunity(db, opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Not found")
    return opportunity

@router.patch("/{opportunity_id}/status", response_model=OpportunityRead)
def patch_status(opportunity_id: int, data: OpportunityStatusUpdate, db: Session = Depends(get_db)):
    opportunity = service.update_opportunity_status(db, opportunity_id, data.status)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Not found")
    return opportunity
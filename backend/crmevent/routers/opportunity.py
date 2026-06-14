from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from crmevent.db.base import get_db
from crmevent.schemas.opportunity import OpportunityCreate, OpportunityRead,OpportunityStatus, OpportunityStatusUpdate, OpportunityUpdate
from crmevent.models.opportunity import Opportunity
from crmevent.services import opportunity as service
from crmevent.core.security import get_current_user

router = APIRouter(prefix="/opportunities", tags=["opportunities"])

@router.post("/", response_model=OpportunityRead)
def create(data: OpportunityCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.create_opportunity(db, data)

@router.get("/", response_model=list[OpportunityRead])
def list_all(
    db: Session = Depends(get_db),
    company_id: int | None = Query(default=None),
    contact_id: int | None = Query(default=None),
    status: OpportunityStatus | None = Query(default=None),
    commercial_id: int | None = Query(default=None),
    sort_by: str = Query(default="created_at", regex="^(title|amount|status|created_at|updated_at)$"),
    sort_order: str = Query(default="desc", regex="^(asc|desc)$"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
):
    return service.get_opportunities(
        db,
        company_id=company_id,
        contact_id=contact_id,
        status=status,
        commercial_id=commercial_id,
        sort_by=sort_by,
        sort_order=sort_order,
        skip=skip,
        limit=limit
    )

@router.get("/{opportunity_id}", response_model=OpportunityRead)
def get(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = service.get_opportunity(db, opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Not found")
    return opportunity

@router.patch("/{opportunity_id}", response_model=OpportunityRead)
def patch(opportunity_id: int, data: OpportunityUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    opportunity = service.update_opportunity(db, opportunity_id, data)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Not found")
    return opportunity


@router.patch("/{opportunity_id}/status", response_model=OpportunityRead)
def patch_status(opportunity_id: int, data: OpportunityStatusUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    opportunity = service.update_opportunity_status(db, opportunity_id, data.status)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Not found")
    return opportunity

@router.delete("/{opportunity_id}")
def delete(opportunity_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(opportunity)
    db.commit()
    return True
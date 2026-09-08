from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from crmevent.db.base import get_db
from crmevent.schemas.opportunity import OpportunityCreate, OpportunityRead, OpportunityStatus, OpportunityUpdate
from crmevent.services import opportunity as service
from crmevent.core.security import get_current_user, require_roles
from crmevent.services.history import record_history, status_label

router = APIRouter(prefix="/opportunities", tags=["opportunities"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=OpportunityRead)
def create(data: OpportunityCreate, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager", "commercial"))):
    opportunity = service.create_opportunity(db, data)
    record_history(db, current_user, "created", "opportunity", opportunity.id, opportunity.title,
                   f"Opportunité « {opportunity.title} » créée", company_id=opportunity.company_id,
                   contact_id=opportunity.contact_id, opportunity_id=opportunity.id)
    return opportunity

@router.get("/", response_model=list[OpportunityRead])
def list_all(
    db: Session = Depends(get_db),
    company_id: int | None = Query(default=None),
    contact_id: int | None = Query(default=None),
    status: OpportunityStatus | None = Query(default=None),
    commercial_id: int | None = Query(default=None),
    sort_by: str = Query(default="created_at", pattern="^(title|amount|status|created_at|updated_at)$"),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
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
def patch(opportunity_id: int, data: OpportunityUpdate, db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "manager", "commercial")),):
    opportunity = service.update_opportunity(db, opportunity_id, data)
    record_history(db, current_user, "updated", "opportunity", opportunity.id, opportunity.title,
                   f"Opportunité « {opportunity.title} » modifiée", company_id=opportunity.company_id,
                   contact_id=opportunity.contact_id, opportunity_id=opportunity.id)
    return opportunity


@router.patch("/{opportunity_id}/status", response_model=OpportunityRead)
def update_status(opportunity_id: int, status: OpportunityStatus, db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "manager", "commercial")),):
    opportunity = service.update_opportunity_status(db, opportunity_id, status)
    record_history(db, current_user, "status_changed", "opportunity", opportunity.id, opportunity.title,
                   f"Statut de l'opportunité passé à « {status_label(status)} »", company_id=opportunity.company_id,
                   contact_id=opportunity.contact_id, opportunity_id=opportunity.id)
    return opportunity


@router.delete("/{opportunity_id}")
def delete(opportunity_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager"))):
    opportunity = service.get_opportunity(db, opportunity_id)
    context = dict(company_id=opportunity.company_id, contact_id=opportunity.contact_id,
                   opportunity_id=opportunity.id)
    label = opportunity.title
    result = service.delete_opportunity(db, opportunity_id)
    record_history(db, current_user, "deleted", "opportunity", opportunity_id, label,
                   f"Opportunité « {label} » supprimée", **context)
    return result

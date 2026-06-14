from fastapi import HTTPException
from sqlalchemy.orm import Session
from crmevent.models.opportunity import Opportunity
from crmevent.models.company import Company
from crmevent.models.contact import Contact
from crmevent.models.users import Users
from crmevent.schemas.opportunity import OpportunityCreate, OpportunityStatus, OpportunityUpdate

def create_opportunity(db: Session, data: OpportunityCreate):
    company = db.query(Company).filter(Company.id == data.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company {data.company_id} not found")
    
    contact = db.query(Contact).filter(Contact.id == data.contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail=f"Contact {data.contact_id} not found")
    
    commercial = db.query(Users).filter(Users.id == data.commercial_id).first()
    if not commercial:
        raise HTTPException(status_code=404, detail=f"Commercial {data.commercial_id} not found")
    
    opportunity = Opportunity(**data.dict())
    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    return opportunity

def get_opportunities(db: Session, company_id: int | None = None, contact_id: int | None = None, status: str | None = None, commercial_id: int | None = None, sort_by: str | None = None, sort_order: str | None = None, skip: int = 0, limit: int = 100):
    query = db.query(Opportunity)
    if company_id is not None:
        query = query.filter(Opportunity.company_id == company_id)
    if contact_id is not None:
        query = query.filter(Opportunity.contact_id == contact_id)
    if status is not None:
        query = query.filter(Opportunity.status == status)
    if commercial_id is not None:
        query = query.filter(Opportunity.commercial_id == commercial_id)
    
    sort_column = getattr(Opportunity, sort_by, Opportunity.created_at)
    if sort_order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
    query = query.offset(skip).limit(limit)
    return query.all()

def get_opportunity(db: Session, opportunity_id: int):
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail=f"Opportunity {opportunity_id} not found")
    return opportunity

def update_opportunity(db: Session, opportunity_id: int, data: OpportunityUpdate):
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if opportunity:
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(opportunity, key, value)
        db.commit()
        db.refresh(opportunity)
        return opportunity
    raise HTTPException(status_code=404, detail=f"Opportunity {opportunity_id} not found")

def update_opportunity_status( db: Session, opportunity_id: int, status: OpportunityStatus):
    opportunity = get_opportunity(db, opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail=f"Opportunity {opportunity_id} not found")

    opportunity.status = status.value
    db.commit()
    db.refresh(opportunity)
    return opportunity
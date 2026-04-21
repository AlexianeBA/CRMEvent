from sqlalchemy.orm import Session
from crmevent.models.opportunity import Opportunity
from crmevent.schemas.opportunity import OpportunityCreate, OpportunityStatus

def create_opportunity(db: Session, data: OpportunityCreate):
    opportunity = Opportunity(**data.dict())
    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    return opportunity

def get_opportunities(db: Session, company_id: int | None = None, contact_id: int | None = None, status: str | None = None, commercial_id: int | None = None):
    query = db.query(Opportunity)
    if company_id is not None:
        query = query.filter(Opportunity.company_id == company_id)
    if contact_id is not None:
        query = query.filter(Opportunity.contact_id == contact_id)
    if status is not None:
        query = query.filter(Opportunity.status == status)
    if commercial_id is not None:
        query = query.filter(Opportunity.commercial_id == commercial_id)
    return query.all()
    

def get_opportunity(db: Session, opportunity_id: int):
    return db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()

def update_opportunity(db: Session, opportunity_id: int, data: OpportunityCreate):
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if opportunity:
        for key, value in data.dict().items():
            setattr(opportunity, key, value)
        db.commit()
        db.refresh(opportunity)
        return opportunity
    return None

def update_opportunity_status( db: Session, opportunity_id: int, status: OpportunityStatus):
    opportunity = get_opportunity(db, opportunity_id)
    if not opportunity:
        return None

    opportunity.status = status.value
    db.commit()
    db.refresh(opportunity)
    return opportunity
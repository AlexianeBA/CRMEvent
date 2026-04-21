from sqlalchemy.orm import Session
from crmevent.models.opportunity import Opportunity
from crmevent.schemas.opportunity import OpportunityCreate

def create_opportunity(db: Session, data: OpportunityCreate):
    opportunity = Opportunity(**data.dict())
    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    return opportunity

def get_opportunities(db: Session, company_id: int | None = None, contact_id: int | None = None):
    query = db.query(Opportunity)
    if company_id is not None:
        query = query.filter(Opportunity.company_id == company_id)
    if contact_id is not None:
        query = query.filter(Opportunity.contact_id == contact_id)
    return query.all()

def get_opportunity(db: Session, opportunity_id: int):
    return db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()


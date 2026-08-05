from sqlalchemy.orm import Session
from crmevent.models.company import Company
from crmevent.models.contact import Contact
from crmevent.schemas.company import CompanyCreate, CompanyUpdate
from datetime import datetime, timezone
from fastapi import HTTPException

def create_company(db: Session, data: CompanyCreate):
    contact = None

    if data.contact_id is not None:
        contact = (
            db.query(Contact)
            .filter(Contact.id == data.contact_id)
            .first()
        )

        if not contact:
            raise HTTPException(
                status_code=404,
                detail=f"Contact {data.contact_id} not found",
            )
        
    now = datetime.now(timezone.utc).isoformat()

    payload = data.model_dump(exclude={"contact_id"})
    payload.update({"created_at": now, "updated_at": now})
    company = Company(**payload)
    db.add(company)
    db.flush()
    if contact:
        contact.company_id = company.id
    db.commit()
    db.refresh(company)
    return company

def get_companies(db: Session, skip: int = 0, limit: int = 10, q: str | None = None):
    query = db.query(Company)
    
    if q:
        query = query.filter(Company.name.ilike(f"%{q}%"))
    
    return query.offset(skip).limit(limit).all()

def get_company(db: Session, company_id: int):
    return db.query(Company).filter(Company.id == company_id).first()

def update_company(db: Session, company_id: int, data: CompanyUpdate):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        return None
    
    now = datetime.now(timezone.utc).isoformat()
    update_data = data.dict(exclude_unset=True)
    update_data["updated_at"] = now
    
    for key, value in update_data.items():
        setattr(company, key, value)
    
    db.commit()
    db.refresh(company)
    return company

def delete_company(db: Session, company_id: int):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        return False
    
    db.delete(company)
    db.commit()
    return True
from sqlalchemy.orm import Session
from crmevent.models.company import Company
from crmevent.schemas.company import CompanyCreate, CompanyUpdate
from datetime import datetime, timezone

def create_company(db: Session, data: CompanyCreate):
    now = datetime.now(timezone.utc).isoformat()
    payload = data.dict()
    payload.update({"created_at": now, "updated_at": now})
    company = Company(**payload)
    db.add(company)
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
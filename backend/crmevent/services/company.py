from sqlalchemy.orm import Session
from crmevent.models.company import Company
from crmevent.schemas.company import CompanyCreate

def create_company(db: Session, data: CompanyCreate):
    company = Company(**data.dict())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

def get_companies(db: Session):
    return db.query(Company).all()

def get_company(db: Session, company_id: int):
    return db.query(Company).filter(Company.id == company_id).first()
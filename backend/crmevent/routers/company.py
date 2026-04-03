from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crmevent.db.base import get_db
from crmevent.schemas.company import CompanyCreate, CompanyRead
from crmevent.services import company as service

router = APIRouter(prefix="/companies", tags=["companies"])

@router.post("/", response_model=CompanyRead)
def create(data: CompanyCreate, db: Session = Depends(get_db)):
    return service.create_company(db, data)

@router.get("/", response_model=list[CompanyRead])
def list_all(db: Session = Depends(get_db)):
    return service.get_companies(db)

@router.get("/{company_id}", response_model=CompanyRead)
def get(company_id: int, db: Session = Depends(get_db)):
    company = service.get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Not found")
    return company
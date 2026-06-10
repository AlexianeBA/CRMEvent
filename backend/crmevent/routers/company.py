from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from crmevent.db.base import get_db
from crmevent.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate
from crmevent.services import company as service
from crmevent.core.security import get_current_user


router = APIRouter(prefix="/companies", tags=["companies"])

@router.post("/", response_model=CompanyRead)
def create(data: CompanyCreate, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return service.create_company(db, data)

@router.get("/", response_model=list[CompanyRead])
def list_all(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    q: str | None = Query(default=None, description="Recherche par nom"),
):
    return service.get_companies(db, skip=skip, limit=limit, q=q)

@router.get("/{company_id}", response_model=CompanyRead)
def get(company_id: int, db: Session = Depends(get_db)):
    company = service.get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Not found")
    return company

@router.patch("/{company_id}", response_model=CompanyRead)
def update(company_id: int, data: CompanyUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    company = service.update_company(db, company_id, data)
    if not company:
        raise HTTPException(status_code=404, detail="Not found")
    return company

@router.delete("/{company_id}", status_code=204)
def delete(company_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not service.delete_company(db, company_id):
        raise HTTPException(status_code=404, detail="Not found")
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crmevent.db.base import get_db
from crmevent.schemas.contact import ContactCreate, ContactRead
from crmevent.services import contact as service

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactRead)
def create(data: ContactCreate, db: Session = Depends(get_db)):
    return service.create_contact(db, data)

@router.get("/", response_model=list[ContactRead])
def list_all(db: Session = Depends(get_db)):
    return service.get_contacts(db)

@router.get("/{contact_id}", response_model=ContactRead)
def get(contact_id: int, db: Session = Depends(get_db)):
    contact = service.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Not found")
    return contact


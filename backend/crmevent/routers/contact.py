from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from crmevent.db.base import get_db
from crmevent.schemas.contact import ContactCreate, ContactRead
from crmevent.services import contact as service
from crmevent.core.security import get_current_user

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactRead)
def create(data: ContactCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    existing_contact = db.query(service.Contact).filter(
        service.Contact.email == data.email,
        service.Contact.company_id == data.company_id
    ).first()
    if existing_contact:
        raise HTTPException(status_code=400, detail="Contact with this email already exists for the company")
    return service.create_contact(db, data)

@router.get("/", response_model=list[ContactRead])
def list_all(
    db: Session = Depends(get_db),
    company_id: int | None = Query(default=None),
    q: str | None = Query(default=None, description="Recherche nom, prenom, email, phone"),
):
    return service.get_contacts(db, company_id=company_id, q=q)

@router.get("/{contact_id}", response_model=ContactRead)
def get(contact_id: int, db: Session = Depends(get_db)):
    contact = service.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Not found")
    return contact


@router.delete("/{contact_id}", response_model=dict)
def delete(contact_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    contact = service.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Not found")
    service.delete_contact(db, contact)
    return {"detail": f"Contact {contact_id} deleted successfully"}

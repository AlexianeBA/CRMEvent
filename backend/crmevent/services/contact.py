from sqlalchemy.orm import Session
from sqlalchemy import or_
from crmevent.models.contact import Contact
from crmevent.models.company import Company
from crmevent.schemas.contact import ContactCreate, ContactUpdate
from fastapi import HTTPException


def _ensure_company_exists(db: Session, company_id: int | None):
    if company_id is None:
        return

    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Entreprise {company_id} introuvable")


def _ensure_email_available(db: Session, email: str, contact_id: int | None = None):
    query = db.query(Contact).filter(Contact.email == email)
    if contact_id is not None:
        query = query.filter(Contact.id != contact_id)
    if query.first():
        raise HTTPException(status_code=409, detail="Un contact utilise déjà cette adresse email")

def create_contact(db: Session, data: ContactCreate):
    _ensure_company_exists(db, data.company_id)
    _ensure_email_available(db, data.email)
    contact = Contact(**data.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

def get_contacts(db: Session, skip: int = 0, limit: int = 100, company_id: int = None, q: str = None):
    query = db.query(Contact)

    if company_id is not None:
        query = query.filter(Contact.company_id == company_id)

    if q:
        pattern = f"%{q}%"
        query = query.filter(
            or_(
                Contact.first_name.ilike(pattern),
                Contact.last_name.ilike(pattern),
                Contact.email.ilike(pattern),
                Contact.phone_number.ilike(pattern),
            )
        )

    return query.offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def update_contact(db: Session, contact_id: int, data: ContactUpdate):
    
    contact = get_contact(db, contact_id)

    if not contact:
        return None

    payload = data.model_dump(exclude_unset=True)
    if "company_id" in payload:
        _ensure_company_exists(db, payload["company_id"])
    if "email" in payload:
        if payload["email"] is None:
            raise HTTPException(status_code=422, detail="L'adresse email est obligatoire")
        _ensure_email_available(db, payload["email"], contact_id)

    for field, value in payload.items():
        setattr(contact, field, value)

    db.commit()
    db.refresh(contact)

    return contact

def delete_contact(db: Session, contact_id: int):
    contact = get_contact(db, contact_id)

    if not contact:
        return False

    dependencies = []
    if contact.opportunities:
        dependencies.append("opportunités")
    if contact.events:
        dependencies.append("événements")
    if dependencies:
        raise HTTPException(
            status_code=409,
            detail="Suppression impossible : le contact est utilisé par " + ", ".join(dependencies),
        )

    db.delete(contact)
    db.commit()

    return True

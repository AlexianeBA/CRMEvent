from sqlalchemy.orm import Session
from sqlalchemy import or_
from crmevent.models.contact import Contact
from crmevent.schemas.contact import ContactCreate

def create_contact(db: Session, data: ContactCreate):
    contact = Contact(**data.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

def get_contacts(db: Session, company_id: int = None, q: str = None):
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

    return query.all()

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


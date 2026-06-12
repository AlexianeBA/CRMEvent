from sqlalchemy.orm import Session
from sqlalchemy import or_
from crmevent.models.contact import Contact
from crmevent.schemas.contact import ContactCreate, ContactUpdate

def create_contact(db: Session, data: ContactCreate):
    contact = Contact(**data.dict())
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

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)

    db.commit()
    db.refresh(contact)

    return contact

def delete_contact(db: Session, contact_id: int):
    contact = get_contact(db, contact_id)

    if not contact:
        return False

    db.delete(contact)
    db.commit()

    return True
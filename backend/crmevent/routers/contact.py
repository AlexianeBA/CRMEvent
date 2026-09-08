from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from crmevent.db.base import get_db
from crmevent.schemas.contact import ContactCreate, ContactRead, ContactUpdate
from crmevent.services import contact as service
from crmevent.core.security import get_current_user, require_roles
from crmevent.services.history import record_history

router = APIRouter(prefix="/contacts", tags=["contacts"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=ContactRead)
def create(data: ContactCreate, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager", "commercial"))):
    contact = service.create_contact(db, data)
    label = f"{contact.first_name} {contact.last_name}"
    record_history(db, current_user, "created", "contact", contact.id, label,
                   f"Contact « {label} » créé", company_id=contact.company_id, contact_id=contact.id)
    return contact

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

@router.patch("/{contact_id}", response_model=ContactRead)
def update(contact_id: int, data: ContactUpdate, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager", "commercial"))):
    if not service.get_contact(db, contact_id):
        raise HTTPException(status_code=404, detail="Not found")
    contact = service.update_contact(db, contact_id, data)
    label = f"{contact.first_name} {contact.last_name}"
    record_history(db, current_user, "updated", "contact", contact.id, label,
                   f"Contact « {label} » modifié", company_id=contact.company_id, contact_id=contact.id)
    return contact

@router.delete("/{contact_id}", response_model=dict)
def delete(contact_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager"))):
    contact = service.get_contact(db, contact_id)
    label = f"{contact.first_name} {contact.last_name}" if contact else f"Contact {contact_id}"
    company_id = contact.company_id if contact else None
    deleted = service.delete_contact(db, contact_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")

    record_history(db, current_user, "deleted", "contact", contact_id, label,
                   f"Contact « {label} » supprimé", company_id=company_id, contact_id=contact_id)

    return {"detail": (f"Contact {contact_id} "f"deleted successfully"),
    }

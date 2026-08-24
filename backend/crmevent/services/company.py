from sqlalchemy.orm import Session
from crmevent.models.company import Company
from crmevent.models.contact import Contact
from crmevent.schemas.company import CompanyCreate, CompanyUpdate
from datetime import datetime, timezone
from fastapi import HTTPException

def create_company(db: Session, data: CompanyCreate):
    contact_ids = set(data.contact_ids)

    contacts = []

    if contact_ids:
        contacts = (
            db.query(Contact)
            .filter(Contact.id.in_(contact_ids))
            .all()
        )

        found_contact_ids = {
            contact.id for contact in contacts
        }

        missing_contact_ids = (
            contact_ids - found_contact_ids
        )

        if missing_contact_ids:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Contacts introuvables : "
                    f"{sorted(missing_contact_ids)}"
                ),
            )

    now = datetime.now(timezone.utc).isoformat()

    payload = data.model_dump(
        exclude={"contact_ids"},
    )

    payload.update({
        "created_at": now,
        "updated_at": now,
    })

    company = Company(**payload)

    # SQLAlchemy renseignera contacts.company_id
    company.contacts = contacts

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
    
    contact_ids = data.contact_ids

    update_data = data.model_dump(
        exclude_unset=True,
        exclude={"contact_ids"},
    )

    update_data["updated_at"] = (
        datetime.now(timezone.utc).isoformat()
    )
    
    for key, value in update_data.items():
        setattr(company, key, value)

    if contact_ids is not None:
        unique_contact_ids = set(contact_ids)

        contacts = []

        if unique_contact_ids:
            contacts = (
                db.query(Contact)
                .filter(
                    Contact.id.in_(unique_contact_ids)
                )
                .all()
            )

            found_contact_ids = {
                contact.id for contact in contacts
            }

            missing_contact_ids = (
                unique_contact_ids
                - found_contact_ids
            )

            if missing_contact_ids:
                raise HTTPException(
                    status_code=404,
                    detail=(
                        "Contacts introuvables : "
                        f"{sorted(missing_contact_ids)}"
                    ),
                )
        company.contacts = contacts

    db.commit()
    db.refresh(company)
    return company

def delete_company(db: Session, company_id: int):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        return False

    dependencies = []
    if company.opportunities:
        dependencies.append("opportunités")
    if company.events:
        dependencies.append("événements")
    if company.quotes:
        dependencies.append("devis")
    if company.invoices:
        dependencies.append("factures")
    if dependencies:
        raise HTTPException(
            status_code=409,
            detail="Suppression impossible : l'entreprise est utilisée par " + ", ".join(dependencies),
        )

    for contact in company.contacts:
        contact.company_id = None
    
    db.delete(company)
    db.commit()
    return True

from sqlalchemy.orm import Session
from crmevent.models.invoice import Invoice
from crmevent.models.quote import Quote
from crmevent.schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceStatus
from crmevent.services.company import get_company
from crmevent.services.opportunity import get_opportunity
from crmevent.services.event import get_event
from crmevent.models.users import Users
from sqlalchemy import asc, desc


from fastapi import HTTPException

from crmevent.services.workflow import ensure_transition_allowed, INVOICE_TRANSITIONS


IMMUTABLE_FIELDS_AFTER_SENT = {"quote_id", "company_id", "opportunity_id", "assigned_user_id", "number"}

def generate_invoice_number(db: Session):
    last_invoice = db.query(Invoice).order_by(Invoice.id.desc()).first()
    if not last_invoice or not last_invoice.number:
        return "INV-0001"

    try:
        last_number = int(last_invoice.number.split("-")[1])
    except Exception:
        last_number = last_invoice.id

    return f"INV-{last_number + 1:04d}"

def create_invoice_from_quote(db: Session, quote_id: int, user_id: int):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()

    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    if quote.status != "accepted":
        raise HTTPException(status_code=400, detail="Quote must be accepted")

    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    invoice = Invoice(
        number=generate_invoice_number(db),
        title=quote.title,
        total_amount=quote.total_amount,
        company_id=quote.company_id,
        quote_id=quote.id,
        opportunity_id=quote.opportunity_id,
        assigned_user_id=user_id,
        status="draft",
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

def get_invoice(db: Session, invoice_id: int):
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()

ALLOWED_SORT = {
    "id": Invoice.id,
    "number": Invoice.number,
    "total_amount": Invoice.total_amount,
    "created_at": Invoice.created_at,
}


def get_invoices(
    db: Session,
    company_id: int | None = None,
    quote_id: int | None = None,
    opportunity_id: int | None = None,
    assigned_user_id: int | None = None,
    status: InvoiceStatus | None = None,
    sort_by: str = "id",
    sort_order: str = "desc",
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(Invoice)

    if company_id is not None:
        query = query.filter(Invoice.company_id == company_id)

    if quote_id is not None:
        query = query.filter(Invoice.quote_id == quote_id)

    if opportunity_id is not None:
        query = query.filter(Invoice.opportunity_id == opportunity_id)

    if assigned_user_id is not None:
        query = query.filter(Invoice.assigned_user_id == assigned_user_id)

    if status is not None:
        query = query.filter(Invoice.status == status)

    sort_column = ALLOWED_SORT.get(sort_by, Invoice.id)

    if sort_order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    return query.offset(skip).limit(limit).all()


def update_invoice(db: Session, invoice: Invoice, data: InvoiceUpdate):
    payload = data.model_dump(exclude_unset=True)

    if invoice.status in {"paid", "canceled", "locked"}:
        raise HTTPException(status_code=400, detail="Invoice is locked")

    if invoice.status in {"sent", "overdue"}:
        forbidden = IMMUTABLE_FIELDS_AFTER_SENT.intersection(payload.keys())
        if forbidden:
            raise HTTPException(status_code=400, detail=f"Immutable fields after sent: {', '.join(sorted(forbidden))}")

    if "status" in payload:
        new_status = payload.pop("status").value
        ensure_transition_allowed(INVOICE_TRANSITIONS, invoice.status, new_status, "Invoice")
        invoice.status = new_status

    for key, value in payload.items():
        setattr(invoice, key, value)

    db.commit()
    db.refresh(invoice)
    return invoice

def update_invoice_status(db: Session, invoice_id: int, status: InvoiceStatus):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail=f"Invoice {invoice_id} not found")

    ensure_transition_allowed(INVOICE_TRANSITIONS, invoice.status, status.value, "Invoice")
    invoice.status = status.value
    db.commit()
    db.refresh(invoice)
    return invoice

def delete_invoice(db: Session, invoice: Invoice):
    if invoice.status in {"sent", "paid", "overdue", "locked"}:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete invoice after workflow start",
        )

    db.delete(invoice)
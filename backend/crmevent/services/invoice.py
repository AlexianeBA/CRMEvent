from sqlalchemy.orm import Session
from crmevent.models.invoice import Invoice, InvoicePayment
from crmevent.models.quote import Quote
from crmevent.schemas.invoice import InvoiceUpdate, InvoiceStatus, InvoicePaymentCreate
from crmevent.models.users import Users
from crmevent.models.notification import Notification
from sqlalchemy import asc, desc
from datetime import datetime, timedelta, timezone
from decimal import Decimal


from fastapi import HTTPException

from crmevent.services.workflow import ensure_transition_allowed, INVOICE_TRANSITIONS


IMMUTABLE_FIELDS_AFTER_SENT = {
    "quote_id", "company_id", "opportunity_id", "assigned_user_id",
    "number", "title", "total_amount",
}


def _set_billing_notifications_archived(db: Session, invoice: Invoice, archived: bool):
    values = {Notification.archived_at: datetime.now(timezone.utc)} if archived else {
        Notification.archived_at: None,
        Notification.is_read: False,
        Notification.read_at: None,
    }
    db.query(Notification).filter(
        Notification.target_url == f"/invoices/{invoice.id}",
        Notification.type.in_(("invoice_due", "invoice_overdue")),
    ).update(values, synchronize_session=False)

def generate_invoice_number(db: Session):
    last_invoice = db.query(Invoice).order_by(Invoice.id.desc()).first()
    if not last_invoice or not last_invoice.number:
        return "INV-0001"

    try:
        last_number = int(last_invoice.number.split("-")[1])
    except Exception:
        last_number = last_invoice.id

    return f"INV-{last_number + 1:04d}"

def create_invoice_from_quote(db: Session, quote_id: int):
    existing_invoice = (
        db.query(Invoice)
        .filter(Invoice.quote_id == quote_id)
        .first()
    )

    if existing_invoice:
        return existing_invoice

    quote = db.query(Quote).filter(Quote.id == quote_id).first()

    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    if quote.status != "accepted":
        raise HTTPException(status_code=400, detail="Quote must be accepted")

    user = db.query(Users).filter(Users.id == quote.assigned_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    invoice = Invoice(
        number=generate_invoice_number(db),
        title=quote.title,
        total_amount=quote.total_amount,
        company_id=quote.company_id,
        quote_id=quote.id,
        opportunity_id=quote.opportunity_id,
        assigned_user_id=quote.assigned_user_id,
        status="draft",
        issue_date=datetime.now(timezone.utc),
        due_date=datetime.now(timezone.utc) + timedelta(days=30),
        payment_terms="Paiement à 30 jours",
        amount_paid=Decimal("0.00"),
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

def get_invoice(db: Session, invoice_id: int):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if invoice:
        refresh_invoice_status(db, invoice)
    return invoice


def refresh_invoice_status(db: Session, invoice: Invoice, commit: bool = True):
    now = datetime.now(timezone.utc)
    due_date = invoice.due_date
    if due_date and due_date.tzinfo is None:
        now = now.replace(tzinfo=None)
    new_status = invoice.status
    if invoice.status not in {"draft", "canceled", "locked"}:
        if invoice.amount_paid >= invoice.total_amount:
            new_status = "paid"
        elif due_date and due_date < now:
            new_status = "overdue"
        else:
            new_status = "sent"
    if new_status != invoice.status:
        invoice.status = new_status
        if commit:
            db.commit()
            db.refresh(invoice)
    return invoice

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

    invoices_to_refresh = query.filter(Invoice.status.in_(("sent", "overdue", "paid"))).all()
    changed = False
    for invoice in invoices_to_refresh:
        previous_status = invoice.status
        refresh_invoice_status(db, invoice, commit=False)
        changed = changed or previous_status != invoice.status
    if changed:
        db.commit()

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

    if {"due_date", "issue_date", "payment_terms"}.intersection(payload) and invoice.status != "draft":
        raise HTTPException(status_code=400, detail="Les conditions et dates ne peuvent être modifiées que sur une facture en brouillon")

    issue_date = payload.get("issue_date", invoice.issue_date)
    due_date = payload.get("due_date", invoice.due_date)
    comparable_issue = issue_date.astimezone(timezone.utc).replace(tzinfo=None) if issue_date and issue_date.tzinfo else issue_date
    comparable_due = due_date.astimezone(timezone.utc).replace(tzinfo=None) if due_date and due_date.tzinfo else due_date
    if comparable_issue and comparable_due and comparable_due <= comparable_issue:
        raise HTTPException(status_code=422, detail="La date d'échéance doit être postérieure à la date d'émission")

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

    if status == InvoiceStatus.paid and invoice.amount_paid < invoice.total_amount:
        raise HTTPException(status_code=400, detail="La facture ne peut être payée que lorsque son solde est nul")
    if status == InvoiceStatus.overdue:
        raise HTTPException(status_code=400, detail="Le statut en retard est déterminé automatiquement")
    ensure_transition_allowed(INVOICE_TRANSITIONS, invoice.status, status.value, "Invoice")
    invoice.status = status.value
    if invoice.status in {"paid", "canceled", "locked"}:
        _set_billing_notifications_archived(db, invoice, True)
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
    db.commit()


def add_payment(db: Session, invoice: Invoice, data: InvoicePaymentCreate):
    refresh_invoice_status(db, invoice)
    if invoice.status not in {"sent", "overdue"}:
        raise HTTPException(status_code=400, detail="Les paiements sont possibles uniquement sur une facture envoyée")
    amount = Decimal(str(data.amount)).quantize(Decimal("0.01"))
    if amount > invoice.balance_remaining:
        raise HTTPException(status_code=422, detail="Le paiement dépasse le solde restant")
    payment = InvoicePayment(
        invoice_id=invoice.id,
        amount=amount,
        paid_at=data.paid_at or datetime.now(timezone.utc),
        payment_method=data.payment_method,
        reference=data.reference,
        notes=data.notes,
    )
    invoice.amount_paid += amount
    db.add(payment)
    refresh_invoice_status(db, invoice, commit=False)
    if invoice.status == "paid":
        _set_billing_notifications_archived(db, invoice, True)
    db.commit()
    db.refresh(payment)
    db.refresh(invoice)
    return payment


def delete_payment(db: Session, invoice: Invoice, payment_id: int):
    if invoice.status == "locked":
        raise HTTPException(status_code=400, detail="Une facture verrouillée ne peut plus être modifiée")
    payment = db.query(InvoicePayment).filter(
        InvoicePayment.id == payment_id,
        InvoicePayment.invoice_id == invoice.id,
    ).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Paiement introuvable")
    invoice.amount_paid = max(invoice.amount_paid - payment.amount, Decimal("0.00"))
    db.delete(payment)
    refresh_invoice_status(db, invoice, commit=False)
    if invoice.status in {"sent", "overdue"}:
        _set_billing_notifications_archived(db, invoice, False)
    db.commit()

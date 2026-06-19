from sqlalchemy.orm import Session
from crmevent.models.quote import Quote
from crmevent.schemas.quote import QuoteCreate, QuoteStatus
from crmevent.services.company import get_company
from crmevent.services.opportunity import get_opportunity
from crmevent.services.event import get_event
from crmevent.models.users import Users
from crmevent.services.workflow import ensure_transition_allowed, QUOTE_TRANSITIONS, block_if_final_status
from crmevent.services.invoice import create_invoice_from_quote

from fastapi import HTTPException

IMMUTABLE_AFTER_SENT = {"number", "company_id", "opportunity_id", "assigned_user_id", "event_id"}
IMMUTABLE_AFTER_FINAL = {"number", "title", "total_amount", "company_id", "opportunity_id", "assigned_user_id", "event_id", "status"}
ALLOWED_SORT = {
    "id": Quote.id,
    "title": Quote.title,
    "total_amount": Quote.total_amount,
}

def accept_quote(db: Session, quote_id: int, user_id: int):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    ensure_transition_allowed(QUOTE_TRANSITIONS, quote.status, "accepted", "Quote")
    quote.status = "accepted"

    invoice = create_invoice_from_quote(db, quote.id, user_id)
    db.commit()
    db.refresh(quote)
    return quote, invoice

def generate_quote_number(db: Session):

    last_quote = db.query(Quote).order_by(Quote.id.desc()).first()
    if not last_quote or not last_quote.number:
        return "Q-0001"

    try:
        last_number = int(last_quote.number.split("-")[1])
    except Exception:
        last_number = last_quote.id

    return f"Q-{last_number + 1:04d}"

def create_quote(db: Session, data: QuoteCreate):
    if not get_company(db, data.company_id):
        raise HTTPException(status_code=404, detail=f"Company {data.company_id} not found")

    if not get_opportunity(db, data.opportunity_id):
        raise HTTPException(status_code=404, detail=f"Opportunity {data.opportunity_id} not found")

    user = db.query(Users).filter(Users.id == data.assigned_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {data.assigned_user_id} not found")

    if data.event_id is not None and not get_event(db, data.event_id):
        raise HTTPException(status_code=404, detail=f"Event {data.event_id} not found")
    payload = data.model_dump()
    payload["number"] = generate_quote_number(db)
    quote = Quote(**payload)
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote

def get_quote(db: Session, quote_id: int):
    return db.query(Quote).filter(Quote.id == quote_id).first()

def get_quotes(db: Session, company_id: int | None = None, opportunity_id: int | None = None, assigned_user_id: int | None = None, event_id: int | None = None, q: str | None = None, sort_order: str = "desc", sort_by: str | None = None):
    query = db.query(Quote)

    if company_id is not None:
        query = query.filter(Quote.company_id == company_id)
    if opportunity_id is not None:
        query = query.filter(Quote.opportunity_id == opportunity_id)
    if assigned_user_id is not None:
        query = query.filter(Quote.assigned_user_id == assigned_user_id)
    if event_id is not None:
        query = query.filter(Quote.event_id == event_id)
    if q:
        search = f"%{q}%"
        query = query.filter(Quote.title.ilike(search))

    sort_column = ALLOWED_SORT.get(sort_by, Quote.id)

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    return query.all()

def update_quote(db: Session, quote: Quote, data):
    payload = data.model_dump(exclude_unset=True)

    if quote.status in {"accepted", "rejected", "expired", "locked"}:
        raise HTTPException(status_code=400, detail=f"Quote is locked in status {quote.status}")
    
    if quote.status in {"sent"}:
        forbidden = IMMUTABLE_AFTER_SENT.intersection(payload.keys())
        if forbidden:
            raise HTTPException(
                status_code=400,
                detail=f"Immutable fields for Quote after sent: {', '.join(sorted(forbidden))}",
            )
    if "status" in payload:
        new_status = payload.pop("status").value
        ensure_transition_allowed(QUOTE_TRANSITIONS, quote.status, new_status, "Quote")
        quote.status = new_status

    for key, value in payload.items():
        setattr(quote, key, value)

    db.commit()
    db.refresh(quote)
    return quote

def update_quote_status(db: Session, quote_id: int, status: QuoteStatus):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail=f"Quote {quote_id} not found")

    ensure_transition_allowed(QUOTE_TRANSITIONS, quote.status, status.value, "Quote")
    quote.status = status.value
    db.commit()
    db.refresh(quote)
    return quote

def delete_quote(db: Session, quote: Quote):
    if quote.status in {"sent", "accepted", "rejected", "expired", "locked"}:
        raise HTTPException(status_code=400, detail="Cannot delete a quote after it enters workflow")
    db.delete(quote)
    db.commit()
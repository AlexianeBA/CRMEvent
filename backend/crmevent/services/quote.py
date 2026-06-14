from sqlalchemy.orm import Session
from crmevent.models.quote import Quote
from crmevent.schemas.quote import QuoteCreate
from crmevent.services.company import get_company
from crmevent.services.opportunity import get_opportunity
from crmevent.services.event import get_event
from crmevent.models.users import Users

from fastapi import HTTPException

ALLOWED_SORT = {
    "id": Quote.id,
    "title": Quote.title,
    "total_amount": Quote.total_amount,
}

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
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(quote, key, value)

    db.commit()
    db.refresh(quote)
    return quote

def delete_quote(db: Session, quote: Quote):
    db.delete(quote)
    db.commit()
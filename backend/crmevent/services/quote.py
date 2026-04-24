from sqlalchemy.orm import Session
from crmevent.models.quote import Quote
from crmevent.schemas.quote import QuoteCreate

def create_quote(db: Session, data: QuoteCreate):
    quote = Quote(**data.dict())
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote

def get_quote(db: Session, quote_id: int):
    return db.query(Quote).filter(Quote.id == quote_id).first()

def get_quotes(db: Session, company_id: int | None = None, opportunity_id: int | None = None, assigned_user_id: int | None = None, event_id: int | None = None, q: str | None = None):
    query = db.query(Quote)
    if company_id:
        query = query.filter(Quote.company_id == company_id)
    if opportunity_id:
        query = query.filter(Quote.opportunity_id == opportunity_id)
    if assigned_user_id:
        query = query.filter(Quote.assigned_user_id == assigned_user_id)
    if event_id:
        query = query.filter(Quote.event_id == event_id)
    if q:
        search = f"%{q}%"
        query = query.filter(Quote.title.ilike(search))
    return query.all()

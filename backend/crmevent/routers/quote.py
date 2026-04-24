from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from crmevent.db.base import get_db
from crmevent.schemas.quote import QuoteCreate, QuoteRead
from crmevent.services import quote as service

router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.post("/", response_model=QuoteRead)
def create(data: QuoteCreate, db: Session = Depends(get_db)):
    return service.create_quote(db, data)


@router.get("/{quote_id}", response_model=QuoteRead)
def get(quote_id: int, db: Session = Depends(get_db)):
    quote = service.get_quote(db, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Not found")
    return quote


@router.get("/", response_model=list[QuoteRead])
def list_all(
    db: Session = Depends(get_db),
    company_id: int | None = Query(default=None),
    opportunity_id: int | None = Query(default=None),
    assigned_user_id: int | None = Query(default=None),
    event_id: int | None = Query(default=None),
    q: str | None = Query(default=None, description="Recherche titre"),
):
    return service.get_quotes(
        db,
        company_id=company_id,
        opportunity_id=opportunity_id,
        assigned_user_id=assigned_user_id,
        event_id=event_id,
        q=q,
    )
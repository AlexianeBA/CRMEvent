from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from crmevent.db.base import get_db
from crmevent.schemas.quote import QuoteCreate, QuoteRead, QuoteStatus, QuoteUpdate
from crmevent.services import quote as service
from crmevent.core.security import get_current_user

router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.post("/", response_model=QuoteRead)
def create(data: QuoteCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.create_quote(db, data)

@router.post("/{quote_id}/accept")
def accept_quote(quote_id: int, user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user),):
    return service.accept_quote(db, quote_id, user_id)

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

@router.patch("/{quote_id}", response_model=QuoteRead)
def update(quote_id: int, data: QuoteUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    quote = service.get_quote(db, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Not found")
    return service.update_quote(db, quote, data)

@router.patch("/{quote_id}/status", response_model=QuoteRead)
def update_status(quote_id: int, status: QuoteStatus, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.update_quote_status(db, quote_id, status)

@router.delete("/{quote_id}", response_model=dict)
def delete(quote_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    quote = service.update_quote_worflow(db, quote_id, QuoteStatus.deleted)
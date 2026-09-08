from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from crmevent.core.security import get_current_user
from crmevent.db.base import get_db
from crmevent.schemas.history import HistoryRead
from crmevent.services.history import get_history


router = APIRouter(prefix="/history", tags=["history"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[HistoryRead])
def list_history(
    db: Session = Depends(get_db),
    company_id: int | None = Query(default=None, gt=0),
    contact_id: int | None = Query(default=None, gt=0),
    opportunity_id: int | None = Query(default=None, gt=0),
    event_id: int | None = Query(default=None, gt=0),
    quote_id: int | None = Query(default=None, gt=0),
    invoice_id: int | None = Query(default=None, gt=0),
    limit: int = Query(default=100, ge=1, le=200),
):
    return get_history(
        db,
        limit=limit,
        company_id=company_id,
        contact_id=contact_id,
        opportunity_id=opportunity_id,
        event_id=event_id,
        quote_id=quote_id,
        invoice_id=invoice_id,
    )

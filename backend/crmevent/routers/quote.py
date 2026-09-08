from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from crmevent.db.base import get_db
from crmevent.schemas.quote import QuoteCreate, QuoteRead, QuoteStatus, QuoteUpdate
from crmevent.services import quote as service
from crmevent.core.security import get_current_user, require_roles
from crmevent.services.history import record_history, status_label

router = APIRouter(prefix="/quotes", tags=["quotes"], dependencies=[Depends(get_current_user)])


@router.post("/", response_model=QuoteRead)
def create(data: QuoteCreate, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager", "commercial"))):
    quote = service.create_quote(db, data)
    record_history(db, current_user, "created", "quote", quote.id, quote.number,
                   f"Devis {quote.number} créé", company_id=quote.company_id,
                   opportunity_id=quote.opportunity_id, event_id=quote.event_id, quote_id=quote.id)
    return quote

@router.post("/{quote_id}/accept")
def accept_quote(quote_id: int, db: Session = Depends(get_db), current_user=Depends(require_roles("admin", "manager", "commercial")),):
    quote, invoice = service.accept_quote(db, quote_id)
    context = dict(company_id=quote.company_id, opportunity_id=quote.opportunity_id,
                   event_id=quote.event_id, quote_id=quote.id)
    record_history(db, current_user, "status_changed", "quote", quote.id, quote.number,
                   f"Devis {quote.number} accepté", **context)
    record_history(db, current_user, "created", "invoice", invoice.id, invoice.number,
                   f"Facture {invoice.number} générée depuis le devis {quote.number}",
                   company_id=invoice.company_id, opportunity_id=invoice.opportunity_id,
                   quote_id=quote.id, invoice_id=invoice.id)
    return {"quote": quote, "invoice": invoice}

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
def update(quote_id: int, data: QuoteUpdate, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager", "commercial"))):
    quote = service.get_quote(db, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Not found")
    quote = service.update_quote(db, quote, data)
    record_history(db, current_user, "updated", "quote", quote.id, quote.number,
                   f"Devis {quote.number} modifié", company_id=quote.company_id,
                   opportunity_id=quote.opportunity_id, event_id=quote.event_id, quote_id=quote.id)
    return quote

@router.patch("/{quote_id}/status", response_model=QuoteRead)
def update_status(quote_id: int, status: QuoteStatus, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager", "commercial"))):
    quote = service.update_quote_status(db, quote_id, status)
    record_history(db, current_user, "status_changed", "quote", quote.id, quote.number,
                   f"Statut du devis passé à « {status_label(status)} »", company_id=quote.company_id,
                   opportunity_id=quote.opportunity_id, event_id=quote.event_id, quote_id=quote.id)
    return quote

@router.delete("/{quote_id}", response_model=dict)
def delete(quote_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager"))):
    quote = service.get_quote(db, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Not found")
    context = dict(company_id=quote.company_id, opportunity_id=quote.opportunity_id,
                   event_id=quote.event_id, quote_id=quote.id)
    label = quote.number
    service.delete_quote(db, quote)
    record_history(db, current_user, "deleted", "quote", quote_id, label,
                   f"Devis {label} supprimé", **context)
    return {"detail": "Quote deleted successfully"}

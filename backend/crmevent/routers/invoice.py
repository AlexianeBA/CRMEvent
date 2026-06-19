from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from crmevent.db.base import get_db
from crmevent.models.invoice import Invoice
from crmevent.schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceStatus, InvoiceUpdate
from crmevent.services import invoice as service
from crmevent.core.security import get_current_user

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("/", response_model=InvoiceRead)
def create_from_quote(quote_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return service.create_invoice_from_quote(db, quote_id, current_user.id)

@router.get("/", response_model=list[InvoiceRead])
def list_all(
    db: Session = Depends(get_db),
    company_id: int | None = Query(default=None),
    quote_id: int | None = Query(default=None),
    opportunity_id: int | None = Query(default=None),
    assigned_user_id: int | None = Query(default=None),
    event_id: int | None = Query(default=None),
):
    return service.get_invoices(
        db,
        company_id=company_id,
        quote_id=quote_id,
        opportunity_id=opportunity_id,
        assigned_user_id=assigned_user_id,
        event_id=event_id,
    )

@router.get("/{invoice_id}", response_model=InvoiceRead)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = service.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Not found")
    return invoice

@router.patch("/{invoice_id}", response_model=InvoiceRead)
def update_invoice(
    invoice_id: int,
    data: InvoiceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    invoice = service.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Not found")

    return service.update_invoice(db, invoice, data)

@router.patch("/{invoice_id}/status", response_model=InvoiceRead)
def patch_status(
    invoice_id: int,
    status: InvoiceStatus,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.update_invoice_status(db, invoice_id, status)

@router.delete("/{invoice_id}", response_model=dict)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    invoice = service.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Not found")
    service.delete_invoice(db, invoice)
    return {"detail": f"Invoice {invoice_id} deleted successfully"}



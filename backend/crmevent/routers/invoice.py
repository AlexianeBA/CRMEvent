from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from crmevent.db.base import get_db
from crmevent.models.invoice import Invoice
from crmevent.schemas.invoice import InvoiceRead, InvoiceStatus, InvoiceUpdate
from crmevent.services import invoice as service
from crmevent.core.security import get_current_user, require_roles
from crmevent.services.history import record_history, status_label

router = APIRouter(prefix="/invoices", tags=["invoices"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=InvoiceRead)
def create_from_quote(quote_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager", "comptable"))):
    invoice = service.create_invoice_from_quote(db, quote_id)
    record_history(db, current_user, "created", "invoice", invoice.id, invoice.number,
                   f"Facture {invoice.number} générée depuis un devis", company_id=invoice.company_id,
                   opportunity_id=invoice.opportunity_id, quote_id=invoice.quote_id, invoice_id=invoice.id)
    return invoice

@router.get("/", response_model=list[InvoiceRead])
def list_all(
    db: Session = Depends(get_db),
    company_id: int | None = Query(default=None),
    quote_id: int | None = Query(default=None),
    opportunity_id: int | None = Query(default=None),
    assigned_user_id: int | None = Query(default=None),
    status: InvoiceStatus | None = Query(default=None),
):
    return service.get_invoices(
        db,
        company_id=company_id,
        quote_id=quote_id,
        opportunity_id=opportunity_id,
        assigned_user_id=assigned_user_id,
        status=status,
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
    current_user=Depends(require_roles("admin", "manager", "comptable")),
):
    invoice = service.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Not found")

    invoice = service.update_invoice(db, invoice, data)
    record_history(db, current_user, "updated", "invoice", invoice.id, invoice.number,
                   f"Facture {invoice.number} modifiée", company_id=invoice.company_id,
                   opportunity_id=invoice.opportunity_id, quote_id=invoice.quote_id, invoice_id=invoice.id)
    return invoice

@router.patch("/{invoice_id}/status", response_model=InvoiceRead)
def patch_status(
    invoice_id: int,
    status: InvoiceStatus,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager", "comptable")),
):
    invoice = service.update_invoice_status(db, invoice_id, status)
    record_history(db, current_user, "status_changed", "invoice", invoice.id, invoice.number,
                   f"Statut de la facture passé à « {status_label(status)} »", company_id=invoice.company_id,
                   opportunity_id=invoice.opportunity_id, quote_id=invoice.quote_id, invoice_id=invoice.id)
    return invoice

@router.delete("/{invoice_id}", response_model=dict)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db), current_user = Depends(require_roles("admin", "manager", "comptable"))):
    invoice = service.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Not found")
    context = dict(company_id=invoice.company_id, opportunity_id=invoice.opportunity_id,
                   quote_id=invoice.quote_id, invoice_id=invoice.id)
    label = invoice.number
    service.delete_invoice(db, invoice)
    record_history(db, current_user, "deleted", "invoice", invoice_id, label,
                   f"Facture {label} supprimée", **context)
    return {"detail": f"Invoice {invoice_id} deleted successfully"}

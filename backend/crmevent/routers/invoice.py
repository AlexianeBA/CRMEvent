from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from crmevent.db.base import get_db
from crmevent.models.invoice import Invoice
from crmevent.schemas.invoice import InvoiceRead, InvoiceStatus, InvoiceUpdate, InvoicePaymentCreate, InvoicePaymentRead
from crmevent.services import invoice as service
from crmevent.core.security import get_current_user, require_roles
from crmevent.services.history import record_history, status_label
from crmevent.services.document_export import generate_pdf, invoices_excel

router = APIRouter(prefix="/invoices", tags=["invoices"], dependencies=[Depends(get_current_user)])


@router.get("/export/excel")
def export_excel(
    db: Session = Depends(get_db),
    company_id: int | None = Query(default=None),
    quote_id: int | None = Query(default=None),
    opportunity_id: int | None = Query(default=None),
    assigned_user_id: int | None = Query(default=None),
    status: InvoiceStatus | None = Query(default=None),
):
    invoices = service.get_invoices(db, company_id=company_id, quote_id=quote_id,
        opportunity_id=opportunity_id, assigned_user_id=assigned_user_id, status=status)
    return StreamingResponse(
        invoices_excel(invoices),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="factures.xlsx"'},
    )

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


@router.get("/{invoice_id}/pdf")
def download_pdf(invoice_id: int, db: Session = Depends(get_db)):
    invoice = service.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Not found")
    content = generate_pdf("invoice.html", invoice=invoice, status=invoice.status)
    return Response(content=content, media_type="application/pdf", headers={
        "Content-Disposition": f'attachment; filename="{invoice.number}.pdf"',
    })

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


@router.post("/{invoice_id}/payments", response_model=InvoicePaymentRead, status_code=201)
def create_payment(
    invoice_id: int,
    data: InvoicePaymentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager", "comptable")),
):
    invoice = service.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Not found")
    payment = service.add_payment(db, invoice, data)
    record_history(db, current_user, "payment_added", "invoice", invoice.id, invoice.number,
                   f"Paiement de {payment.amount} € enregistré", company_id=invoice.company_id,
                   opportunity_id=invoice.opportunity_id, quote_id=invoice.quote_id, invoice_id=invoice.id)
    return payment


@router.get("/{invoice_id}/payments", response_model=list[InvoicePaymentRead])
def list_payments(invoice_id: int, db: Session = Depends(get_db)):
    invoice = service.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Not found")
    return invoice.payments


@router.delete("/{invoice_id}/payments/{payment_id}", status_code=204)
def remove_payment(
    invoice_id: int,
    payment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager", "comptable")),
):
    invoice = service.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Not found")
    service.delete_payment(db, invoice, payment_id)
    record_history(db, current_user, "payment_deleted", "invoice", invoice.id, invoice.number,
                   "Paiement supprimé", company_id=invoice.company_id, opportunity_id=invoice.opportunity_id,
                   quote_id=invoice.quote_id, invoice_id=invoice.id)

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

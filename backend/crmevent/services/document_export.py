import os
from decimal import Decimal
from io import BytesIO
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from weasyprint import HTML


TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates" / "documents"
templates = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)

STATUS_LABELS = {
    "draft": "Brouillon", "sent": "Envoyé", "accepted": "Accepté",
    "rejected": "Refusé", "expired": "Expiré", "locked": "Verrouillé",
    "scheduled": "Planifié", "held": "Réalisé", "canceled": "Annulé",
    "paid": "Payée", "overdue": "En retard",
}


def organization_settings():
    return {
        "name": os.getenv("ORGANIZATION_NAME", "CRMEvent"),
        "address": os.getenv("ORGANIZATION_ADDRESS", ""),
        "postal_code": os.getenv("ORGANIZATION_POSTAL_CODE", ""),
        "city": os.getenv("ORGANIZATION_CITY", ""),
        "country": os.getenv("ORGANIZATION_COUNTRY", "France"),
        "email": os.getenv("ORGANIZATION_EMAIL", ""),
        "phone": os.getenv("ORGANIZATION_PHONE", ""),
        "siret": os.getenv("ORGANIZATION_SIRET", ""),
        "vat_number": os.getenv("ORGANIZATION_VAT_NUMBER", ""),
        "legal_notice": os.getenv("ORGANIZATION_LEGAL_NOTICE", ""),
        "registration_notice": os.getenv(
            "ORGANIZATION_REGISTRATION_NOTICE",
            "Dispense d'immatriculation au RCS et au RM.",
        ),
        "late_penalty_rate": os.getenv("LATE_PAYMENT_PENALTY_RATE", "8.25"),
        "recovery_fee": os.getenv("RECOVERY_FEE_AMOUNT", "30"),
        "bank_name": os.getenv("ORGANIZATION_BANK_NAME", ""),
        "iban": os.getenv("ORGANIZATION_IBAN", ""),
        "bic": os.getenv("ORGANIZATION_BIC", ""),
    }


def generate_pdf(template_name: str, **context) -> bytes:
    document = context.get("invoice") or context.get("quote")
    exported_entity = document or context.get("event")
    vat_rate = Decimal(str(getattr(document, "vat_rate", os.getenv("DEFAULT_VAT_RATE", "20"))))
    total_excl_tax = Decimal(str(document.total_amount)) if document else Decimal("0")
    lines = list(getattr(document, "lines", []) or [])
    vat_amount = (sum((line.vat_amount for line in lines), Decimal("0.00")) if lines else total_excl_tax * vat_rate / Decimal("100")).quantize(Decimal("0.01"))
    template = templates.get_template(template_name)
    html = template.render(
        organization=organization_settings(),
        vat_rate=vat_rate,
        total_excl_tax=total_excl_tax,
        vat_amount=vat_amount,
        total_incl_tax=total_excl_tax + vat_amount,
        lines=lines,
        customer=getattr(exported_entity, "company", None),
        status_label=STATUS_LABELS.get(str(context.get("status", "")), str(context.get("status", ""))),
        **context,
    )
    return HTML(string=html, base_url=str(TEMPLATE_DIR)).write_pdf()


def generate_table_excel(sheet_name: str, headers: list[str], rows: list[list]) -> BytesIO:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = sheet_name[:31]
    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = f"A1:{get_column_letter(len(headers))}1"
    worksheet.append(headers)

    header_fill = PatternFill("solid", fgColor="1D4ED8")
    for cell in worksheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")

    for row in rows:
        worksheet.append(row)

    for column_index, header in enumerate(headers, start=1):
        values = [str(worksheet.cell(row=row, column=column_index).value or "") for row in range(1, worksheet.max_row + 1)]
        worksheet.column_dimensions[get_column_letter(column_index)].width = min(max(len(header) + 2, max(map(len, values)) + 2), 45)

    output = BytesIO()
    workbook.save(output)
    output.seek(0)
    return output


def invoices_excel(invoices) -> BytesIO:
    return generate_table_excel("Factures", [
        "Numéro", "Titre", "Client", "Émission", "Échéance", "Statut",
        "Montant HT", "TVA", "Montant TTC", "Montant payé", "Solde restant",
    ], [[
        item.number, item.title, item.company.name, item.issue_date, item.due_date, item.status,
        float(item.total_amount), float(item.vat_amount), float(item.total_incl_tax),
        float(item.amount_paid), float(item.balance_remaining),
    ] for item in invoices])


def quotes_excel(quotes) -> BytesIO:
    return generate_table_excel("Devis", [
        "Numéro", "Titre", "Client", "Opportunité", "Événement", "Statut", "Montant total",
    ], [[
        item.number, item.title, item.company.name, item.opportunity.title,
        item.event.title if item.event else "", item.status, float(item.total_amount),
    ] for item in quotes])


def events_excel(events) -> BytesIO:
    return generate_table_excel("Événements", [
        "Titre", "Type", "Date", "Durée (h)", "Lieu", "Entreprise", "Contact", "Statut",
    ], [[
        item.title, item.type, item.date, item.duration, item.location, item.company.name,
        f"{item.contact.first_name} {item.contact.last_name}" if item.contact else "", item.status,
    ] for item in events])

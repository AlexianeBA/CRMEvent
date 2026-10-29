"""Shared list queries. Legacy endpoints remain available for form selectors."""
import csv
from dataclasses import dataclass, field
from io import BytesIO, StringIO
from math import ceil

from fastapi import HTTPException
from fastapi.responses import Response
from openpyxl import Workbook
from sqlalchemy import String, and_, case, cast, func, or_, select
from sqlalchemy.orm import selectinload

from crmevent.models.activity import Activity
from crmevent.models.company import Company
from crmevent.models.contact import Contact
from crmevent.models.event import Event
from crmevent.models.history import HistoryEntry
from crmevent.models.invoice import Invoice, InvoiceLine
from crmevent.models.notification import Notification
from crmevent.models.opportunity import Opportunity
from crmevent.models.quote import Quote
from crmevent.models.task import Task
from crmevent.models.users import Users
from crmevent.schemas.activity import ActivityRead
from crmevent.schemas.company import CompanyRead
from crmevent.schemas.contact import ContactRead
from crmevent.schemas.event import EventRead
from crmevent.schemas.history import HistoryRead
from crmevent.schemas.invoice import InvoiceRead
from crmevent.schemas.notification import NotificationRead
from crmevent.schemas.opportunity import OpportunityRead
from crmevent.schemas.quote import QuoteRead
from crmevent.schemas.task import TaskRead
from crmevent.schemas.users import UsersRead


STATUS_LABELS = {
    "new": "Nouvelle", "qualification": "Qualification", "proposal": "Proposition",
    "negotiation": "Négociation", "closed_won": "Gagnée", "closed_lost": "Perdue",
    "draft": "Brouillon", "planned": "Planifiée", "scheduled": "Planifié",
    "held": "Réalisé", "canceled": "Annulé", "locked": "Verrouillé",
    "sent": "Envoyé", "accepted": "Accepté", "rejected": "Refusé", "expired": "Expiré",
    "paid": "Payée", "overdue": "En retard", "todo": "À faire",
    "in_progress": "En cours", "done": "Terminé",
    "created": "Création", "updated": "Modification", "status_changed": "Changement de statut",
    "deleted": "Suppression", "email_sent": "Email envoyé",
    "active": "Actif", "inactive": "Inactif", "read": "Lue", "unread": "Non lue",
}


def history_date(model, entity):
    return (select(func.min(HistoryEntry.created_at)).where(
        HistoryEntry.entity_type == entity,
        HistoryEntry.entity_id == model.id,
        HistoryEntry.action == "created",
    ).correlate(model).scalar_subquery())


def event_day():
    # Existing events use DD-MM-YYYY, unlike the other ISO date strings.
    return (func.substr(Event.date, 7, 4) + "-" + func.substr(Event.date, 4, 2)
            + "-" + func.substr(Event.date, 1, 2))


@dataclass
class ListSpec:
    model: object
    schema: object
    columns: dict
    search: tuple
    period: object = None
    period_label: str = "Date de création"
    filters: dict = field(default_factory=dict)
    sort_extra: dict = field(default_factory=dict)
    status_values: tuple = ()
    status_label: str = "Statut"
    loads: tuple = ()

    @property
    def sortable(self):
        return {**{key: getattr(self.model, key) for key in self.columns}, **self.sort_extra}


def specs():
    company_name = lambda column: select(Company.name).where(Company.id == column).scalar_subquery()
    user_email = lambda column: select(Users.email).where(Users.id == column).scalar_subquery()
    opportunity_statuses = tuple(Opportunity.status.type.enums)
    invoice_line_vat = (select(func.sum(
        InvoiceLine.quantity * InvoiceLine.unit_price_excl_tax
        * (1 - InvoiceLine.discount_rate / 100) * InvoiceLine.vat_rate / 100
    )).where(InvoiceLine.invoice_id == Invoice.id).correlate(Invoice).scalar_subquery())
    vat = func.round(func.coalesce(invoice_line_vat, Invoice.total_amount * Invoice.vat_rate / 100), 2)
    total_ttc = Invoice.total_amount + vat
    return {
        "companies": ListSpec(Company, CompanyRead,
            {"id": "ID", "name": "Nom", "address": "Adresse", "city": "Ville", "created_at": "Création"},
            (Company.name, Company.address, Company.city), period=Company.created_at,
            filters={"company_id": Company.id}, status_values=opportunity_statuses,
            status_label="Statut de l’opportunité liée", loads=(Company.contacts,)),
        "contacts": ListSpec(Contact, ContactRead,
            {"id": "ID", "last_name": "Nom", "first_name": "Prénom", "phone_number": "Téléphone", "email": "Email"},
            (Contact.last_name, Contact.first_name, Contact.email, Contact.phone_number),
            period=history_date(Contact, "contact"), period_label="Création (historique disponible)",
            filters={"company_id": Contact.company_id}, status_values=opportunity_statuses,
            status_label="Statut de l’opportunité liée", loads=(Contact.company,)),
        "opportunities": ListSpec(Opportunity, OpportunityRead,
            {"id": "ID", "title": "Titre", "amount": "Montant", "status": "Statut", "created_at": "Création"},
            (Opportunity.title,), period=Opportunity.created_at,
            filters={"status": Opportunity.status, "company_id": Opportunity.company_id, "commercial_id": Opportunity.commercial_id},
            sort_extra={"company": company_name(Opportunity.company_id)},
            loads=(Opportunity.company, Opportunity.contact, Opportunity.commercial)),
        "activities": ListSpec(Activity, ActivityRead,
            {"id": "ID", "type": "Type", "content": "Contenu", "status": "Statut", "created_at": "Création", "scheduled_at": "Planification"},
            (Activity.content, Activity.email_subject, Activity.type), period=Activity.created_at,
            filters={"status": Activity.status, "company_id": Opportunity.company_id, "commercial_id": Opportunity.commercial_id}),
        "events": ListSpec(Event, EventRead,
            {"id": "ID", "title": "Titre", "type": "Type", "date": "Date", "duration": "Durée", "location": "Lieu", "status": "Statut"},
            (Event.title, Event.type, Event.location, Event.date), period=event_day(), period_label="Date de l’événement",
            filters={"status": Event.status, "company_id": Event.company_id, "commercial_id": Event.assigned_user_id},
            sort_extra={"date": event_day()}, loads=(Event.company, Event.opportunity, Event.contact, Event.assigned_user)),
        "quotes": ListSpec(Quote, QuoteRead,
            {"id": "ID", "number": "Numéro", "title": "Titre", "total_amount": "Total HT", "status": "Statut"},
            (Quote.number, Quote.title), period=history_date(Quote, "quote"), period_label="Création (historique disponible)",
            filters={"status": Quote.status, "company_id": Quote.company_id, "commercial_id": Quote.assigned_user_id},
            loads=(Quote.company, Quote.opportunity, Quote.assigned_user, Quote.event, Quote.lines)),
        "invoices": ListSpec(Invoice, InvoiceRead,
            {"id": "ID", "number": "Numéro", "title": "Titre", "total_amount": "Montant HT", "due_date": "Échéance", "status": "Statut"},
            (Invoice.number, Invoice.title), period=Invoice.issue_date, period_label="Date d’émission",
            filters={"status": Invoice.status, "company_id": Invoice.company_id, "commercial_id": Invoice.assigned_user_id},
            sort_extra={"total_incl_tax": total_ttc, "balance_remaining": case((total_ttc > Invoice.amount_paid, total_ttc - Invoice.amount_paid), else_=0)},
            loads=(Invoice.company, Invoice.quote, Invoice.opportunity, Invoice.assigned_user, Invoice.lines)),
        "tasks": ListSpec(Task, TaskRead,
            {"id": "ID", "title": "Titre", "priority": "Priorité", "status": "Statut", "due_at": "Échéance"},
            (Task.title, Task.description, Task.priority), period=Task.due_at, period_label="Échéance",
            filters={"status": Task.status, "company_id": func.coalesce(Opportunity.company_id, Event.company_id), "commercial_id": Task.assigned_user_id},
            sort_extra={"assigned_user": user_email(Task.assigned_user_id)},
            loads=(Task.assigned_user, Task.created_by, Task.opportunity, Task.event)),
        "users": ListSpec(Users, UsersRead,
            {"id": "ID", "email": "Email", "role": "Rôle", "is_active": "Compte actif"}, (Users.email, Users.role),
            filters={"status": Users.is_active}, status_values=("active", "inactive"), status_label="Compte"),
        "notifications": ListSpec(Notification, NotificationRead,
            {"id": "ID", "title": "Titre", "message": "Message", "type": "Type", "severity": "Priorité", "is_read": "Lue", "created_at": "Création"},
            (Notification.title, Notification.message), period=Notification.created_at,
            filters={"status": Notification.is_read}, status_values=("read", "unread"), status_label="Lecture"),
        "history": ListSpec(HistoryEntry, HistoryRead,
            {"id": "ID", "message": "Action", "entity_label": "Élément", "user_email": "Auteur", "created_at": "Date"},
            (HistoryEntry.message, HistoryEntry.entity_label, HistoryEntry.user_email), period=HistoryEntry.created_at,
            filters={"status": HistoryEntry.action, "company_id": HistoryEntry.company_id, "commercial_id": HistoryEntry.user_id},
            status_values=("created", "updated", "status_changed", "deleted", "email_sent"), status_label="Action"),
    }


SPECS = specs()


def get_spec(resource, user):
    spec = SPECS.get(resource)
    if spec is None:
        raise HTTPException(404, "Liste inconnue")
    if resource == "users" and user.role != "admin":
        raise HTTPException(403, "Accès administrateur requis")
    return spec


def metadata(resource, user):
    spec = get_spec(resource, user)
    statuses = spec.status_values
    if not statuses and "status" in spec.filters:
        statuses = tuple(getattr(spec.filters["status"].type, "enums", ()))
    return {
        "statuses": [{"value": value, "title": STATUS_LABELS.get(value, value)} for value in statuses],
        "status_label": spec.status_label,
        "company": "company_id" in spec.filters,
        "commercial": "commercial_id" in spec.filters or resource in {"companies", "contacts"},
        "period_label": spec.period_label if spec.period is not None else None,
        "sortable": list(spec.sortable),
        "sort_options": [{"value": key, "title": spec.columns.get(key, {"company": "Entreprise", "assigned_user": "Assigné à", "total_incl_tax": "Montant TTC", "balance_remaining": "Solde"}.get(key, key))} for key in spec.sortable],
    }


def build_query(db, resource, params, user):
    spec = get_spec(resource, user)
    model = spec.model
    query = db.query(model)
    if resource == "activities":
        query = query.join(Opportunity, Activity.opportunity_id == Opportunity.id)
    elif resource == "tasks":
        query = query.outerjoin(Opportunity, Task.opportunity_id == Opportunity.id).outerjoin(Event, Task.event_id == Event.id)
        if user.role not in {"admin", "manager"}:
            query = query.filter(Task.assigned_user_id == user.id)
    elif resource == "notifications":
        query = query.filter(Notification.user_id == user.id, Notification.archived_at.is_(None))

    if params.date_from and params.date_to and params.date_from > params.date_to:
        raise HTTPException(422, "La date de début doit précéder la date de fin")

    if params.q.strip():
        # Escape LIKE wildcards so that user input is a literal search.
        value = params.q.strip().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        query = query.filter(or_(*(cast(column, String).ilike(f"%{value}%", escape="\\") for column in spec.search)))

    if resource in {"companies", "contacts"}:
        conditions = []
        if params.status is not None:
            if params.status not in spec.status_values:
                raise HTTPException(422, "Statut invalide")
            conditions.append(Opportunity.status == params.status)
        if params.commercial_id is not None:
            conditions.append(Opportunity.commercial_id == params.commercial_id)
        if conditions:
            # EXISTS avoids duplicates and matches both filters on the same opportunity.
            query = query.filter(model.opportunities.any(and_(*conditions)))

    for key in ("status", "company_id", "commercial_id"):
        value = getattr(params, key)
        if value is None or (resource in {"companies", "contacts"} and key != "company_id"):
            continue
        column = spec.filters.get(key)
        if column is None:
            raise HTTPException(422, f"Filtre indisponible : {key}")
        if key == "status":
            allowed = spec.status_values or tuple(getattr(column.type, "enums", ()))
            if allowed and value not in allowed:
                raise HTTPException(422, "Statut invalide")
            if resource in {"users", "notifications"}:
                value = value in {"active", "read"}
        query = query.filter(column == value)

    for key in ("opportunity_id", "contact_id", "event_id", "quote_id", "invoice_id"):
        value = getattr(params, key)
        if value is not None:
            column = getattr(model, key, None)
            if column is None:
                raise HTTPException(422, f"Filtre indisponible : {key}")
            query = query.filter(column == value)

    if params.date_from or params.date_to:
        if spec.period is None:
            raise HTTPException(422, "Cette liste ne possède pas de date")
        # All bounds are inclusive calendar dates, using the stored calendar day.
        day = func.substr(cast(spec.period, String), 1, 10)
        if params.date_from:
            query = query.filter(day >= params.date_from.isoformat())
        if params.date_to:
            query = query.filter(day <= params.date_to.isoformat())

    column = spec.sortable.get(params.sort_by)
    if column is None:
        raise HTTPException(422, "Colonne de tri invalide")
    direction = column.asc() if params.sort_order == "asc" else column.desc()
    query = query.order_by(direction, model.id.asc())
    return spec, query


def list_page(db, resource, params, user):
    spec, query = build_query(db, resource, params, user)
    total = query.order_by(None).count()
    items = query.options(*(selectinload(relation) for relation in spec.loads)).offset(
        (params.page - 1) * params.page_size
    ).limit(params.page_size).all()
    return {
        "items": [spec.schema.model_validate(item).model_dump(mode="json") for item in items],
        "total": total, "page": params.page, "page_size": params.page_size,
        "pages": ceil(total / params.page_size),
    }


def safe_cell(value):
    if value is None:
        return ""
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if isinstance(value, str) and (value.lstrip().startswith(("=", "+", "-", "@")) or value.startswith(("\t", "\r", "\n"))):
        return "'" + value
    return value


def export_list(db, resource, params, user, export_format):
    spec, query = build_query(db, resource, params, user)
    # Fetch explicit public fields only; never export password hashes or internal tokens.
    columns = dict(spec.columns)
    extra_labels = {"company": "Entreprise", "assigned_user": "Assigné à", "total_incl_tax": "Montant TTC", "balance_remaining": "Solde"}
    for key in spec.sort_extra:
        if key not in columns:
            columns[key] = extra_labels[key]
    for key, title in (("company_id", "Entreprise (ID)"), ("commercial_id", "Commercial (ID)"), ("assigned_user_id", "Assigné à (ID)")):
        if hasattr(spec.model, key):
            columns[key] = title
    expressions = [spec.sortable[key] if key in spec.sort_extra and key not in spec.columns else getattr(spec.model, key) for key in columns]
    rows = query.with_entities(*expressions).yield_per(500)
    if export_format == "csv":
        output = StringIO(newline="")
        writer = csv.writer(output, delimiter=";")
        writer.writerow(columns.values())
        for row in rows:
            writer.writerow([safe_cell(value) for value in row])
        content = output.getvalue().encode("utf-8-sig")
        media_type = "text/csv; charset=utf-8"
    else:
        workbook = Workbook(write_only=True)
        sheet = workbook.create_sheet("Export")
        sheet.append(list(columns.values()))
        for row in rows:
            sheet.append([safe_cell(value) for value in row])
        output = BytesIO()
        workbook.save(output)
        content = output.getvalue()
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return Response(content, media_type=media_type, headers={
        "Content-Disposition": f'attachment; filename="{resource}.{export_format}"',
    })

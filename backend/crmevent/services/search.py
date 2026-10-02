from sqlalchemy import or_
from sqlalchemy.orm import Session

from crmevent.models.company import Company
from crmevent.models.contact import Contact
from crmevent.models.event import Event
from crmevent.models.invoice import Invoice
from crmevent.models.opportunity import Opportunity
from crmevent.models.quote import Quote
from crmevent.schemas.search import GlobalSearchItem


def global_search(db: Session, query: str, limit: int = 5) -> list[GlobalSearchItem]:
    pattern = f"%{query.strip()}%"
    results: list[GlobalSearchItem] = []

    companies = (
        db.query(Company)
        .filter(or_(Company.name.ilike(pattern), Company.city.ilike(pattern), Company.email.ilike(pattern)))
        .order_by(Company.name.asc())
        .limit(limit)
        .all()
    )
    results.extend(
        GlobalSearchItem(
            id=item.id,
            type="company",
            title=item.name,
            subtitle=" · ".join(part for part in [item.city, item.email] if part) or None,
            url=f"/companies/{item.id}",
        )
        for item in companies
    )

    contacts = (
        db.query(Contact)
        .filter(
            or_(
                Contact.first_name.ilike(pattern),
                Contact.last_name.ilike(pattern),
                Contact.email.ilike(pattern),
                Contact.phone_number.ilike(pattern),
            )
        )
        .order_by(Contact.last_name.asc(), Contact.first_name.asc())
        .limit(limit)
        .all()
    )
    results.extend(
        GlobalSearchItem(
            id=item.id,
            type="contact",
            title=f"{item.first_name} {item.last_name}",
            subtitle=" · ".join(part for part in [item.email, item.company.name if item.company else None] if part),
            url=f"/contacts/{item.id}",
        )
        for item in contacts
    )

    opportunities = (
        db.query(Opportunity)
        .filter(Opportunity.title.ilike(pattern))
        .order_by(Opportunity.id.desc())
        .limit(limit)
        .all()
    )
    results.extend(
        GlobalSearchItem(
            id=item.id,
            type="opportunity",
            title=item.title,
            subtitle=item.company.name if item.company else None,
            url=f"/opportunities/{item.id}",
        )
        for item in opportunities
    )

    events = (
        db.query(Event)
        .filter(or_(Event.title.ilike(pattern), Event.number.ilike(pattern), Event.location.ilike(pattern)))
        .order_by(Event.id.desc())
        .limit(limit)
        .all()
    )
    results.extend(
        GlobalSearchItem(
            id=item.id,
            type="event",
            title=item.title,
            subtitle=" · ".join(part for part in [item.number, item.date] if part),
            url=f"/events/{item.id}",
        )
        for item in events
    )

    quotes = (
        db.query(Quote)
        .filter(or_(Quote.number.ilike(pattern), Quote.title.ilike(pattern)))
        .order_by(Quote.id.desc())
        .limit(limit)
        .all()
    )
    results.extend(
        GlobalSearchItem(
            id=item.id,
            type="quote",
            title=item.number,
            subtitle=" · ".join(part for part in [item.title, item.company.name if item.company else None] if part),
            url=f"/quotes/{item.id}",
        )
        for item in quotes
    )

    invoices = (
        db.query(Invoice)
        .filter(or_(Invoice.number.ilike(pattern), Invoice.title.ilike(pattern)))
        .order_by(Invoice.id.desc())
        .limit(limit)
        .all()
    )
    results.extend(
        GlobalSearchItem(
            id=item.id,
            type="invoice",
            title=item.number,
            subtitle=" · ".join(part for part in [item.title, item.company.name if item.company else None] if part),
            url=f"/invoices/{item.id}",
        )
        for item in invoices
    )

    return results


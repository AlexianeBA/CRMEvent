from datetime import datetime, timezone

from sqlalchemy.orm import Session

from crmevent.models.history import HistoryEntry


STATUS_LABELS = {
    "new": "nouvelle", "qualification": "qualification", "proposal": "proposition",
    "negotiation": "négociation", "closed_won": "gagnée", "closed_lost": "perdue",
    "draft": "brouillon", "scheduled": "planifié", "held": "réalisé",
    "sent": "envoyé", "accepted": "accepté", "rejected": "refusé",
    "expired": "expiré", "paid": "payé", "overdue": "en retard",
    "planned": "planifiée", "done": "terminée", "canceled": "annulé", "locked": "clôturé",
}


def status_label(status) -> str:
    value = getattr(status, "value", status)
    return STATUS_LABELS.get(value, value)


def record_history(db: Session, user, action: str, entity_type: str, entity_id: int,
                   entity_label: str, message: str, **context):
    entry = HistoryEntry(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        entity_label=entity_label,
        message=message,
        user_id=user.id,
        user_email=user.email,
        created_at=datetime.now(timezone.utc).isoformat(),
        **context,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_history(db: Session, limit: int = 100, **filters):
    query = db.query(HistoryEntry)
    for field, value in filters.items():
        if value is not None:
            query = query.filter(getattr(HistoryEntry, field) == value)
    return query.order_by(HistoryEntry.created_at.desc()).limit(limit).all()

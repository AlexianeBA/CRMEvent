from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from crmevent.models.document_sequence import DocumentSequence


PREFIXES = {"quote": "DEV", "invoice": "FAC", "event": "EVT"}


def next_document_number(db: Session, document_type: str) -> str:
    year = datetime.now(timezone.utc).year
    sequence = db.query(DocumentSequence).filter(
        DocumentSequence.document_type == document_type,
        DocumentSequence.year == year,
    ).with_for_update().first()
    if not sequence:
        try:
            with db.begin_nested():
                sequence = DocumentSequence(document_type=document_type, year=year, next_number=1, prefix=PREFIXES[document_type])
                db.add(sequence)
                db.flush()
        except IntegrityError:
            sequence = db.query(DocumentSequence).filter(
                DocumentSequence.document_type == document_type,
                DocumentSequence.year == year,
            ).with_for_update().one()
    value = sequence.next_number
    sequence.next_number += 1
    db.flush()
    return f"{sequence.prefix}-{year}-{value:04d}"

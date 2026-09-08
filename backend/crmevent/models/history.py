from sqlalchemy import Column, Integer, String

from crmevent.db.base import Base


class HistoryEntry(Base):
    __tablename__ = "history_entries"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)
    entity_type = Column(String, nullable=False, index=True)
    entity_id = Column(Integer, nullable=False, index=True)
    entity_label = Column(String, nullable=False)
    message = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    user_email = Column(String, nullable=False)
    company_id = Column(Integer, nullable=True, index=True)
    contact_id = Column(Integer, nullable=True, index=True)
    opportunity_id = Column(Integer, nullable=True, index=True)
    event_id = Column(Integer, nullable=True, index=True)
    quote_id = Column(Integer, nullable=True, index=True)
    invoice_id = Column(Integer, nullable=True, index=True)
    created_at = Column(String, nullable=False, index=True)

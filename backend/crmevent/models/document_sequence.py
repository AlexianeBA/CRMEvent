from sqlalchemy import Column, Integer, String, UniqueConstraint
from crmevent.db.base import Base


class DocumentSequence(Base):
    __tablename__ = "document_sequences"
    __table_args__ = (UniqueConstraint("document_type", "year", name="uq_document_sequence_type_year"),)

    id = Column(Integer, primary_key=True)
    document_type = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)
    next_number = Column(Integer, nullable=False, default=1)
    prefix = Column(String(10), nullable=False)

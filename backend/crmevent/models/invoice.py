from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Numeric, DateTime
from sqlalchemy.orm import relationship
from crmevent.db.base import Base
from datetime import datetime

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False)
    title = Column(String, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum("draft", "sent", "paid", "overdue", "canceled", "locked", name="invoice_status"), nullable=False)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=False)
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    company = relationship("Company", back_populates="invoices")
    quote = relationship("Quote", back_populates="invoices")
    opportunity = relationship("Opportunity", back_populates="invoices")
    assigned_user = relationship("Users", back_populates="assigned_invoices")

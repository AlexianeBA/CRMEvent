from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from crmevent.db.base import Base

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    status = Column(Enum("new", "qualification", "proposal", "negotiation", "closed_won", "closed_lost", name="opportunity_status"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)
    commercial_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    contact = relationship("Contact", back_populates="opportunities")
    company = relationship("Company", back_populates="opportunities")
    activities = relationship("Activity", back_populates="opportunity")
    quotes = relationship("Quote", back_populates="opportunity")
    events = relationship("Event", back_populates="opportunity")
    commercial = relationship("Users", back_populates="opportunities")
    invoices = relationship("Invoice", back_populates="opportunity")
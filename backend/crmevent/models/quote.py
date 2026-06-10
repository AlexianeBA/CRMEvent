from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from crmevent.db.base import Base

class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum("draft", "sent", "accepted", "rejected", name="quote_status"), nullable=False) 
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=False)
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)

    opportunity = relationship("Opportunity", back_populates="quotes")
    company = relationship("Company", back_populates="quotes")
    event = relationship("Event", back_populates="quotes")
    assigned_user = relationship("Users", back_populates="assigned_quotes")
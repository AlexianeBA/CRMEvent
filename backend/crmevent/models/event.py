from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from crmevent.db.base import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(Enum("webinar", "workshop", "conference", name="event_type"), nullable=False) 
    date = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    description = Column(String, nullable=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=False)
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)

    opportunity = relationship("Opportunity", back_populates="events")
    contact = relationship("Contact", back_populates="events")
    company = relationship("Company", back_populates="events")
    quotes = relationship("Quote", back_populates="event")
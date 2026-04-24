from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from crmevent.db.base import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)

    company = relationship("Company", back_populates="contacts")
    opportunities = relationship("Opportunity", back_populates="contact")
    events = relationship("Event", back_populates="contact")
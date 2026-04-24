from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from crmevent.db.base import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)

    contacts = relationship("Contact", back_populates="company")
    opportunities = relationship("Opportunity", back_populates="company")
    events = relationship("Event", back_populates="company")
    quotes = relationship("Quote", back_populates="company")

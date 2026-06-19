from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from crmevent.db.base import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Integer, default=1)
    
    
    opportunities = relationship(
        "Opportunity",
        back_populates="commercial"
    )

    assigned_events = relationship(
        "Event",
        back_populates="assigned_user"
    )

    assigned_quotes = relationship(
        "Quote",
        back_populates="assigned_user"
    )
    assigned_invoices = relationship(
        "Invoice",
        back_populates="assigned_user"
    )
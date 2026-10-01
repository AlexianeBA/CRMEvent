from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from crmevent.db.base import Base

class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum("draft", "sent", "accepted", "rejected", "expired", "locked", name="quote_status"), nullable=False, default="draft")
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=False)
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)

    opportunity = relationship("Opportunity", back_populates="quotes")
    company = relationship("Company", back_populates="quotes")
    event = relationship("Event", back_populates="quotes")
    assigned_user = relationship("Users", back_populates="assigned_quotes")
    invoices = relationship("Invoice", back_populates="quote")
    lines = relationship("QuoteLine", back_populates="quote", cascade="all, delete-orphan", order_by="QuoteLine.position")


class QuoteLine(Base):
    __tablename__ = "quote_lines"
    id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey("quotes.id", ondelete="CASCADE"), nullable=False, index=True)
    description = Column(String, nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(30), nullable=False, default="unité")
    unit_price_excl_tax = Column(Numeric(10, 2), nullable=False)
    vat_rate = Column(Numeric(5, 2), nullable=False, default=20)
    discount_rate = Column(Numeric(5, 2), nullable=False, default=0)
    position = Column(Integer, nullable=False, default=0)
    quote = relationship("Quote", back_populates="lines")

    @property
    def total_excl_tax(self):
        return self.gross_total_excl_tax - self.discount_amount

    @property
    def gross_total_excl_tax(self):
        return self.quantity * self.unit_price_excl_tax

    @property
    def discount_amount(self):
        return self.gross_total_excl_tax * self.discount_rate / 100

    @property
    def vat_amount(self):
        return self.total_excl_tax * self.vat_rate / 100

    @property
    def total_incl_tax(self):
        return self.total_excl_tax + self.vat_amount

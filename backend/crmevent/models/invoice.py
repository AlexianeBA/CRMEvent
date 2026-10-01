from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Numeric, DateTime, Text
from sqlalchemy.orm import relationship
from crmevent.db.base import Base
from datetime import datetime
from decimal import Decimal

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False)
    title = Column(String, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    vat_rate = Column(Numeric(5, 2), nullable=False, default=20)
    status = Column(Enum("draft", "sent", "paid", "overdue", "canceled", "locked", name="invoice_status"), nullable=False)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=False)
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    issue_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    payment_terms = Column(Text, nullable=False, default="Paiement à 30 jours")
    amount_paid = Column(Numeric(10, 2), nullable=False, default=0)

    company = relationship("Company", back_populates="invoices")
    quote = relationship("Quote", back_populates="invoices")
    opportunity = relationship("Opportunity", back_populates="invoices")
    assigned_user = relationship("Users", back_populates="assigned_invoices")
    payments = relationship("InvoicePayment", back_populates="invoice", cascade="all, delete-orphan", order_by="InvoicePayment.paid_at.desc()")
    lines = relationship("InvoiceLine", back_populates="invoice", cascade="all, delete-orphan", order_by="InvoiceLine.position")

    @property
    def balance_remaining(self):
        return max(self.total_incl_tax - self.amount_paid, 0)

    @property
    def vat_amount(self):
        if self.lines:
            return sum((line.vat_amount for line in self.lines), Decimal("0.00")).quantize(Decimal("0.01"))
        return (self.total_amount * self.vat_rate / 100).quantize(Decimal("0.01"))

    @property
    def total_incl_tax(self):
        return self.total_amount + self.vat_amount


class InvoicePayment(Base):
    __tablename__ = "invoice_payments"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    paid_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    payment_method = Column(String(50), nullable=False)
    reference = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    invoice = relationship("Invoice", back_populates="payments")


class InvoiceLine(Base):
    __tablename__ = "invoice_lines"
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    description = Column(String, nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(30), nullable=False, default="unité")
    unit_price_excl_tax = Column(Numeric(10, 2), nullable=False)
    vat_rate = Column(Numeric(5, 2), nullable=False, default=20)
    discount_rate = Column(Numeric(5, 2), nullable=False, default=0)
    position = Column(Integer, nullable=False, default=0)
    invoice = relationship("Invoice", back_populates="lines")

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

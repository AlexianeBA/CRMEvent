from datetime import datetime

from pydantic import BaseModel, Field
import enum

class InvoiceStatus(str, enum.Enum):
    draft = "draft"
    sent = "sent"
    paid = "paid"
    overdue = "overdue"
    canceled = "canceled"
    locked = "locked"

class InvoiceBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    total_amount: float = Field(..., gt=0)
    quote_id: int = Field(..., gt=0)
    company_id: int = Field(..., gt=0)
    opportunity_id: int = Field(..., gt=0)
    assigned_user_id: int = Field(..., gt=0)
    status: InvoiceStatus = InvoiceStatus.draft

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceCompanyRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class InvoiceQuoteRead(BaseModel):
    id: int
    number: str
    title: str

    class Config:
        from_attributes = True

class InvoiceOpportunityRead(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True

class InvoiceUserRead(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class InvoiceRead(InvoiceBase):
    id: int
    number: str
    title: str
    total_amount: float
    status: InvoiceStatus
    company_id: int
    quote_id: int | None
    opportunity_id: int
    assigned_user_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    company: InvoiceCompanyRead
    quote: InvoiceQuoteRead
    opportunity: InvoiceOpportunityRead
    assigned_user: InvoiceUserRead

    class Config:
        from_attributes = True

class InvoiceUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    total_amount: float | None = Field(default=None, gt=0)
    status: InvoiceStatus | None = None
    

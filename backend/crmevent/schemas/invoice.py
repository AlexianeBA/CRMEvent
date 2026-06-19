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

    class Config:
        from_attributes = True

class InvoiceUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    total_amount: float | None = Field(default=None, gt=0)
    status: InvoiceStatus | None = None
    


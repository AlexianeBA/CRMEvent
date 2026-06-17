from pydantic import BaseModel, Field
import enum

class InvoiceStatus(str, enum.Enum):
    draft = "draft"
    sent = "sent"
    paid = "paid"
    overdue = "overdue"

class InvoiceBase(BaseModel):
    total_amount: float = Field(..., gt=0)
    opportunity_id: int = Field(..., gt=0)

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
    total_amount: float | None = Field(default=None, gt=0)
    status: InvoiceStatus | None = None
    opportunity_id: int | None = Field(default=None, gt=0)


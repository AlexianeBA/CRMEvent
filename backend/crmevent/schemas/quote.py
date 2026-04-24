from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
import enum


class QuoteStatus(str, enum.Enum):
    draft = "draft"
    sent = "sent"
    accepted = "accepted"
    rejected = "rejected"

class QuoteBase(BaseModel):
    number: str
    title: str
    total_amount: Decimal = Field(..., gt=0)
    status: QuoteStatus
    company_id: int
    opportunity_id: int
    assigned_user_id: int
    event_id: Optional[int] = None

class QuoteCreate(QuoteBase):
    pass

class QuoteRead(QuoteBase):
    id: int

    class Config:
        from_attributes = True
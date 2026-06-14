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
    number: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=255)
    total_amount: Decimal = Field(..., gt=0)
    status: QuoteStatus = Field(..., description="Status of the quote")
    company_id: int = Field(..., gt=0)
    opportunity_id: int = Field(..., gt=0)
    assigned_user_id: int = Field(..., gt=0)
    event_id: Optional[int] = Field(default=None, gt=0) 

class QuoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    total_amount: Optional[Decimal] = Field(None, gt=0)
    status: Optional[QuoteStatus] = Field(None, description="Status of the quote")
    company_id: Optional[int] = Field(None, gt=0)
    opportunity_id: Optional[int] = Field(None, gt=0)
    assigned_user_id: Optional[int] = Field(None, gt=0)
    event_id: Optional[int] = Field(default=None, gt=0)
class QuoteCreate(QuoteBase):
    pass

class QuoteRead(QuoteBase):
    id: int

    class Config:
        from_attributes = True
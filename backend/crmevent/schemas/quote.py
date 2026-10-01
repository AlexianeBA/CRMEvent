from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
import enum


class QuoteStatus(str, enum.Enum):
    draft = "draft"
    sent = "sent"
    accepted = "accepted"
    rejected = "rejected"
    expired = "expired"
    locked = "locked"


class QuoteLineBase(BaseModel):
    description: str = Field(..., min_length=1, max_length=500)
    quantity: Decimal = Field(..., gt=0)
    unit: str = Field(default="unité", min_length=1, max_length=30)
    unit_price_excl_tax: Decimal = Field(..., ge=0)
    vat_rate: Decimal = Field(default=20, ge=0, le=100)
    discount_rate: Decimal = Field(default=0, ge=0, le=100)
    position: int = Field(default=0, ge=0)


class QuoteLineRead(QuoteLineBase):
    id: int
    total_excl_tax: Decimal
    gross_total_excl_tax: Decimal
    discount_amount: Decimal
    vat_amount: Decimal
    total_incl_tax: Decimal
    class Config:
        from_attributes = True

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
    status: Optional[QuoteStatus] = Field(None, description="Status of the quote")
    lines: list[QuoteLineBase] | None = None
    
class QuoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    total_amount: Decimal | None = Field(default=None, gt=0)
    company_id: int = Field(..., gt=0)
    opportunity_id: int = Field(..., gt=0)
    assigned_user_id: int = Field(..., gt=0)
    event_id: Optional[int] = Field(default=None, gt=0)
    lines: list[QuoteLineBase] = Field(..., min_length=1)

class QuoteCompanyRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class QuoteOpportunityRead(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True

class QuoteUserRead(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class QuoteEventRead(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True

class QuoteRead(QuoteBase):
    id: int
    company: QuoteCompanyRead
    opportunity: QuoteOpportunityRead
    assigned_user: QuoteUserRead
    event: QuoteEventRead | None = None
    lines: list[QuoteLineRead] = Field(default_factory=list)

    class Config:
        from_attributes = True

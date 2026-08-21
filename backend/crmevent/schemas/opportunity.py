from decimal import Decimal

from pydantic import BaseModel, Field, field_validator
from enum import Enum

class OpportunityStatus(str, Enum):
    new = "new"
    qualification = "qualification"
    proposal = "proposal"
    negotiation = "negotiation"
    closed_won = "closed_won"
    closed_lost = "closed_lost"


class OpportunityBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    status: OpportunityStatus
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    company_id: int = Field(..., gt=0)
    contact_id: int = Field(..., gt=0)
    commercial_id: int = Field(..., gt=0)

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v
    
class OpportunityCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    company_id: int = Field(..., gt=0)
    contact_id: int = Field(..., gt=0)
    commercial_id: int = Field(..., gt=0)

class OpportunityUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    amount: Decimal | None = Field(default=None, gt=0, decimal_places=2)

class OpportunityCompanyRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class OpportunityContactRead(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class OpportunityCommercialRead(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class OpportunityRead(OpportunityBase):
    id: int
    created_at: str
    updated_at: str
    company: OpportunityCompanyRead
    contact: OpportunityContactRead
    commercial: OpportunityCommercialRead

    class Config:
        from_attributes = True

class OpportunityStatusUpdate(BaseModel):
    status: OpportunityStatus

from pydantic import BaseModel
from enum import Enum

class OpportunityStatus(str, Enum):
    new = "new"
    qualification = "qualification"
    proposal = "proposal"
    negotiation = "negotiation"
    closed_won = "closed_won"
    closed_lost = "closed_lost"


class OpportunityBase(BaseModel):
    title: str
    status: OpportunityStatus
    amount: int
    company_id: int
    contact_id: int
    commercial_id: int
    
class OpportunityCreate(OpportunityBase):
    pass

class OpportunityRead(OpportunityBase):
    id: int

    class Config:
        from_attributes = True

class OpportunityStatusUpdate(BaseModel):
    status: OpportunityStatus
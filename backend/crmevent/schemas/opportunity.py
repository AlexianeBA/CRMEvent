from pydantic import BaseModel

class OpportunityBase(BaseModel):
    title: str
    status: str
    amount: int
    company_id: int
    contact_id: int
    
class OpportunityCreate(OpportunityBase):
    pass

class OpportunityRead(OpportunityBase):
    id: int

    class Config:
        from_attributes = True


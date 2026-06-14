from pydantic import BaseModel, Field

class EventBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    date: str = Field(..., pattern=r"^\d{2}-\d{2}-\d{4}$")  
    company_id: int = Field(..., gt=0)
    opportunity_id: int = Field(..., gt=0)
    assigned_user_id: int = Field(..., gt=0)
    type: str = Field(..., min_length=1, max_length=100)
    duration: int = Field(..., gt=0)
    location: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)

class EventCreate(EventBase):
    pass

class EventRead(EventBase):
    id: int

    class Config:
        from_attributes = True

        
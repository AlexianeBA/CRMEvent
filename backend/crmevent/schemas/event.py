from pydantic import BaseModel

class EventBase(BaseModel):
    name: str
    date: str
    company_id: int
    opportunity_id: int
    assigned_user_id: int
    type: str
    duration: int
    location: str
    description: str | None = None

class EventCreate(EventBase):
    pass

class EventRead(EventBase):
    id: int

    class Config:
        from_attributes = True

        
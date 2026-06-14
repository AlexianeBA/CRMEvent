from pydantic import BaseModel, Field
from enum import Enum

class EventType(str, Enum):
    webinar = "webinar"
    workshop = "workshop"
    conference = "conference"
class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    date: str = Field(..., pattern=r"^\d{2}-\d{2}-\d{4}$")  
    company_id: int = Field(..., gt=0)
    opportunity_id: int = Field(..., gt=0)
    assigned_user_id: int = Field(..., gt=0)
    type: EventType = Field(..., description="Type of the event")
    duration: int = Field(..., gt=0)
    location: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    contact_id: int | None = Field(default=None, gt=0)

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: str | None = None
    date: str | None = None
    company_id: int | None = None
    opportunity_id: int | None = None
    assigned_user_id: int | None = None
    type: EventType | None = None
    duration: int | None = None
    location: str | None = None
    description: str | None = None
    contact_id: int | None = None

class EventRead(EventBase):
    id: int

    class Config:
        from_attributes = True

        
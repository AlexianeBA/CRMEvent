from pydantic import BaseModel, Field
from enum import Enum

class EventType(str, Enum):
    webinar = "webinar"
    workshop = "workshop"
    conference = "conference"

class EventStatus(str, Enum):
    draft = "draft"
    scheduled = "scheduled"
    held = "held"
    canceled = "canceled"
    locked = "locked"
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
    title: str | None = Field(default=None, min_length=1, max_length=255)
    date: str | None = Field(default=None, pattern=r"^\d{2}-\d{2}-\d{4}$")
    type: EventType | None = None
    duration: int | None = Field(default=None, gt=0)
    location: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    company_id: int | None = Field(default=None, gt=0)
    opportunity_id: int | None = Field(default=None, gt=0)
    assigned_user_id: int | None = Field(default=None, gt=0)
    contact_id: int | None = Field(default=None, gt=0)

class EventCompanyRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
class EventOpportunityRead(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True

class EventContactRead(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class EventUserRead(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class EventRead(EventBase):
    id: int
    status: EventStatus
    company: EventCompanyRead
    opportunity: EventOpportunityRead
    contact: EventContactRead | None = None
    assigned_user: EventUserRead

    class Config:
        from_attributes = True

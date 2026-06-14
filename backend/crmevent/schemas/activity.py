from pydantic import BaseModel, Field
from enum import Enum


class ActivityType(str, Enum):
    note = "note"
    call = "call"
    email = "email"
    meeting = "meeting"

    
class ActivityBase(BaseModel):
    type: ActivityType
    content: str = Field(..., min_length=1, max_length=1000)
    opportunity_id: int = Field(..., gt=0)

class ActivityUpdate(BaseModel):
    type: ActivityType | None = None
    content: str | None = Field(default=None, min_length=1, max_length=1000)
    opportunity_id: int | None = Field(default=None, gt=0)
class ActivityCreate(ActivityBase):
    pass

class ActivityRead(ActivityBase):
    id: int

    class Config:
        from_attributes = True


from pydantic import BaseModel, Field
from enum import Enum


class ActivityType(str, Enum):
    note = "note"
    call = "call"
    email = "email"
    meeting = "meeting"


class ActivityStatus(str, Enum):
    draft = "draft"
    planned = "planned"
    done = "done"
    canceled = "canceled"


class ActivityBase(BaseModel):
    type: ActivityType
    content: str = Field(..., min_length=1, max_length=1000)
    opportunity_id: int = Field(..., gt=0)
    status: ActivityStatus = ActivityStatus.draft

class ActivityUpdate(BaseModel):
    type: ActivityType | None = None
    content: str | None = Field(default=None, min_length=1, max_length=1000)
    status: ActivityStatus | None = None

class ActivityCreate(ActivityBase):
    pass

class ActivityRead(ActivityBase):
    id: int

    class Config:
        from_attributes = True


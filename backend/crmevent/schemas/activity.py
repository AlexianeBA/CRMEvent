from datetime import datetime

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

class ActivityUpdate(BaseModel):
    type: ActivityType | None = None
    content: str | None = Field(default=None, min_length=1, max_length=1000)
    scheduled_at: datetime | None = None

class ActivityCreate(ActivityBase):
    pass

class ActivityRead(ActivityBase):
    id: int
    status: ActivityStatus
    created_at: str
    updated_at: str
    scheduled_at: datetime | None = None

    class Config:
        from_attributes = True

from datetime import datetime

from pydantic import BaseModel, Field, model_validator
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
    email_subject: str | None = Field(default=None, min_length=1, max_length=255)

class ActivityUpdate(BaseModel):
    type: ActivityType | None = None
    content: str | None = Field(default=None, min_length=1, max_length=1000)
    scheduled_at: datetime | None = None
    email_subject: str | None = Field(default=None, min_length=1, max_length=255)

class ActivityCreate(ActivityBase):
    @model_validator(mode="after")
    def validate_email_subject(self):
        if self.type == ActivityType.email and not self.email_subject:
            raise ValueError("L'objet est obligatoire pour une activité email")
        if self.email_subject and any(char in self.email_subject for char in ("\r", "\n")):
            raise ValueError("L'objet de l'email ne peut pas contenir de retour à la ligne")
        return self

class ActivityRead(ActivityBase):
    id: int
    status: ActivityStatus
    created_at: str
    updated_at: str
    scheduled_at: datetime | None = None

    class Config:
        from_attributes = True

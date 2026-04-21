from pydantic import BaseModel
from enum import Enum


class ActivityType(str, Enum):
    note = "note"
    call = "call"
    email = "email"

    
class ActivityBase(BaseModel):
    type: ActivityType
    content: str
    opportunity_id: int

class ActivityCreate(ActivityBase):
    pass

class ActivityRead(ActivityBase):
    id: int

    class Config:
        from_attributes = True


from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, model_validator


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    canceled = "canceled"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    priority: TaskPriority = TaskPriority.medium
    due_at: datetime
    assigned_user_id: int = Field(..., gt=0)
    opportunity_id: int | None = Field(default=None, gt=0)
    event_id: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def require_context(self):
        if self.opportunity_id is None and self.event_id is None:
            raise ValueError("La tâche doit être liée à une opportunité ou à un événement")
        value = self.due_at
        now = datetime.now(value.tzinfo) if value.tzinfo else datetime.now()
        if value <= now:
            raise ValueError("L'échéance doit être dans le futur")
        return self


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_at: datetime | None = None
    assigned_user_id: int | None = Field(default=None, gt=0)
    opportunity_id: int | None = Field(default=None, gt=0)
    event_id: int | None = Field(default=None, gt=0)


class TaskUserRead(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


class TaskRelationRead(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_at: datetime
    assigned_user_id: int
    created_by_id: int
    opportunity_id: int | None
    event_id: int | None
    created_at: datetime
    updated_at: datetime
    assigned_user: TaskUserRead
    created_by: TaskUserRead
    opportunity: TaskRelationRead | None
    event: TaskRelationRead | None

    class Config:
        from_attributes = True

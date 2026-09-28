from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class NotificationType(str, Enum):
    event_upcoming = "event_upcoming"
    opportunity_inactive = "opportunity_inactive"
    quote_unanswered = "quote_unanswered"
    invoice_due = "invoice_due"
    invoice_overdue = "invoice_overdue"
    task_assigned = "task_assigned"
    task_due = "task_due"


class NotificationSeverity(str, Enum):
    info = "info"
    warning = "warning"
    error = "error"


class NotificationCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    type: NotificationType
    severity: NotificationSeverity = NotificationSeverity.info
    target_url: str | None = Field(default=None, max_length=500)
    deduplication_key: str = Field(..., min_length=1, max_length=255)
    scheduled_at: datetime | None = None


class NotificationRead(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: NotificationType
    severity: NotificationSeverity
    target_url: str | None
    deduplication_key: str
    is_read: bool
    read_at: datetime | None
    scheduled_at: datetime | None
    archived_at: datetime | None
    emailed_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationCount(BaseModel):
    unread_count: int

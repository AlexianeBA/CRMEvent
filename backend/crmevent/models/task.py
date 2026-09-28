from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from crmevent.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum("todo", "in_progress", "done", "canceled", name="task_status"), nullable=False, default="todo")
    priority = Column(Enum("low", "medium", "high", name="task_priority"), nullable=False, default="medium")
    due_at = Column(DateTime(timezone=True), nullable=False, index=True)
    assigned_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id", ondelete="CASCADE"), nullable=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    assigned_user = relationship("Users", foreign_keys=[assigned_user_id], back_populates="assigned_tasks")
    created_by = relationship("Users", foreign_keys=[created_by_id], back_populates="created_tasks")
    opportunity = relationship("Opportunity", back_populates="tasks")
    event = relationship("Event", back_populates="tasks")

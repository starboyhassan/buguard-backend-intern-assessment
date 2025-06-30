from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum #enumerated types for fixed choices (TaskStatus, TaskPriority)
from datetime import datetime, timezone


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.pending)  # task status = pending by DEFAULT
    priority: TaskPriority = Field(default=TaskPriority.medium) # task priority = medium by DEFAULT
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) # this method 'datetime.now(timezone.utc)' will work with all python versions (even 3.11+)
    updated_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = Field(default=None, max_length=100)
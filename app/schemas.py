from datetime import datetime, timezone
from pydantic import BaseModel, field_validator # or pydantic v2 @validator is deprecated
from typing import Optional, List
from .models import TaskStatus, TaskPriority

# enusure you inhiret BaseModel for pydantic for Data Validation and Serialization
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.pending # task status = pending by DEFAULT 
    priority: Optional[TaskPriority] = TaskPriority.medium # task priority = medium by DEFAULT
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = None

#Title validation:
   # 1- Cannot be empty or whitespace only
   # 2- Must be trimmed of leading/trailing spaces
    @field_validator("title") # make custom validation 
    @classmethod
    def title_validator(cls, titleValue: str):
        titleValue = titleValue.strip()
        if not titleValue:
            raise ValueError('Title cannot be Empty or Whitespaces only')
        return titleValue

#Due date validation: must be in the future (if provided) we will make sure its after the current utc time
    @field_validator("due_date")
    @classmethod
    def due_date_validator(cls, ddate: Optional[datetime]):
        if ddate and ddate <= datetime.now(timezone.utc): # this method 'datetime.now(timezone.utc)' will work with all python versions (even 3.11+)
            raise ValueError('Due date must be in the future not Before or Equal the current datetime')
        return ddate

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


###########BULK OPERATIONS

class BulkTaskUpdate(BaseModel):
    task_ids: List[int]
    update_data: TaskUpdate  

class BulkDeleteRequest(BaseModel):
    task_ids: List[int]

class BulkResponse(BaseModel):
    count: int

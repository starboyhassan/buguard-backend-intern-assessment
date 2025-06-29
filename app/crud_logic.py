from sqlmodel import Session
from .models import Task
from .schemas import TaskCreate
from fastapi import HTTPException


# Create Task
def create_task(db: Session, task_input: TaskCreate) -> Task:
    task = Task.model_validate(task_input) # convert pydantic model (TaskCreate) into a SQLModel ORM instance (Task)
    db.add(task)
    db.commit()
    db.refresh(task) #refreshe the task object with data from the database to ensure latest database-generated values #Without refresh(), task.id or created_at might still be None or outdated

    return task # to know the created object's details

# Get Task by ID
def get_task(db: Session, task_id: int) -> Task:
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Worng ID, Task not found")
    return task



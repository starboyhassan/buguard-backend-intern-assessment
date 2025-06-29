from sqlmodel import Session,select
from .models import Task
from .schemas import TaskCreate,TaskUpdate
from fastapi import HTTPException
from datetime import datetime, timezone


# Create Task
def create_task(db: Session, task_input: TaskCreate) -> Task:
    task = Task.model_validate(task_input) # convert pydantic model (TaskCreate) into a SQLModel ORM instance (Task)
    db.add(task)
    db.commit()
    db.refresh(task) 
    return task

# Get Task by ID
def get_task(db: Session, task_id: int) -> Task:
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Worng ID, Task not found")
    return task

# Get tasks with pagination and filter with status, priority
def get_tasks(db: Session, skip: int = 0, limit: int = 100, status: str = None, priority: str = None):
    query = select(Task).order_by(Task.id) # should use order_by to ensure all tasks orderd by ID
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    return db.exec(query.offset(skip).limit(limit)).all()


# Update Task
def update_task(db: Session, task_id: int, task: TaskUpdate) -> Task:
    db_task = db.get(Task, task_id)
    if not db_task:
        return None
    
    task_data = task.model_dump(exclude_unset=True)

    for key, value in task_data.items():
        setattr(db_task, key, value)

    db_task.updated_at = datetime.now(timezone.utc)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Delete Task
def delete_task(db: Session, task_id: int) -> bool:
    db_task = db.get(Task, task_id)
    
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True

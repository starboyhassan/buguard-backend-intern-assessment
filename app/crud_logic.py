from sqlmodel import Session
from .models import Task
from .schemas import TaskCreate

def create_task(db: Session, task_input: TaskCreate) -> Task:
    task = Task.model_validate(task_input) # convert pydantic model (TaskCreate) into a SQLModel ORM instance (Task)
    db.add(task)
    db.commit()
    db.refresh(task) #refreshe the task object with data from the database to ensure latest database-generated values #Without refresh(), task.id or created_at might still be None or outdated

    return task
from sqlmodel import select, func, asc, desc, or_
from .database import Session
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

# Get tasks with pagination and filters, soring and search
def get_tasks(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    status: str = None,
    priority: str = None,
    assigned_to: str = None,
    due_date_start: datetime = None,
    due_date_end: datetime = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    search: str = None
):

    query = select(Task)
    # apply advanced filtering >>> Multiple filters [Bonus Point]
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    if assigned_to:
        query = query.where(Task.assigned_to.ilike(f"%{assigned_to}%")) # ilike (case-insensitive like)
    if due_date_start:
        query = query.where(Task.due_date >= due_date_start)
    if due_date_end:
        query = query.where(Task.due_date <= due_date_end)

    # apply search >>> text search in title/description [Bonus Point]
    if search:
        search_term = f"%{search}%"
        query = query.where(or_(
            Task.title.ilike(search_term),
            Task.description.ilike(search_term)
        ))

    # apply orting>>> Dynamic field sorting [Bonus Point]
    valid_sort_fields = {
        "id", "title", "status", "priority", 
        "created_at", "updated_at", "due_date"
    }
    if sort_by in valid_sort_fields:
        sort_field = getattr(Task, sort_by)
    else:
        sort_field = Task.created_at
    
    if sort_order.lower() == "asc":
        query = query.order_by(asc(sort_field))
    else:
        query = query.order_by(desc(sort_field))
    
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


###########BULK OPERATIONS###############

#bulk update
def bulk_update_tasks(db: Session, task_ids: list, update_data: TaskUpdate ) -> dict:

    update_dict = update_data.model_dump(exclude_unset=True)
    count = 0
    errors = []
    
    for task_id in task_ids:
        task = db.get(Task, task_id)
        if not task:
            errors.append(f"Task {task_id} not found")
            continue
            
        try:
            for field, value in update_dict.items():
                #skip id and created_at which shouldnt be updated
                if field in ["id", "created_at"]:
                    continue
                    
                #special handling for updated_at
                if field == "updated_at":
                    setattr(task, field, datetime.now(timezone.utc))
                else:
                    # validation for each task
                    if field == "title" and value:
                        value = value.strip()
                        if not value:
                            raise ValueError("Title cannot be empty")
                    if field == "due_date" and value and value < datetime.now(timezone.utc):
                        raise ValueError("Due date must be in the future")
                        
                    setattr(task, field, value)

            #add the updated_at in object
            task.updated_at = datetime.now(timezone.utc)
            db.add(task)
            count += 1
        except Exception as e:
            errors.append(f"Task {task_id}: {str(e)}")
    
    if count > 0:
        db.commit()
    
    return {"count": count, "errors": errors}



#bulk delete
def bulk_delete_tasks(db: Session, task_ids: list) -> dict:
    count = 0
    errors = []
    
    for task_id in task_ids:
        task = db.get(Task, task_id)
        if not task:
            errors.append(f"Task {task_id} not found")
            continue
            
        try:
            db.delete(task)
            count += 1
        except Exception as e:
            errors.append(f"Task {task_id}: {str(e)}")
    
    if count > 0:
        db.commit()
    
    return {"count": count, "errors": errors}


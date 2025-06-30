from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session
from . import crud_logic, schemas
from .database import get_session
from typing import List, Optional
from datetime import datetime

router = APIRouter()

# POST Task
@router.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
def create(task: schemas.TaskCreate, db: Session = Depends(get_session)):
    return crud_logic.create_task(db, task)



# GET tasks with pagination and filters, search, sorting
@router.get("/tasks", response_model=List[schemas.TaskResponse])
def read_tasks(

    # pagination parameters
    skip: int = Query(0, ge=0, description="num of tasks to skip"),
    limit: int = Query(10, le=1000, description="max num of tasks to return"),
    
    # advanced filters parameters
    status: Optional[str] = Query(None, description="filter by task status"),
    priority: Optional[str] = Query(None, description="filter by task priority"),
    assigned_to: Optional[str] = Query(None, description="filter by assigne"),
    due_date_start: Optional[datetime] = Query(None, description="filter by due date starting from"),
    due_date_end: Optional[datetime] = Query(None, description="filter by due date ending at"),
    
    # sorting parameters
    sort_by: Optional[str] = Query("created_at", description="Field to sort by (id, title, status, priority, created_at, updated_at, due_date)"),
    sort_order: Optional[str] = Query("desc", description="Sort order (asc or desc)"),
    
    # search Parameter
    search: Optional[str] = Query(None, description="Search text in title or description"),
    
    db: Session = Depends(get_session)
):
    return crud_logic.get_tasks(
        db=db,
        skip=skip,
        limit=limit,
        status=status,
        priority=priority,
        assigned_to=assigned_to,
        due_date_start=due_date_start,
        due_date_end=due_date_end,
        sort_by=sort_by,
        sort_order=sort_order,
        search=search
    )



# GET tasks based on status
@router.get("/tasks/status/{status}", response_model=List[schemas.TaskResponse])
def get_tasks_by_status(status: str, db: Session = Depends(get_session)):
    return crud_logic.get_tasks(db, status=status)

# GET tasks based on priority
@router.get("/tasks/priority/{priority}", response_model=List[schemas.TaskResponse])
def get_tasks_by_priority(priority: str, db: Session = Depends(get_session)):
    return crud_logic.get_tasks(db, priority=priority)

# Update Task
@router.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_session)):
    updated_task = crud_logic.update_task(db, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

# Delete Task
@router.delete("/tasks/{task_id}")
def delete(task_id: int, db: Session = Depends(get_session)):
    if not crud_logic.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"Message": "Task deleted DONE"}


###########BULK OPERATIONS###############

#BULK UPDATE
@router.put("/tasks/bulk", response_model=schemas.BulkResponse)
def bulk_update_endpoint(bulk_update: schemas.BulkTaskUpdate, db: Session = Depends(get_session)):
    result = crud_logic.bulk_update_tasks(db, bulk_update.task_ids, bulk_update.update_data)
    

    if result["errors"]:
        # if all operations failed >> return 400
        if result["count"] == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "All updates failed",
                    "errors": result["errors"]
                })
        
        return result  # 200 OK with errors >> partial success
    
    return result  # 200 OK >> all success

#BULK DELETE
@router.delete("/tasks/bulk", response_model=schemas.BulkResponse)
def bulk_delete_endpoint(delete_data: schemas.BulkDeleteRequest, db: Session = Depends(get_session)):
    result = crud_logic.bulk_delete_tasks(db, delete_data.task_ids)
    
    if result["errors"]:
        # if all operations failed >> return 400
        if result["count"] == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "All deletions failed",
                    "errors": result["errors"]
                })
        
        return result  # 200 OK with errors >> partial success
    
    return result  # 200 OK >> all success

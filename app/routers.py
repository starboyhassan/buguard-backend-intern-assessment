from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session
from . import crud_logic, schemas
from .database import get_session
from typing import List


router = APIRouter()

# POST Task
@router.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
def create(task: schemas.TaskCreate, db: Session = Depends(get_session)):
    return crud_logic.create_task(db, task)

# GET tasks with pagination and filter with status, priority
@router.get("/tasks", response_model=List[schemas.TaskResponse])
def read_tasks(skip: int = Query(0, ge=0, description="Number of tasks to skip"), limit: int = Query(10, ge=1, le=1000, description="Maximum tasks to return"),
                status: str = None, priority: str = None, session: Session = Depends(get_session)):
    return crud_logic.get_tasks(session, skip, limit, status, priority)

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

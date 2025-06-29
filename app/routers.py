from fastapi import APIRouter, Depends
from sqlmodel import Session
from . import crud_logic, schemas
from .database import get_session

router = APIRouter()

@router.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
def create(task: schemas.TaskCreate, db: Session = Depends(get_session)):
    return crud_logic.create_task(db, task)

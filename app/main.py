from fastapi import FastAPI
from .database import init_db
from .routers import router
from datetime import datetime, timezone

app = FastAPI(
    title="Task Management API",
    description="A robust task management system for cybersecurity operations",
    version="1.0.0"
)

app.include_router(router)

@app.on_event("startup")
def on_startup():
    init_db()

# Root endpoint - API information
@app.get("/", tags=["Root"])
def read_root():
    return {
        "name": "Task Management API",
        "version": "1.0.0",
        "description": "Secure task management system for cybersecurity teams",
        "endpoints": {
            "root": "/",
            "health": "/health",
            "documentation": "/docs",
            "create_task": "POST /tasks",
            "list_tasks": "GET /tasks",
            "get_task": "GET /tasks/{task_id}",
            "update_task": "PUT /tasks/{task_id}",
            "delete_task": "DELETE /tasks/{task_id}",
            "tasks_by_status": "GET /tasks/status/{status}",
            "tasks_by_priority": "GET /tasks/priority/{priority}"
        }
    }

# Health check endpoint
@app.get("/health", tags=["Health Check"])
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
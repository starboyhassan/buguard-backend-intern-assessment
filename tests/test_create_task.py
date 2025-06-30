import sys
import os
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

client = TestClient(app)

def test_create_task():
    dueDate = (datetime.now(timezone.utc) + timedelta(days=7))
    dueDateIso = dueDate.isoformat()  # JSON only knows about strings #the method taks datetime object and turns it into a string

    
    response = client.post("/tasks", json={
        "title": "Test task",
        "description": "Test task description",
        "status": "completed",
        "due_date": dueDateIso,
        "priority": "high",
        "assigned_to": "Test task Team"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["priority"] == "high"
    assert "id" in data

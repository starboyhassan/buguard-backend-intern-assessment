from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta, timezone

client = TestClient(app)

def test_create_task():
    dueDate = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
    
    response = client.post("/tasks", json={
        "title": "Test task",
        "description": "Test task description",
        "status": "completed",
        "due_date": dueDate,
        "priority": "high",
        "assigned_to": "Test task Team"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Future task"
    assert data["due_date"] == dueDate
    assert data["priority"] == "high"
    assert "id" in data

import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

client = TestClient(app)

def test_get_tasks():
    
    #GET tasks
    response = client.get("/tasks")
    
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 1
    
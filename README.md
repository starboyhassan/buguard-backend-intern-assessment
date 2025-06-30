# Task Management API

**Task Management API Assessment for Buguard Backend Internship**
---
**Candidate**: Mahmoud Hassan  
**Email**: [mahmoudhassan7x@gmail.com](mahmoudhassan7x@gmail.com)  
**Mobile**: [+20 106 147 5854](tel:+201061475854)  
**LinkedIn**: [linkedin.com/in/mahmoudhassan7](https://www.linkedin.com/in/mahmoudhassan7/)  
**CV**: [https://drive.google.com/file/d/1NMQ09resLtINUzxWsAgSezzL8TFpiOKS/view?usp=drive_link](https://drive.google.com/file/d/1NMQ09resLtINUzxWsAgSezzL8TFpiOKS/view?usp=drive_link)  

---

## Features
- Complete CRUD operations
    - Create Task
    - Get all Tasks
    - Get/Update/Delete task by ID
    - Get Task by Status/Priority
- Health endpoint
- Data Validation
- Error Handling
- Pagination
- Database Integration
- API Documentation
- Pre-populated security task examples in DB file
- Bonus Points
    - Advanced filtering
    - sorting
    - Search
    - Bulk update/delete operations
    - Test Cases
    - Docker support

## Setup

### Prerequisites
- Python 3.10+
- Docker
### Installation
```bash
# Create virtual environment
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate  # Linux
myenv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

#Running the Application
uvicorn app.main:app --reload

```
#
### Accessing Documentation
Swagger UI: http://localhost:8000/docs

#

### Docker Setup
```bash
# Build image
docker build -f docker/Dockerfile -t task-api .

# Run container
docker run -p 8000:8000 task-api
```

## Example API Calls
### 1. Create Task

```bash
curl -X POST "http://localhost:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{
        "title": "Vulnerability Scan",
        "description": "Run weekly network vulnerability scan",
        "status": "in_progress",
        "priority": "high",
        "due_date": "2025-07-15T14:00:00Z",
        "assigned_to": "SOC Team"
     }'

```
### 2. List Tasks (with filtering)

```bash
curl "http://localhost:8000/tasks?priority=high&status=in_progress&sort_by=due_date&sort_order=asc"

```
### 3. Bulk Update 
```bash
curl -X PUT "http://localhost:8000/tasks/bulk" \
     -H "Content-Type: application/json" \
     -d '{
        "task_ids": [1, 3, 5],
        "update_data": {"status": "in_progress"}
     }'
```

## Design Decisions
### Security Focus
#### 1. Input Validation:
- Title cannot be empty
- Due dates must be in future
- Enum restrictions for status/priority
#### 2. Data Sanitization:
- Automatic trimming of string inputs
- Timezone-aware timestamps (UTC)

#### 3. Error Handling:

1. 404 for missing resources
2. 422 for validation errors
3. 400 for client errors
4. 500 for internal server errors

### Performance Optimizations
#### 1. Bulk Operations:
- updates/deletes for multiple tasks
- Partial success reporting

#### 2. Efficient Queries:
- Dynamic filtering/sorting
- Pagination support (skip/limit)

#### 3. Database Health Checks:

```http://localhost:8000/health``` endpoint verifies DB connectivity



### Production Readiness
#### 1. Containerization:
- Docker support with slim image
- Pre-populated database

#### 2. Monitoring:

- Health check endpoint
- Timestamped responses

#### 3. Testing:

- Unit tests for core functionality
- Sample test cases included

## Future Enhancements
### 1. Authentication & Authorization:
  - **Why**: for securing task management operations in team environments
   - **Benefit**: 
     - Prevents unauthorized access to security tasks
     - Enables role based access control for different team members
### 2. Database Migration to PostgreSQL:
   - **Why**: SQLite doesn't scale for production workloads
   - **Benefit**: Concurrent connections
### 3. Asynchronous Processing:
   - **Why**: Handle more requests with same resources
   - **Benefit**: throughput improvement for IO Bound operations
### 4. Caching Layer (Redis Caching)
   - **Why**: Reduce database load for frequent queries
   - **Benefit**: Reduce response times for common requests

### 5. CI/CD Pipeline:
   - **Why**: Automate testing and deployment
   - **Benefit**: Reduce time (Auomated process), consistent deployments

### 6. Cloud Deployment:
   - **Why**: Enterprise grade scalability and reliability
   - **Benefit**: AutoScaling, global availability


### 7. Nginx :
   - **Why**: Essential for production deployments
   - **Benefit**: SSL , load balancing


## Sample Data
```bash
[
  {
    "title": "Security Awareness Training",
    "description": "Launch phishing simulation and track employee click-through rates.",
    "status": "pending",
    "priority": "medium",
    "due_date": "2025-08-10T09:30:00Z",
    "assigned_to": "GRC Team",
    "id": 1,
    "created_at": "2025-06-30T13:03:23.724335",
    "updated_at": null
  },
  {
    "title": "Incident Response Drill",
    "description": "Simulate ransomware attack scenario and evaluate IR playbooks.",
    "status": "pending",
    "priority": "high",
    "due_date": "2025-07-18T11:00:00Z",
    "assigned_to": "IR Team",
    "id": 2,
    "created_at": "2025-06-30T13:03:05.174311",
    "updated_at": null
  }
]
```

## Testing Instructions
### 1. Run test cases
```bash
# run the app
uvicorn app.main:app --reload

# run test cases for endpoints testing
python3 tests/run_tests.py
```
When you open the terminal test cases information will apear to you

### 2. Check Health and DB connection
```bash
 http://localhost:8000/health

 # Expected: {"status":"healthy","database":"connected","timestamp":"..."}
```
#
#
# Thank you, waiting for your feedback. 
# THE END
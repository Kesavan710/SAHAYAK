# Sahayak Testing Guide

## Quick Start - Test Current System

### 1. Make Sure Server is Running

```bash
cd /home/kesavan-p/Documents/Sahayak_Hackathon/SAHAYAK/backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 2. Run Test Script

Open a **new terminal** and run:

```bash
cd /home/kesavan-p/Documents/Sahayak_Hackathon/SAHAYAK/backend
python test_current_endpoints.py
```

This will test all current endpoints and show you what's working.

### 3. Interactive API Testing

Open your browser and go to:
```
http://localhost:8000/docs
```

This opens **Swagger UI** where you can:
- See all endpoints
- Try them interactively
- See request/response schemas
- No coding required!

## Testing Methods

### Method 1: Browser (Easiest)

**Swagger UI**: `http://localhost:8000/docs`
- Click any endpoint
- Click "Try it out"
- Fill in parameters
- Click "Execute"
- See response immediately

**ReDoc**: `http://localhost:8000/redoc`
- Better for reading documentation
- Clean interface

### Method 2: curl (Command Line)

#### Test Health
```bash
curl http://localhost:8000/health | python -m json.tool
```

#### Test Root
```bash
curl http://localhost:8000/ | python -m json.tool
```

#### Test Chat (if agent is created)
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is PM-KISAN scheme?",
    "user_id": "test_user"
  }' | python -m json.tool
```

#### Test Profile Creation
```bash
curl -X POST "http://localhost:8000/api/v1/profile?user_id=test123" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "age": 30,
    "gender": "Male",
    "mobile": "9876543210",
    "address": "Test Address, Bangalore",
    "district": "Bangalore Urban",
    "state": "Karnataka",
    "pincode": "560001",
    "annual_family_income": 100000,
    "caste_category": "General"
  }' | python -m json.tool
```

#### Test Documents Listing
```bash
curl http://localhost:8000/api/v1/schemes/pm-kisan/documents | python -m json.tool
```

### Method 3: Python Script (Best for Automation)

Use the provided `test_current_endpoints.py` or create custom tests:

```python
import requests

# Test health
response = requests.get("http://localhost:8000/health")
print(response.json())

# Test chat
response = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={"message": "Hello", "user_id": "test"}
)
print(response.json())
```

### Method 4: Postman (GUI Tool)

1. Download Postman: https://www.postman.com/downloads/
2. Import OpenAPI spec: `http://localhost:8000/openapi.json`
3. All endpoints auto-loaded
4. Click to test any endpoint

## Testing RPwD Endpoints (When Implemented)

Once you implement the RPwD features, use this test flow:

### Complete RPwD Application Flow Test

```bash
# 1. Start conversation
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am Venu, 21 years old from Bengaluru. I have visual impairment since birth.",
    "language": "en"
  }'

# Save the session_id and application_id from response

# 2. Continue conversation
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "<session_id_from_step_1>",
    "message": "My father is Ravi Kumar and mother is Lakshmi Devi",
    "language": "en"
  }'

# 3. Check application status
curl http://localhost:8000/api/v1/applications/<application_id>

# 4. Update specific field (if needed)
curl -X PATCH http://localhost:8000/api/v1/applications/<application_id> \
  -H "Content-Type: application/json" \
  -d '{
    "updates": {
      "education_and_occupation": {
        "educational_status": "Graduate",
        "occupation": "Student"
      }
    }
  }'

# 5. Validate application
curl -X POST http://localhost:8000/api/v1/applications/<application_id>/validate

# 6. Confirm declaration
curl -X POST http://localhost:8000/api/v1/applications/<application_id>/confirm \
  -H "Content-Type: application/json" \
  -d '{
    "confirmed": true,
    "application_place": "Bengaluru"
  }'

# 7. Generate PDF
curl -X POST http://localhost:8000/api/v1/applications/<application_id>/generate-pdf

# 8. Get PDF download link
curl http://localhost:8000/api/v1/applications/<application_id>/pdf
```

## Common Testing Scenarios

### Scenario 1: Happy Path (Everything Works)

```python
# User provides all info naturally
message = """
I am Venu Kumar, 21 years old. My father is Ravi Kumar and mother is Lakshmi Devi.
I was born on May 15, 2002. I am male.
I live at 123 MG Road, Indiranagar, Bengaluru, Karnataka - 560038.
I have visual impairment since birth.
I am a BSc student.
I have never applied for a disability certificate before.
My Aadhaar is available and I have passport photos.
"""

# Agent should extract most fields, ask only for missing details
```

### Scenario 2: Incomplete Information

```python
message = "I have a disability"

# Agent should ask:
# - What type of disability?
# - Basic personal information
# - When did it occur?
# etc.
```

### Scenario 3: Conditional Logic Test

```python
# Test 1: Same address
# If user says communication address same as permanent
# Agent should NOT ask for communication address again

# Test 2: From birth disability
# If onset_type = from_birth
# Agent should NOT ask for onset_year

# Test 3: No previous application
# If previously_applied = false
# Agent should NOT ask for authority/district/result
```

## Debugging Failed Tests

### Problem: Connection Refused

```
Error: Connection refused at http://localhost:8000
```

**Solution**:
```bash
# Check if server is running
ps aux | grep "python.*main.py"

# If not, start it
cd backend
python main.py
```

### Problem: 404 Not Found

```
Status Code: 404
Error: Not Found
```

**Solution**:
- Endpoint doesn't exist yet
- Check endpoint path spelling
- Verify it's implemented in routers

### Problem: 422 Validation Error

```
Status Code: 422
Error: Validation error
```

**Solution**:
- Check request body format
- Ensure required fields are present
- Verify field types match schema

### Problem: 500 Internal Server Error

```
Status Code: 500
Error: Internal server error
```

**Solution**:
- Check server logs for stack trace
- Likely a bug in endpoint code
- May need to create agent first (for /chat endpoint)

## Automated Testing (For CI/CD)

Create `backend/tests/test_api.py`:

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Sahayak API" in response.text

def test_chat_endpoint():
    response = client.post("/api/v1/chat", json={
        "message": "Hello",
        "user_id": "test"
    })
    assert response.status_code in [200, 500]  # 500 if agent not created

# Run with: pytest backend/tests/
```

## Performance Testing

### Load Test with Apache Bench

```bash
# Install apache bench
sudo apt-get install apache2-utils

# Test health endpoint (100 requests, 10 concurrent)
ab -n 100 -c 10 http://localhost:8000/health

# Test chat endpoint
ab -n 50 -c 5 -p chat_request.json -T application/json http://localhost:8000/api/v1/chat
```

### Load Test with wrk

```bash
# Install wrk
sudo apt-get install wrk

# Test for 30 seconds with 10 connections
wrk -t10 -c10 -d30s http://localhost:8000/health
```

## Monitoring in Production

### Health Check Endpoint

```bash
# Should always return 200
curl http://localhost:8000/health

# Use for:
# - Kubernetes liveness/readiness probes
# - Load balancer health checks
# - Monitoring systems (Prometheus, etc.)
```

### Metrics Collection

```python
# Add to main.py for basic metrics
from fastapi import Request
import time

@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"{request.method} {request.url.path} - {process_time:.3f}s")
    return response
```

## Quick Reference Commands

```bash
# Start server
python backend/main.py

# Test current endpoints
python backend/test_current_endpoints.py

# View API docs
# Open: http://localhost:8000/docs

# Test specific endpoint
curl http://localhost:8000/health

# Check server logs
# Look at terminal where server is running

# Stop server
# Press Ctrl+C in server terminal
```

## Summary

1. **Use Swagger UI** (`/docs`) for interactive testing - easiest method
2. **Use test script** for automated validation
3. **Use curl** for quick command-line tests
4. **Check logs** when things fail
5. **Test incrementally** as you implement features

Happy testing! 🧪

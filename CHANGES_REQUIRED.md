# Required Changes Based on RPwD Blueprint

## Summary

The PDF defines a **complete rewrite** for an **RPwD (Rights of Persons with Disabilities) application preparation feature**, not a general scheme assistant.

## What I've Created

### ✅ 1. RPwD Application Schema (`backend/schemas/rpwd_application.py`)
Complete data model with:
- All fields from the blueprint
- Validation rules
- Conditional logic
- Request/Response models
- Enums for all categories

## What Still Needs to Be Done

### 2. Services Layer (Need to Create)

#### `backend/services/application_state.py`
```python
class ApplicationStateService:
    def __init__(self):
        self.applications = {}  # In-memory for MVP
    
    def create_application(self, session_id: str) -> RPwDApplication
    def get_application(self, application_id: str) -> RPwDApplication
    def update_application(self, application_id: str, updates: dict) -> RPwDApplication
    def merge_extracted_fields(self, app: RPwDApplication, extracted: dict) -> RPwDApplication
    def calculate_completion(self, app: RPwDApplication) -> int
```

#### `backend/services/validation.py`
```python
class ValidationService:
    def get_missing_fields(self, app: RPwDApplication) -> List[str]
    def validate_application(self, app: RPwDApplication) -> ValidationResponse
    def get_conditional_requirements(self, app: RPwDApplication) -> List[str]
    def is_ready_for_pdf(self, app: RPwDApplication) -> bool
```

#### `backend/services/pdf_generator.py`
```python
class PDFGeneratorService:
    def generate_rpwd_application_pdf(self, app: RPwDApplication) -> bytes
    def create_application_summary(self, app: RPwDApplication) -> dict
```

#### `backend/services/storage.py`
```python
class S3StorageService:
    def __init__(self, bucket_name: str):
        self.s3_client = boto3.client('s3')
        self.bucket = bucket_name
    
    def store_pdf(self, application_id: str, pdf_bytes: bytes) -> str
    def get_signed_url(self, s3_key: str, expiration: int = 3600) -> str
    def store_application_json(self, application_id: str, data: dict) -> str
```

### 3. Agent Updates

#### Update `backend/foundry/prompts.py`
Replace generic system prompt with RPwD-specific:
```python
RPWD_SYSTEM_PROMPT = """You are Sahayak, helping prepare RPwD disability certificate applications.

CRITICAL RULES:
1. EXTRACT FIRST, ASK LATER
   - Extract ALL fields present in user's natural language
   - Only ask for fields that are truly missing
   - Never ask questions you already have answers to

2. CONDITIONAL LOGIC
   - If same_as_permanent=true, skip communication address
   - If previously_applied=false, skip authority/district/result
   - If onset_type=from_birth, skip onset_year
   - If has_guardian=false, skip guardian details

3. BOUNDARIES
   - You prepare information ONLY
   - NEVER claim to issue certificates
   - NEVER claim to submit applications
   - NEVER medically diagnose
   - NEVER handle OTPs/passwords/CAPTCHA

4. SINGLE QUESTION RULE
   - Ask ONE question at a time
   - Make it the most relevant missing field
   - Be conversational, not robotic

5. EXTRACTION FORMAT
   When extracting, return structured JSON matching RPwDApplication schema.
"""
```

#### Create `backend/agent/field_extractor.py`
```python
def extract_application_fields(message: str, current_app: RPwDApplication) -> dict:
    """
    Use LLM to extract RPwDApplication fields from natural language.
    Returns dict with extracted fields.
    """
```

### 4. API Routers

#### `backend/api/rpwd_chat.py`
```python
@router.post("/chat", response_model=ChatResponse)
async def rpwd_chat(request: ChatRequest):
    # 1. Get or create application
    # 2. Extract fields from message
    # 3. Merge with current state
    # 4. Validate and get missing fields
    # 5. Generate next question
    # 6. Return response
```

#### `backend/api/rpwd_applications.py`
```python
@router.get("/applications/{application_id}")
@router.patch("/applications/{application_id}")
@router.post("/applications/{application_id}/validate")
@router.post("/applications/{application_id}/confirm")
@router.post("/applications/{application_id}/generate-pdf")
@router.get("/applications/{application_id}/pdf")
```

### 5. Update `backend/main.py`

Remove old routers, add new ones:
```python
from api import rpwd_chat, rpwd_applications

app.include_router(rpwd_chat.router, prefix="/api/v1", tags=["RPwD Chat"])
app.include_router(rpwd_applications.router, prefix="/api/v1", tags=["RPwD Applications"])
```

### 6. Environment Variables

Add to `.env`:
```bash
# S3 Storage (required for PDF storage)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=ap-south-1
S3_BUCKET_NAME=sahayak-rpwd

# Existing Azure vars stay the same
FOUNDRY_PROJECT_ENDPOINT=...
FOUNDRY_MODEL_DEPLOYMENT=...
BING_CONNECTION_ID=...
```

### 7. Dependencies

Add to `requirements.txt`:
```
boto3>=1.34.0  # For S3
reportlab>=4.0.0  # For PDF generation
```

## Quick Implementation Steps

Since this is a major change, here's the fastest path:

### Phase 1: Core Schema ✅ (DONE)
- Created RPwD application schema

### Phase 2: Services (30 min)
1. Create `backend/services/` directory
2. Implement application_state.py (in-memory storage)
3. Implement validation.py (field checking)
4. Implement pdf_generator.py (basic PDF)
5. Implement storage.py (S3 operations)

### Phase 3: API Layer (30 min)
1. Create `backend/api/` directory
2. Implement rpwd_chat.py
3. Implement rpwd_applications.py
4. Update main.py

### Phase 4: Agent (30 min)
1. Create field extraction tool
2. Update system prompt
3. Wire into chat endpoint

### Phase 5: Testing (30 min)
1. Test chat flow
2. Test PDF generation
3. Test S3 upload
4. End-to-end workflow

## Key Differences from Original Design

| Aspect | Original (Generic Schemes) | New (RPwD Application) |
|--------|---------------------------|----------------------|
| Scope | Multiple schemes | Single RPwD application |
| Data Model | Generic UserProfile | Detailed RPwDApplication |
| Workflow | Q&A about schemes | Information extraction + PDF generation |
| Storage | In-memory only | S3 for PDFs |
| Endpoints | 6 generic endpoints | 7 RPwD-specific endpoints |
| Agent Behavior | Answer questions | Extract fields, ask smartly |

## Testing the New System

```bash
# 1. Start server
python backend/main.py

# 2. Test chat
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am Venu, 21 years old from Bengaluru. I have visual impairment since birth.",
    "language": "en"
  }'

# Expected: Agent extracts name, age, city, disability, onset
# Then asks for missing field like father's name

# 3. Continue conversation
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "<from-previous-response>",
    "message": "My father is Ravi Kumar",
    "language": "en"
  }'

# 4. Get application status
curl http://localhost:8000/api/v1/applications/{application_id}

# 5. Confirm and generate PDF
curl -X POST http://localhost:8000/api/v1/applications/{application_id}/confirm \
  -H "Content-Type: application/json" \
  -d '{"confirmed": true, "application_place": "Bengaluru"}'

curl -X POST http://localhost:8000/api/v1/applications/{application_id}/generate-pdf
```

## Timeline Estimate

- **Minimum Viable**: 2-3 hours (basic extraction, validation, simple PDF)
- **Production Quality**: 6-8 hours (complete validation, good PDF, S3)
- **Full Featured**: 12+ hours (error handling, retries, comprehensive testing)

## Recommendation

Given this is a hackathon:

1. **Keep the schema** I created (it's complete)
2. **Implement services** with minimal features first
3. **Create basic PDF** (text-based, not fancy)
4. **Use S3 mock** if AWS setup takes time
5. **Focus on the demo flow** - one complete end-to-end example

The blueprint is comprehensive but you can iterate. Start with the happy path!

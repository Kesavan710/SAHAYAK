# Backend Restructure Summary

## What Changed

The PDF blueprint reveals this is **NOT a general scheme assistant** but specifically an **RPwD (Rights of Persons with Disabilities) application preparation system**.

## Current Status

### ✅ COMPLETED

1. **RPwD Application Schema** (`backend/schemas/rpwd_application.py`)
   - Complete 300+ line data model
   - All fields from blueprint
   - Validation rules
   - Conditional logic
   - Request/Response models

2. **Documentation**
   - `RPWD_IMPLEMENTATION_PLAN.md` - Strategy overview
   - `CHANGES_REQUIRED.md` - Detailed implementation guide
   - This file - Quick summary

### ⏳ NEEDS TO BE DONE

The following files need to be created from scratch:

#### Services Layer
- `backend/services/application_state.py` - Manage application state
- `backend/services/validation.py` - Field validation logic
- `backend/services/pdf_generator.py` - Generate RPwD application PDF
- `backend/services/storage.py` - S3 storage operations

#### API Layer  
- `backend/api/rpwd_chat.py` - Conversational chat endpoint
- `backend/api/rpwd_applications.py` - Application CRUD endpoints

#### Agent Updates
- Update `backend/foundry/prompts.py` with RPwD-specific prompt
- Create `backend/agent/field_extractor.py` for NLP extraction

#### Main App
- Update `backend/main.py` to use new routers

## Key Principle: Extract First, Ask Later

❌ **WRONG** (Old way):
```
Agent: "What is your name?"
User: "Venu"
Agent: "What is your age?"
User: "21"
Agent: "What is your city?"
User: "Bengaluru"
```

✅ **RIGHT** (New way):
```
User: "I am Venu, 21 years old from Bengaluru with visual impairment since birth"
Agent extracts:
  - name: Venu
  - age: 21
  - city: Bengaluru
  - disability: Visual Impairment
  - onset: from_birth
Agent: "Thank you Venu. What is your father's name?"
```

## API Endpoints Required

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/chat` | POST | Conversational information collection |
| `/applications/{id}` | GET | Get application status |
| `/applications/{id}` | PATCH | Update application fields |
| `/applications/{id}/validate` | POST | Validate completeness |
| `/applications/{id}/confirm` | POST | Confirm declaration |
| `/applications/{id}/generate-pdf` | POST | Generate PDF package |
| `/applications/{id}/pdf` | GET | Download PDF |

## What the Old Code Did

- Generic scheme eligibility checking
- Document requirements listing
- Form field explanations
- Application status tracking (mock)
- Multiple schemes support

## What the New Code Must Do

- Extract RPwD application fields from natural language
- Manage complex conditional logic (30+ fields)
- Validate based on disability type, previous applications, etc.
- Generate professional PDF application package
- Store PDFs in S3
- Track completion percentage
- Never claim to submit or issue certificates

## Environment Variables Needed

Add to `.env`:
```bash
# NEW - Required for PDF storage
AWS_ACCESS_KEY_ID=your-key-here
AWS_SECRET_ACCESS_KEY=your-secret-here
AWS_REGION=ap-south-1
S3_BUCKET_NAME=sahayak-rpwd

# EXISTING - Keep these
FOUNDRY_PROJECT_ENDPOINT=https://sahayak-christinhack.openai.azure.com/openai/v1
FOUNDRY_MODEL_DEPLOYMENT=gpt-5.4-mini
BING_CONNECTION_ID=your-bing-connection-id-here
```

## Dependencies to Add

```bash
pip install boto3 reportlab
```

## Fastest Path to Working Demo

1. **Use my schema** ✅ (already done)

2. **Create minimal services**:
   ```python
   # application_state.py - Just dict storage
   # validation.py - Check required fields
   # pdf_generator.py - Simple text PDF
   # storage.py - Mock S3 or real if time permits
   ```

3. **Create API endpoints**:
   ```python
   # Start with /chat endpoint only
   # Add others as time permits
   ```

4. **Update agent**:
   ```python
   # Change system prompt
   # Add extraction logic
   ```

5. **Test one complete flow**:
   ```
   User speaks → Extract fields → Ask for missing → Confirm → Generate PDF → Download
   ```

## What to Keep vs Replace

### KEEP (Still useful):
- `backend/foundry/agent.py` - Agent creation logic
- `backend/foundry/runner.py` - Conversation loop
- `backend/main.py` - FastAPI setup (just change routers)
- `backend/requirements.txt` - Add boto3, reportlab

### REPLACE/UPDATE:
- `backend/routers/*` - Replace with RPwD-specific ones
- `backend/models/*` - Use new schemas instead
- `backend/tools/*` - Replace with RPwD services
- `backend/foundry/prompts.py` - Update to RPwD focus

### DELETE (Not needed):
- `backend/tools/eligibility.py` - Not for RPwD flow
- `backend/tools/documents.py` - Different for RPwD
- `backend/tools/status.py` - Different tracking model

## Next Steps

1. Read `CHANGES_REQUIRED.md` for detailed implementation guide
2. Decide: Build from scratch or adapt existing?
3. If adapting: Start with routers, update one by one
4. If from scratch: Follow the services → API → agent sequence

## Time Estimate

- **Schema**: ✅ Done (1 hour saved!)
- **Services**: 1-2 hours (basic implementation)
- **API**: 1-2 hours (7 endpoints)
- **Agent**: 1 hour (prompt + extraction)
- **Testing**: 1 hour (end-to-end flow)
- **Total**: 4-6 hours for MVP

Good luck! The schema is solid, now just wire it up! 🚀

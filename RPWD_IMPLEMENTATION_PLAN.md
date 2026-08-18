# RPwD Implementation Plan

Based on the **Sahayak_RPwD_Shared_Schema_and_API_Blueprint.pdf**, I need to implement a complete RPwD (Rights of Persons with Disabilities) application preparation system.

## What's Changed

The original implementation was for **general scheme assistance**. The new requirement is specifically for **RPwD application preparation** with a very different workflow.

## Key Differences

### Old System (General Schemes)
- Multiple schemes (PM-KISAN, Ayushman Bharat, etc.)
- Generic eligibility checking
- Document listing
- Application status tracking

### New System (RPwD Application)
- **Single focused feature**: RPwD disability certificate application preparation
- **Conversational information extraction**: Extract multiple fields from natural language
- **Smart questioning**: Only ask for missing information
- **PDF generation**: Create application preparation package
- **S3 storage**: Store generated PDFs
- **Strict boundaries**: Never claim to submit applications or issue certificates

## Implementation Status

### ✅ Completed
1. **RPwD Application Schema** (`backend/schemas/rpwd_application.py`)
   - Complete data model with all required fields
   - Validation rules
   - Conditional field logic
   - Request/Response models

### 🔄 In Progress  
2. **Services Layer** (to create)
   - `backend/services/application_state.py` - State management
   - `backend/services/validation.py` - Field validation
   - `backend/services/pdf_generator.py` - PDF generation
   - `backend/services/storage.py` - S3 storage

3. **API Endpoints** (to update)
   - `POST /chat` - Conversational information collection
   - `GET /applications/{application_id}` - Get application status
   - `PATCH /applications/{application_id}` - Update application
   - `POST /applications/{application_id}/validate` - Validate application
   - `POST /applications/{application_id}/confirm` - Confirm declaration
   - `POST /applications/{application_id}/generate-pdf` - Generate PDF
   - `GET /applications/{application_id}/pdf` - Get PDF download link

4. **Agent Updates** (to modify)
   - Update agent to extract RPwD application fields
   - Implement smart questioning logic
   - Add field extraction from natural language
   - Conditional question logic

## Core Principles from Blueprint

### 1. Do NOT Interrogate the User
❌ Wrong: Ask all 30+ fields one by one
✅ Right: Extract everything possible from natural language, then ask only what's missing

Example:
```
User: "I am Venu, 21 years old. I live in Bengaluru. I have had visual impairment since birth."

Agent extracts:
✓ first_name: Venu
✓ age: 21
✓ city: Bengaluru  
✓ disability_type: Visual Impairment
✓ onset_type: from_birth

Then asks ONLY missing fields:
"What is your father's name?"
"What is your permanent address?"
```

### 2. Conditional Logic
- If `same_as_permanent = true`, don't ask for communication address
- If `previously_applied = false`, don't ask authority/district/result
- If `onset_type = from_birth`, don't ask onset_year
- If `has_guardian = false`, don't ask guardian details

### 3. Status Flow
1. `draft` → Application created
2. `collecting_information` → Gathering data
3. `ready_for_review` → All required fields complete
4. `confirmed` → User confirmed declaration
5. `pdf_generated` → PDF created and stored
6. `error` → Recoverable error

### 4. Important Boundaries
The agent must NEVER:
- Claim to issue a disability certificate
- Medically assess/diagnose the applicant
- Submit the government application
- Handle OTPs/passwords/CAPTCHA
- Complete authentication processes

## API Contract Summary

### POST /chat
```json
{
  "session_id": "optional-uuid",
  "message": "I am a BSc student...",
  "language": "en"
}
```

Response includes:
- `assistant_message`: What the agent says
- `application`: Current RPwDApplication state
- `missing_fields`: What's still needed
- `next_question`: The single next question to ask
- `status`: Current application status

### POST /applications/{id}/generate-pdf
Only allowed when:
- Status is `confirmed`
- All required fields are present
- Declaration is confirmed

Response includes:
- `pdf_object_key`: S3 location
- `download_url`: Signed temporary URL
- `generated_at`: Timestamp

## S3 Structure

```
sahayak-rpwd/
  applications/
    {application_id}/
      application.json
      uploads/
        residence-proof/
        previous-certificate/
      generated/
        rpwd_application_summary.pdf
      temp/
  {session_id}/
```

## Next Steps

1. Create services layer
2. Update API routers for RPwD endpoints
3. Modify agent to handle RPwD extraction
4. Add PDF generation capability
5. Integrate S3 storage
6. Update main.py to use new routes
7. Test complete workflow

## Required Environment Variables

Add to `.env`:
```
# S3 Storage
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret  
AWS_REGION=ap-south-1
S3_BUCKET_NAME=sahayak-rpwd

# Existing
FOUNDRY_PROJECT_ENDPOINT=...
FOUNDRY_MODEL_DEPLOYMENT=...
BING_CONNECTION_ID=...
```

This is a complete rewrite focusing on the RPwD use case!

# Sahayak Backend API

Complete backend implementation for Sahayak - an AI-powered assistant for Indian government welfare schemes.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Routers    │  │   Models     │  │    Tools     │     │
│  │              │  │              │  │              │     │
│  │ • Chat       │  │ • Profile    │  │ • Eligibility│     │
│  │ • Profile    │  │ • Chat       │  │ • Documents  │     │
│  │ • Eligibility│  │ • Application│  │ • Form Help  │     │
│  │ • Documents  │  │              │  │ • Application│     │
│  │ • Application│  │              │  │ • Status     │     │
│  │ • Status     │  │              │  │              │     │
│  └──────┬───────┘  └──────────────┘  └──────┬───────┘     │
│         │                                    │              │
│         └────────────────┬───────────────────┘              │
│                          │                                  │
│                  ┌───────▼────────┐                         │
│                  │  Agent Runner  │                         │
│                  │                │                         │
│                  │ • Conversation │                         │
│                  │   Management   │                         │
│                  │ • Tool Loop    │                         │
│                  └───────┬────────┘                         │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │  Azure AI Foundry    │
                │                      │
                │ Sahayak Agent        │
                │ • System Prompt      │
                │ • File Search Tool   │
                │ • Bing Grounding     │
                │ • Function Tools     │
                └──────────────────────┘
```

## Features Implemented

### 1. ✅ Azure AI Foundry Agent
- **System Prompt**: Strict rules preventing hallucination
- **File Search Tool**: Vector store for scheme knowledge base
- **Bing Grounding**: Live web search for deadlines (optional)
- **Five Custom Function Tools**: Local execution

### 2. ✅ Five Custom Tools
1. **check_eligibility**: Deterministic eligibility checking
2. **get_required_documents**: Document checklist generation
3. **explain_form_field**: Form field explanations
4. **generate_application_package**: Pre-filled application creation
5. **check_application_status**: Status tracking

### 3. ✅ Tool Execution Loop
- Automatic function calling via Responses API
- Local Python execution (not remote Azure Functions)
- Multi-turn conversation support
- Tool result integration

### 4. ✅ Session Management
- Conversation state management
- Multi-turn context preservation
- User-to-conversation mapping

### 5. ✅ FastAPI Endpoints

All endpoints from section 10 implemented:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/chat` | POST | Main conversational interface |
| `/api/v1/profile` | POST | Create/update user profile |
| `/api/v1/eligibility/check` | POST | Fast eligibility check |
| `/api/v1/schemes/{id}/documents` | GET | Get required documents |
| `/api/v1/application/package` | POST | Generate application package |
| `/api/v1/status/check` | POST | Check application status |

## Directory Structure

```
backend/
├── main.py                      # FastAPI app entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── foundry/                     # Azure AI Foundry integration
│   ├── __init__.py
│   ├── agent.py                 # Agent creation with all tools
│   ├── prompts.py               # System prompt with strict rules
│   ├── runner.py                # Conversation + tool execution loop
│   ├── tool_definitions.py      # FunctionTool schemas
│   └── example_usage.py         # Usage examples
│
├── tools/                       # Tool implementations
│   ├── __init__.py             # TOOL_DISPATCH mapping
│   ├── eligibility.py          # Eligibility checker
│   ├── documents.py            # Document fetcher
│   ├── form_helper.py          # Form field explainer
│   ├── application.py          # Application generator
│   └── status.py               # Status checker
│
├── models/                      # Pydantic models
│   ├── __init__.py
│   ├── user_profile.py         # UserProfile, ProfileUpdate
│   ├── chat.py                 # ChatRequest, ChatResponse
│   └── application.py          # Application models
│
└── routers/                     # API route handlers
    ├── __init__.py
    ├── chat.py                 # Chat endpoint
    ├── profile.py              # Profile CRUD
    ├── eligibility.py          # Eligibility endpoint
    ├── documents.py            # Documents endpoint
    ├── application.py          # Application endpoint
    └── status.py               # Status endpoint
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Add to your `.env` file in the project root:

```env
# Azure AI Foundry (REQUIRED)
FOUNDRY_PROJECT_ENDPOINT=https://sahayak-christinhack.openai.azure.com/openai/v1
FOUNDRY_MODEL_DEPLOYMENT=gpt-5.4-mini

# Bing Search (OPTIONAL - for live deadline grounding)
BING_CONNECTION_ID=your-bing-connection-id-here
```

**Note**: If `BING_CONNECTION_ID` is not set, the agent will work with File Search only (this is fine for the hackathon).

### 3. Authenticate with Azure

```bash
az login
```

### 4. Create the Agent (One-time Setup)

```bash
cd backend/foundry
python example_usage.py
```

This will:
- Upload scheme documents from your specified directory
- Create vector store for file search
- Create the agent with all tools

### 5. Run the API Server

```bash
cd backend
python main.py
```

Server will start at: `http://localhost:8000`

API docs: `http://localhost:8000/docs`

## API Usage Examples

### 1. Start a Conversation

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is PM-KISAN scheme?",
    "user_id": "user_123"
  }'
```

### 2. Check Eligibility

```bash
curl -X POST http://localhost:8000/api/v1/eligibility/check \
  -H "Content-Type: application/json" \
  -d '{
    "scheme_id": "pm-kisan",
    "user_profile": {
      "full_name": "Rajesh Kumar",
      "age": 45,
      "gender": "Male",
      "mobile": "9876543210",
      "address": "Village Rampur",
      "district": "Varanasi",
      "state": "Uttar Pradesh",
      "pincode": "221001",
      "annual_family_income": 80000,
      "caste_category": "General",
      "is_farmer": true,
      "land_holding_acres": 2.5
    }
  }'
```

### 3. Get Required Documents

```bash
curl http://localhost:8000/api/v1/schemes/pm-kisan/documents
```

### 4. Generate Application Package

```bash
curl -X POST http://localhost:8000/api/v1/application/package \
  -H "Content-Type: application/json" \
  -d '{
    "scheme_id": "pm-kisan",
    "output_format": "both",
    "user_profile": { ... }
  }'
```

### 5. Check Application Status

```bash
curl -X POST http://localhost:8000/api/v1/status/check \
  -H "Content-Type: application/json" \
  -d '{
    "scheme_id": "pm-kisan",
    "application_id": "APP123456",
    "mobile_or_aadhaar": "9876543210"
  }'
```

## Key Design Decisions

### 1. Local Tool Execution
**Why**: Simpler, faster, more reliable for hackathon
- Tools run as Python functions in the FastAPI process
- No need to deploy separate Azure Functions
- Easier debugging and iteration

### 2. Dual Entry Points
**Why**: LLM for conversation, direct API for UI speed
- Deterministic endpoints (eligibility, documents) can be called:
  - **By the agent** during conversation (for contextual help)
  - **Directly by UI** (for fast, predictable results)

### 3. In-Memory Storage
**Why**: Simplicity for hackathon
- Conversations and profiles stored in memory
- **Production**: Replace with Redis/PostgreSQL

### 4. Bing Search Optional
**Why**: Provisioning can be slow
- Agent works perfectly with File Search only
- Bing adds live deadline lookups but is not required for core functionality

## Tool Execution Flow

```
User Message
    ↓
[Runner] Create response with agent reference
    ↓
[Azure] Agent processes with system prompt
    ↓
[Azure] Needs info? → Call function tool
    ↓
[Runner] Detect function_call in response
    ↓
[Runner] Execute tool locally via TOOL_DISPATCH
    ↓
[Runner] Send result back to agent
    ↓
[Azure] Agent incorporates result
    ↓
[Azure] Return text response or call another tool
    ↓
[Runner] Loop until no more function calls
    ↓
Return final response to user
```

## Environment Variables Summary

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `FOUNDRY_PROJECT_ENDPOINT` | ✅ Yes | Azure AI Foundry endpoint | - |
| `FOUNDRY_MODEL_DEPLOYMENT` | ✅ Yes | Model deployment name | - |
| `BING_CONNECTION_ID` | ⚠️ Optional | Bing connection for web search | None (File Search only) |

## Next Steps

1. **Add Scheme Data**: Place scheme PDFs/JSONs in a directory and upload via agent setup
2. **Test Endpoints**: Use `/docs` for interactive API testing
3. **Connect Frontend**: Point your React/Vue app to `http://localhost:8000`
4. **Deploy**: Use Azure Container Apps or App Service for production

## Troubleshooting

### "Missing FOUNDRY_PROJECT_ENDPOINT"
- Ensure `.env` file is in project root
- Check variable names match exactly

### "Azure authentication failed"
- Run `az login`
- Ensure you have access to the Azure AI Foundry project

### Tools not being called
- Check agent creation logs - tools should be listed
- Verify tool definitions match function signatures

### Bing Search not working
- Check if `BING_CONNECTION_ID` is set correctly
- Agent will still work with File Search only - this is expected

## Production Considerations

For production deployment:

1. **Database**: Replace in-memory storage with PostgreSQL/Redis
2. **Authentication**: Add JWT/OAuth for user auth
3. **Rate Limiting**: Add rate limiting middleware
4. **Logging**: Implement structured logging
5. **Monitoring**: Add health checks and metrics
6. **CORS**: Configure allowed origins properly
7. **Secrets**: Use Azure Key Vault for credentials
8. **Caching**: Cache scheme data and vector store IDs

## License

Part of the Sahayak Hackathon Project

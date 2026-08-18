# Sahayak Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Install Dependencies (1 min)
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Set Environment Variables (30 sec)
Your `.env` file already has the required variables:
```env
FOUNDRY_PROJECT_ENDPOINT=https://sahayak-christinhack.openai.azure.com/openai/v1
FOUNDRY_MODEL_DEPLOYMENT=gpt-5.4-mini
BING_CONNECTION_ID=your-bing-connection-id-here  # OPTIONAL
```

**Note**: `BING_CONNECTION_ID` is optional. Agent works perfectly without it!

### Step 3: Authenticate with Azure (30 sec)
```bash
az login
```

### Step 4: Start the Server (30 sec)
```bash
cd backend
python main.py
```

Server runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### Step 5: Test It! (2 min)
Open another terminal:
```bash
cd backend
python test_api.py
```

## 📡 Quick API Examples

### Chat with the Agent
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is PM-KISAN scheme?",
    "user_id": "demo_user"
  }'
```

### Check Eligibility (Fast Path)
```bash
curl -X POST http://localhost:8000/api/v1/eligibility/check \
  -H "Content-Type: application/json" \
  -d '{
    "scheme_id": "pm-kisan",
    "user_profile": {
      "full_name": "Test User",
      "age": 40,
      "gender": "Male",
      "mobile": "9876543210",
      "address": "Test Address",
      "district": "Test District",
      "state": "Uttar Pradesh",
      "pincode": "221001",
      "annual_family_income": 100000,
      "caste_category": "General",
      "is_farmer": true
    }
  }'
```

### Get Required Documents
```bash
curl http://localhost:8000/api/v1/schemes/pm-kisan/documents
```

## 🏗️ Architecture at a Glance

```
Frontend → FastAPI → Runner → Azure AI Agent
                ↓               ↓
            Direct Tools    File Search
            (Fast Path)     + Bing Search
                            + Function Tools
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI app entry point |
| `backend/foundry/agent.py` | Agent creation with all tools |
| `backend/foundry/prompts.py` | System prompt (strict rules) |
| `backend/foundry/runner.py` | Tool execution loop |
| `backend/tools/*.py` | 5 custom tools (eligibility, docs, etc.) |
| `backend/routers/*.py` | API endpoints |

## 🔧 Common Commands

### Start Server
```bash
cd backend
python main.py
```

### Run Tests
```bash
cd backend
python test_api.py
```

### Create Agent (One-time)
```bash
cd backend/foundry
python example_usage.py
```

### Validate Setup
```bash
cd backend
python setup.py
```

## 🎯 What's Already Implemented

✅ Agent with system prompt (strict rules)
✅ File Search tool (scheme knowledge base)
✅ Bing Search tool (optional, for live deadlines)
✅ 5 custom function tools:
   - check_eligibility
   - get_required_documents
   - explain_form_field
   - generate_application_package
   - check_application_status
✅ Tool execution loop (local Python functions)
✅ Session/conversation management
✅ All API endpoints (chat, profile, eligibility, docs, application, status)
✅ Dual entry points (LLM + direct API)

## ⚠️ Important Notes

### Bing Connection ID
- **Optional** - Agent works perfectly without it
- Only needed for live deadline web searches
- File Search provides all core functionality
- Can be added later without code changes

### In-Memory Storage
- Used for hackathon simplicity
- Conversations and profiles stored in memory
- For production: Replace with Redis/PostgreSQL

### Scheme Documents
- Need to upload scheme PDFs/JSONs to create vector store
- Run `backend/foundry/example_usage.py` with your documents directory
- One-time setup per agent version

## 🐛 Troubleshooting

### "Module not found"
```bash
pip install -r backend/requirements.txt
```

### "Missing FOUNDRY_PROJECT_ENDPOINT"
Check `.env` file exists in project root with the correct variables

### "Azure authentication failed"
```bash
az login
```

### Server won't start
Check if port 8000 is already in use:
```bash
lsof -i :8000
# Or change port in main.py
```

## 📚 Documentation

- **Full Backend Docs**: `backend/README.md`
- **Agent Setup Guide**: `backend/AGENT_SETUP.md`
- **Implementation Details**: `IMPLEMENTATION_COMPLETE.md`
- **API Docs (Interactive)**: `http://localhost:8000/docs` (when server is running)

## 🎉 You're Ready!

1. ✅ Environment configured
2. ✅ Dependencies installed
3. ✅ Server running
4. ✅ Tests passing

**Now build your frontend and connect to `http://localhost:8000`!**

Happy hacking! 🚀

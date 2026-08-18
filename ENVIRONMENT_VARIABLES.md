# Sahayak Environment Variables Reference

## 📋 Required Variables

These **MUST** be set in your `.env` file:

### 1. FOUNDRY_PROJECT_ENDPOINT
**Status**: ✅ Already configured in your `.env`
```env
FOUNDRY_PROJECT_ENDPOINT=https://sahayak-christinhack.openai.azure.com/openai/v1
```
**Purpose**: Azure AI Foundry project endpoint URL
**Where to find**: Azure AI Foundry portal → Project Settings
**Used by**: Agent creation, OpenAI client, all API operations

### 2. FOUNDRY_MODEL_DEPLOYMENT
**Status**: ✅ Already configured in your `.env`
```env
FOUNDRY_MODEL_DEPLOYMENT=gpt-5.4-mini
```
**Purpose**: Name of the deployed model to use
**Where to find**: Azure AI Foundry portal → Deployments
**Used by**: Agent creation, inference requests

## ⚠️ Optional Variables

These enhance functionality but are **NOT required**:

### 3. BING_CONNECTION_ID
**Status**: 📝 Needs to be configured (optional)
```env
BING_CONNECTION_ID=your-bing-connection-id-here
```
**Purpose**: Bing Search connection for live deadline grounding
**Where to find**: Azure AI Foundry → Connections → Bing Search
**Used by**: Web search tool for real-time information
**Default behavior if not set**: 
- Agent works perfectly with File Search only
- No web search capability
- All scheme information comes from uploaded documents
- **This is perfectly fine for the hackathon!**

**When to set it**:
- ✅ You have time to provision Bing connection
- ✅ You need live deadline lookups from the web
- ✅ You want current government announcements

**When to skip it**:
- ⚠️ Bing provisioning is taking too long
- ⚠️ You're in a hurry for hackathon demo
- ⚠️ File Search provides all needed information

## 🔍 How Variables Are Used

### In Agent Creation (`backend/foundry/agent.py`)
```python
# REQUIRED: Project connection
self.endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
self.model = os.environ.get("FOUNDRY_MODEL_DEPLOYMENT")

# OPTIONAL: Bing search
self.bing_connection_id = os.environ.get("BING_CONNECTION_ID")

if self.bing_connection_id:
    # Enable Bing grounding
else:
    # Continue with File Search only
```

### In Runner (`backend/foundry/runner.py`)
```python
self.endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
self.project = AIProjectClient(endpoint=self.endpoint, ...)
self.openai_client = self.project.get_openai_client()
```

### In Health Check (`backend/main.py`)
```python
@app.get("/health")
async def health_check():
    return {
        "environment": {
            "foundry_endpoint": os.environ.get("FOUNDRY_PROJECT_ENDPOINT"),
            "model": os.environ.get("FOUNDRY_MODEL_DEPLOYMENT"),
            "bing_enabled": bool(os.environ.get("BING_CONNECTION_ID"))
        }
    }
```

## ✅ Current Configuration Status

Your `.env` file currently has:

| Variable | Status | Value |
|----------|--------|-------|
| `FOUNDRY_PROJECT_ENDPOINT` | ✅ Configured | `https://sahayak-christinhack.openai.azure.com/openai/v1` |
| `FOUNDRY_MODEL_DEPLOYMENT` | ✅ Configured | `gpt-5.4-mini` |
| `BING_CONNECTION_ID` | ⚠️ Placeholder | `your-bing-connection-id-here` |

## 🎯 What You Need to Do

### For Hackathon (Minimum Viable):
1. ✅ `FOUNDRY_PROJECT_ENDPOINT` - Already set
2. ✅ `FOUNDRY_MODEL_DEPLOYMENT` - Already set
3. ⚠️ `BING_CONNECTION_ID` - **SKIP if blocked** (agent works without it)

### For Production (Recommended):
1. ✅ All three variables configured
2. ✅ Bing connection provisioned
3. ✅ Environment-specific `.env` files (dev, staging, prod)

## 🔧 How to Get Bing Connection ID

If you decide to enable Bing Search:

### Step 1: Azure Portal
1. Go to Azure AI Foundry portal
2. Navigate to your project: `sahayak-christinhack`

### Step 2: Create Bing Connection
1. Go to "Connections" section
2. Click "New Connection"
3. Select "Bing Search"
4. Follow the setup wizard

### Step 3: Copy Connection ID
1. Once created, open the Bing connection
2. Copy the "Connection ID"
3. Update `.env`:
   ```env
   BING_CONNECTION_ID=conn_abc123xyz...
   ```

### Step 4: Restart Server
```bash
cd backend
python main.py
```

## 🧪 Testing Configuration

### Check Environment Variables
```bash
cd backend
python setup.py
```

### Check Health Endpoint
```bash
curl http://localhost:8000/health
```

Response will show:
```json
{
  "environment": {
    "foundry_endpoint": "https://sahayak-christinhack.openai.azure.com/openai/v1",
    "model": "gpt-5.4-mini",
    "bing_enabled": false  // true if BING_CONNECTION_ID is set
  }
}
```

## 🚨 Common Issues

### Issue: "Missing FOUNDRY_PROJECT_ENDPOINT"
**Solution**: 
1. Ensure `.env` file exists in project root
2. Check variable name spelling (exact match)
3. No spaces around `=` sign
4. Restart server after changes

### Issue: "Azure authentication failed"
**Solution**:
```bash
az login
# Select the correct subscription
az account set --subscription "<your-subscription-id>"
```

### Issue: "Bing Search setup failed"
**Solution**:
- Check logs for specific error
- **Don't worry!** Agent continues with File Search only
- This is not a blocker for demo
- Can be added later without code changes

## 📝 Environment File Template

Copy this template to create your `.env`:

```env
# ============================================
# Sahayak Environment Configuration
# ============================================

# REQUIRED: Azure AI Foundry Configuration
FOUNDRY_PROJECT_ENDPOINT=https://sahayak-christinhack.openai.azure.com/openai/v1
FOUNDRY_MODEL_DEPLOYMENT=gpt-5.4-mini

# OPTIONAL: Bing Search (for live deadline grounding)
# Leave as placeholder if not using
BING_CONNECTION_ID=your-bing-connection-id-here

# ============================================
# Notes:
# - BING_CONNECTION_ID is optional
# - Agent works perfectly without Bing Search
# - File Search provides all core functionality
# ============================================
```

## 🎉 Summary

**You're already 2/2 (100%) configured for core functionality!**

- ✅ Required variables: 2/2 set
- ⚠️ Optional variables: 0/1 set (but that's okay!)

**The agent is ready to run without any additional configuration.**

The Bing Search is a nice-to-have enhancement, not a requirement. Your agent will work perfectly with just File Search for the hackathon demo!

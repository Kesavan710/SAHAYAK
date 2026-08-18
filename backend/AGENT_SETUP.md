# Sahayak Agent Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
cd backend/foundry
pip install -r requirements.txt
```

### 2. Configure Environment
Ensure your `.env` file has:
```
FOUNDRY_PROJECT_ENDPOINT=https://sahayak-christinhack.openai.azure.com/openai/v1
FOUNDRY_MODEL_DEPLOYMENT=gpt-5.4-mini
```

### 3. Authenticate with Azure
```bash
az login
```

### 4. Validate Setup
```bash
cd backend/foundry
python validate_setup.py
```

### 5. Prepare Scheme Documents
Place your government scheme PDFs/JSONs in a directory, e.g., `/data/schemes/`

### 6. Create the Agent

```python
from backend.foundry import create_sahayak_agent

# Create agent with scheme knowledge base
manager, agent = create_sahayak_agent(
    schemes_dir="/data/schemes",
    version_label="v1"
)

print(f"Agent ID: {agent.id}")
print(f"Vector Store ID: {manager.vector_store.id}")
```

## What Was Created

### 1. System Prompt (`prompts.py`)
Contains `SAHAYAK_SYSTEM_PROMPT` with strict rules:
- ✓ Never invent scheme information
- ✓ Always cite sources from knowledge base
- ✓ Never claim to submit applications  
- ✓ Ask one question at a time
- ✓ Provide clear, actionable next steps

### 2. Agent Definition (`agent.py`)
The `SahayakAgent` class provides:
- **Document Upload**: Upload scheme PDFs/JSONs to Azure
- **Vector Store Creation**: Create searchable knowledge base
- **Agent Creation**: Initialize agent with FileSearchTool
- **Convenience Methods**: Quick setup functions

### 3. File Search Tool
Automatically configured to:
- Search uploaded scheme documents
- Ground responses in actual scheme data
- Prevent hallucination by requiring citations

## Architecture

```
Sahayak Agent (gpt-5.4-mini)
│
├── System Prompt (SAHAYAK_SYSTEM_PROMPT)
│   ├── Never invent information
│   ├── Always cite sources
│   ├── Never claim submission
│   ├── Ask one question at a time
│   └── Be helpful & respectful
│
└── Tools
    └── FileSearchTool
        └── Vector Store: "sahayak-schemes"
            ├── Scheme Document 1 (PDF/JSON)
            ├── Scheme Document 2 (PDF/JSON)
            └── ...
```

## Usage Examples

### Example 1: Full Automated Setup
```python
from backend.foundry import create_sahayak_agent

manager, agent = create_sahayak_agent("/data/schemes", "v1")
```

### Example 2: Step-by-Step Control
```python
from backend.foundry import SahayakAgent

manager = SahayakAgent()
file_ids = manager.upload_scheme_documents([
    "/data/schemes/pm-kisan.pdf",
    "/data/schemes/ayushman-bharat.pdf",
])
manager.create_vector_store(file_ids)
agent = manager.create_agent(version_label="v1")
```

### Example 3: Reuse Existing Vector Store
```python
from backend.foundry import SahayakAgent

manager = SahayakAgent()
agent = manager.create_agent(
    vector_store_id="vs_existing_id",
    version_label="v2"
)
```

## Next Steps

1. **Test the Agent**: Use Azure AI Studio to test conversations
2. **Add More Tools**: Implement function calling for eligibility checks
3. **Build API**: Create FastAPI endpoints to interact with agent
4. **Frontend Integration**: Connect to your web/mobile interface

## Files Created

```
backend/foundry/
├── __init__.py           # Package initialization
├── prompts.py            # System prompt with strict rules
├── agent.py              # Main agent implementation
├── example_usage.py      # Usage examples
├── validate_setup.py     # Setup validation script
├── requirements.txt      # Python dependencies
└── README.md            # Detailed documentation
```

## Troubleshooting

### "Missing environment variables"
- Check your `.env` file in the project root
- Ensure `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL_DEPLOYMENT` are set

### "Azure authentication failed"
- Run `az login` to authenticate
- Verify you have access to the Azure AI Foundry project

### "No scheme documents found"
- Check the path to your schemes directory
- Ensure files are PDF or JSON format
- Verify file permissions

## References

- [Azure AI Projects SDK](https://learn.microsoft.com/azure/ai-studio/)
- [FileSearchTool Documentation](https://learn.microsoft.com/azure/ai-services/openai/how-to/file-search)
- See `backend/foundry/README.md` for detailed API documentation

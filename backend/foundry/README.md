# Sahayak Azure AI Foundry Agent

This module contains the Sahayak agent definition using Azure AI Foundry with file search capabilities for government scheme knowledge base.

## Components

### 1. `prompts.py`
Contains `SAHAYAK_SYSTEM_PROMPT` with strict rules:
- Never invent scheme information
- Always cite sources from knowledge base
- Never claim to submit applications
- Ask one question at a time
- Be helpful and respectful

### 2. `agent.py`
Main agent implementation with:
- `SahayakAgent` class for managing agent lifecycle
- Document upload functionality
- Vector store creation for scheme knowledge base
- Agent creation with FileSearchTool
- Convenience functions for quick setup

## Setup

### Prerequisites

1. Install required packages:
```bash
pip install azure-ai-projects azure-identity
```

2. Set environment variables in `.env`:
```
FOUNDRY_PROJECT_ENDPOINT=https://your-project.openai.azure.com/openai/v1
FOUNDRY_MODEL_DEPLOYMENT=gpt-4-mini
```

3. Authenticate with Azure:
```bash
az login
```

### Prepare Scheme Documents

Organize your government scheme documents (PDFs or JSONs) in a directory, for example:
```
/data/schemes/
  ├── pm-kisan.pdf
  ├── ayushman-bharat.pdf
  ├── pradhan-mantri-awas-yojana.pdf
  └── ...
```

## Usage

### Quick Setup (Recommended)

```python
from backend.foundry import create_sahayak_agent

# Create agent with all documents in a directory
manager, agent = create_sahayak_agent(
    schemes_dir="/data/schemes",
    version_label="v1"
)

print(f"Agent ID: {agent.id}")
print(f"Vector Store ID: {manager.vector_store.id}")
```

### Step-by-Step Setup

```python
from backend.foundry import SahayakAgent

# 1. Initialize manager
manager = SahayakAgent()

# 2. Upload scheme documents
scheme_files = [
    "/data/schemes/pm-kisan.pdf",
    "/data/schemes/ayushman-bharat.pdf",
]
file_ids = manager.upload_scheme_documents(scheme_files)

# 3. Create vector store for file search
vector_store = manager.create_vector_store(file_ids)

# 4. Create agent with file search tool
agent = manager.create_agent(version_label="v1")
```

### Reuse Existing Vector Store

```python
from backend.foundry import SahayakAgent

manager = SahayakAgent()

# Use an existing vector store ID
agent = manager.create_agent(
    vector_store_id="vs_xxxxxxxxxxxxx",
    version_label="v2"
)
```

## Agent Features

### File Search Tool
The agent includes Azure's FileSearchTool that:
- Searches the vector store of scheme documents
- Grounds responses in actual scheme information
- Prevents hallucination by requiring source citations

### System Prompt Rules
The agent follows strict guidelines:
1. **Never invent information** - Only use data from knowledge base
2. **Always cite sources** - Reference scheme names and documents
3. **Never claim submission** - Direct users to official portals
4. **One question at a time** - Gather eligibility info gradually
5. **Clear next steps** - Provide actionable guidance

## Architecture

```
┌─────────────────┐
│  Sahayak Agent  │
│   (gpt-4-mini)  │
└────────┬────────┘
         │
         ├─── System Prompt (SAHAYAK_SYSTEM_PROMPT)
         │
         └─── Tools:
              └─── FileSearchTool
                   └─── Vector Store (sahayak-schemes)
                        ├─── Scheme PDF 1
                        ├─── Scheme PDF 2
                        └─── ...
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `FOUNDRY_PROJECT_ENDPOINT` | Azure AI Foundry project endpoint | `https://project.openai.azure.com/openai/v1` |
| `FOUNDRY_MODEL_DEPLOYMENT` | Model deployment name | `gpt-4-mini` |

## Next Steps

After creating the agent, you can:
1. Add more tools (e.g., Code Interpreter, Function Calling)
2. Integrate with a web backend (FastAPI)
3. Build a conversational interface
4. Add eligibility checking functions

See `example_usage.py` for complete examples.

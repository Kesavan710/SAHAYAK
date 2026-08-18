import json
import os
from pathlib import Path
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

# ---------------------------------------------------------------------------
# Load mock schemes at startup
# ---------------------------------------------------------------------------
_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "schemes.json"

def _load_schemes() -> list[dict[str, Any]]:
    try:
        with _DATA_PATH.open(encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return []

_MOCK_SCHEMES: list[dict[str, Any]] = _load_schemes()


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

class SchemeSearchRequest(BaseModel):
    context: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------

@router.post("/search")
async def search_schemes(request: SchemeSearchRequest) -> list[dict[str, Any]]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if api_key:
        return await _ai_search(request.context)

    return _mock_search(request.context)


# ---------------------------------------------------------------------------
# Mock path — simple state filter
# ---------------------------------------------------------------------------

def _mock_search(context: dict[str, Any]) -> list[dict[str, Any]]:
    state = (context.get("state") or "").strip().lower()
    if not state:
        return _MOCK_SCHEMES

    results: list[dict[str, Any]] = []
    for scheme in _MOCK_SCHEMES:
        scheme_state = (scheme.get("state") or "all").lower()
        if scheme_state in ("all", state):
            results.append(scheme)
    return results


# ---------------------------------------------------------------------------
# AI path — uses RAG retriever
# ---------------------------------------------------------------------------

async def _ai_search(context: dict[str, Any]) -> list[dict[str, Any]]:
    from rag.retriever import SchemeRetriever

    retriever = SchemeRetriever()
    return retriever.retrieve(context)

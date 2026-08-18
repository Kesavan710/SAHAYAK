import os
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

class ConversationRequest(BaseModel):
    message: str
    context: dict[str, Any] = Field(default_factory=dict)
    history: list[dict[str, Any]] = Field(default_factory=list)


class ConversationResponse(BaseModel):
    reply: str
    step: str = ""
    options: list[str] = Field(default_factory=list)
    inputType: str = "chips"


# ---------------------------------------------------------------------------
# Mock responses — cycled when OPENAI_API_KEY is absent
# ---------------------------------------------------------------------------
_MOCK_RESPONSES: list[ConversationResponse] = [
    ConversationResponse(
        reply=(
            "Namaste! I'm Sahayak, your government scheme assistant. "
            "To help find the right schemes for you, could you tell me "
            "which state you live in?"
        ),
        step="state",
        options=["Karnataka", "Maharashtra", "Uttar Pradesh", "Tamil Nadu", "Other"],
        inputType="chips",
    ),
    ConversationResponse(
        reply=(
            "Thank you. Now, what type of disability do you have? "
            "This helps me match schemes that apply to your situation."
        ),
        step="disability_type",
        options=[
            "Locomotor / Physical",
            "Visual",
            "Hearing / Speech",
            "Intellectual / Mental",
            "Multiple Disabilities",
        ],
        inputType="chips",
    ),
    ConversationResponse(
        reply=(
            "Got it. Could you share your approximate annual household income? "
            "This is needed to check eligibility for some schemes."
        ),
        step="income",
        options=[
            "Below ₹1 lakh",
            "₹1–2.5 lakh",
            "₹2.5–5 lakh",
            "Above ₹5 lakh",
        ],
        inputType="chips",
    ),
]


# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------

@router.post("/chat", response_model=ConversationResponse)
async def chat(request: ConversationRequest) -> ConversationResponse:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if api_key:
        return await _ai_response(request, api_key)

    # Mock mode: cycle through the three canned responses based on message length
    index = len(request.message) % 3
    return _MOCK_RESPONSES[index]


# ---------------------------------------------------------------------------
# AI path
# ---------------------------------------------------------------------------

async def _ai_response(
    request: ConversationRequest, api_key: str
) -> ConversationResponse:
    from agents.sahayak_agent import SahayakAgent

    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    agent = SahayakAgent(model_name=model_name)
    reply = await agent.chat(message=request.message, history=request.history)
    return ConversationResponse(reply=reply, inputType="text")

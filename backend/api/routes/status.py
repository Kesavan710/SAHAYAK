from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

class StatusLookupRequest(BaseModel):
    registrationNumber: str


class StatusLookupResponse(BaseModel):
    found: bool
    status: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------

_DEMO_TIMELINE: list[dict[str, str]] = [
    {"label": "Submitted", "description": "Application received by the department"},
    {"label": "Document Verification", "description": "Documents under review by district office"},
    {"label": "Field Enquiry", "description": "Social worker visit scheduled"},
    {"label": "Approved", "description": "Application approved by district welfare officer"},
    {"label": "First Pension Disbursed", "description": "₹500 credited to your bank account"},
]


def _build_demo_status(registration_number: str) -> dict[str, Any]:
    return {
        "registrationNumber": registration_number,
        "schemeName": "Indira Gandhi National Disability Pension Scheme (IGNDPS)",
        "applicantName": "Demo Applicant",
        "currentStep": 2,
        "lastUpdated": "18 August 2026",
        "timeline": _DEMO_TIMELINE,
    }


# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------

@router.post("/lookup", response_model=StatusLookupResponse)
async def lookup_status(request: StatusLookupRequest) -> StatusLookupResponse:
    reg = request.registrationNumber.strip().upper()

    if reg.startswith("DEMO") or reg.startswith("KA"):
        return StatusLookupResponse(
            found=True,
            status=_build_demo_status(request.registrationNumber),
        )

    return StatusLookupResponse(found=False, status=None)

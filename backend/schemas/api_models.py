"""
API request/response models for the RPwD application endpoints.
These are what the frontend and agent layer consume — not the internal RPwDApplication directly.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from backend.schemas.rpwd_application import RPwDApplication
from backend.schemas.enums import ApplicationStatus


# ---------------------------------------------------------------------------
# /chat response extension (for RPwD flow)
# ---------------------------------------------------------------------------

class RPwDChatResponse(BaseModel):
    session_id: str
    assistant_message: str
    application: Optional[RPwDApplication] = None
    missing_fields: List[str] = []
    next_question: Optional[str] = None
    status: ApplicationStatus = ApplicationStatus.COLLECTING_INFORMATION
    audio_url: Optional[str] = None


# ---------------------------------------------------------------------------
# GET /applications/{application_id}
# ---------------------------------------------------------------------------

class ApplicationGetResponse(BaseModel):
    application_id: str
    status: ApplicationStatus
    application: RPwDApplication
    completion_percentage: int
    missing_fields: List[str]


# ---------------------------------------------------------------------------
# PATCH /applications/{application_id}
# ---------------------------------------------------------------------------

class ApplicationPatchRequest(BaseModel):
    updates: Dict[str, Any]   # nested partial updates, e.g. {"applicant": {"first_name": "Venu"}}


class ApplicationPatchResponse(BaseModel):
    application: RPwDApplication
    missing_fields: List[str]


# ---------------------------------------------------------------------------
# POST /applications/{application_id}/validate
# ---------------------------------------------------------------------------

class ValidationResponse(BaseModel):
    valid: bool
    missing_fields: List[str]
    invalid_fields: List[str]
    conditional_requirements: List[str]


# ---------------------------------------------------------------------------
# POST /applications/{application_id}/confirm
# ---------------------------------------------------------------------------

class ConfirmRequest(BaseModel):
    confirmed: bool
    application_place: str


class ConfirmResponse(BaseModel):
    status: ApplicationStatus
    ready_for_pdf: bool


# ---------------------------------------------------------------------------
# POST /applications/{application_id}/generate-pdf
# ---------------------------------------------------------------------------

class GeneratePdfResponse(BaseModel):
    application_id: str
    status: ApplicationStatus
    pdf_object_key: str
    download_url: str
    generated_at: str


# ---------------------------------------------------------------------------
# GET /applications/{application_id}/pdf
# ---------------------------------------------------------------------------

class GetPdfResponse(BaseModel):
    status: ApplicationStatus
    download_url: str
    expires_at: str

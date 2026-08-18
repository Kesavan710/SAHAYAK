"""
Sahayak FastAPI backend.

Exposes the API contract consumed by the React frontend.
All eligibility / document / application logic is handled by
deterministic tools — the Foundry agent layer (Person 1) sits
above this and routes tool calls here.

Scholarship flow endpoints:
  POST /chat                       → Foundry agent pass-through (stub until Person 1 connects)
  POST /profile                    → merge partial profile into session
  POST /eligibility/check          → run deterministic eligibility check
  GET  /schemes/{scheme_id}/documents → document list for a scheme + profile
  POST /application/package        → generate application package
  POST /status/check               → application status lookup

RPwD application flow endpoints (mounted under /applications):
  GET    /applications/{id}                → get application state
  PATCH  /applications/{id}               → merge field updates
  POST   /applications/{id}/validate      → run validation
  POST   /applications/{id}/confirm       → confirm declaration
  POST   /applications/{id}/generate-pdf  → generate preparation PDF
  GET    /applications/{id}/pdf           → get PDF download URL

Shared:
  GET  /downloads/{filename}       → serve generated files
  POST /tools/reload               → force reload scheme cache (dev only)
  GET  /health                     → health check
"""

import uuid
from pathlib import Path
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.models.user_profile import UserProfile
from backend.tools.eligibility import check_eligibility
from backend.tools.documents import get_required_documents, explain_form_field
from backend.tools.application import generate_application_package
from backend.tools.status import check_application_status
from backend.tools.scheme_loader import get_all_schemes, reload_schemes

# RPwD application engine
from backend.api.applications import router as applications_router
from backend.services import application_state as rpwd_state
from backend.schemas.rpwd_application import RPwDApplication
from backend.schemas.enums import ApplicationStatus

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Sahayak API",
    description="Voice-first government accessibility agent — application engine endpoints",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite + CRA defaults
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated application packages as static files
_DOWNLOADS_DIR = Path(__file__).resolve().parent.parent / "generated_packages"
_DOWNLOADS_DIR.mkdir(exist_ok=True)
app.mount("/downloads", StaticFiles(directory=str(_DOWNLOADS_DIR)), name="downloads")

# Register RPwD application routes
app.include_router(applications_router)

# ---------------------------------------------------------------------------
# In-memory session store
# Maps session_id → UserProfile (sufficient for a hackathon prototype)
# ---------------------------------------------------------------------------

_sessions: Dict[str, UserProfile] = {}


def _get_or_create_session(session_id: str) -> UserProfile:
    if session_id not in _sessions:
        _sessions[session_id] = UserProfile()
    return _sessions[session_id]


def _merge_profile(existing: UserProfile, update: UserProfile) -> UserProfile:
    """Merge non-None fields from update into existing profile."""
    existing_data = existing.dict()
    update_data = update.dict(exclude_none=True)
    existing_data.update(update_data)
    return UserProfile(**existing_data)


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    session_id: str
    message: str
    language: str = "en"  # "en" | "kn" | "hi"


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    audio_url: Optional[str] = None
    matched_schemes: Optional[list] = None
    missing_documents: Optional[list] = None
    awaiting_field: Optional[str] = None


class ProfileRequest(BaseModel):
    session_id: str
    profile: UserProfile


class ProfileResponse(BaseModel):
    session_id: str
    profile: UserProfile
    missing_fields: list


class EligibilityRequest(BaseModel):
    session_id: Optional[str] = None
    profile: UserProfile
    scheme_id: Optional[str] = None


class EligibilityResponse(BaseModel):
    matches: list


class DocumentsResponse(BaseModel):
    scheme_id: str
    scheme_name: str
    required_documents: list
    available_documents: list
    missing_documents: list
    official_url: str
    source_document: str


class ApplicationPackageRequest(BaseModel):
    session_id: str
    scheme_id: str


class ApplicationPackageResponse(BaseModel):
    scheme_id: str
    scheme_name: str
    package_id: str
    checklist: list
    application_data: dict
    download_url: str
    submission_instructions: str
    missing_profile_fields: list
    completeness_pct: int


class StatusRequest(BaseModel):
    registration_number: str


class StatusResponse(BaseModel):
    registration_number: str
    status: str
    last_updated: str
    source: str
    portal_url: str
    found: bool


class FormFieldRequest(BaseModel):
    field_name: str


# ---------------------------------------------------------------------------
# /chat  — stub until Person 1 wires in Foundry agent
# ---------------------------------------------------------------------------

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(req: ChatRequest):
    """
    Main conversation endpoint.
    Currently a stub that echoes back and runs eligibility if profile is sufficient.
    Person 1 will replace the body of this function with Foundry agent routing.
    """
    session_profile = _get_or_create_session(req.session_id)

    # Determine which field is still needed (drives single-question UX)
    missing = session_profile.missing_fields_for_eligibility()
    awaiting = missing[0] if missing else None

    # If profile is complete enough, run a quick eligibility check
    matched_schemes = None
    if not missing:
        results = check_eligibility(session_profile)
        eligible = [r for r in results if r.eligible]
        if eligible:
            matched_schemes = [
                {
                    "scheme_id": r.scheme_id,
                    "name": r.name,
                    "eligible": r.eligible,
                    "reasons": r.reasons,
                    "benefits": r.benefits,
                    "official_url": r.official_url,
                    "source_document": r.source_document,
                }
                for r in eligible
            ]

    return ChatResponse(
        session_id=req.session_id,
        reply=(
            "Sahayak agent stub — Person 1 will connect the Foundry agent here. "
            f"Received: '{req.message}'"
        ),
        matched_schemes=matched_schemes,
        awaiting_field=awaiting,
    )


# ---------------------------------------------------------------------------
# /profile
# ---------------------------------------------------------------------------

@app.post("/profile", response_model=ProfileResponse, tags=["Profile"])
async def update_profile(req: ProfileRequest):
    """
    Merge a partial profile update into the session's stored profile.
    The frontend sends individual field updates as the agent collects them.
    """
    existing = _get_or_create_session(req.session_id)
    merged = _merge_profile(existing, req.profile)
    _sessions[req.session_id] = merged

    return ProfileResponse(
        session_id=req.session_id,
        profile=merged,
        missing_fields=merged.missing_fields_for_eligibility(),
    )


# ---------------------------------------------------------------------------
# /eligibility/check
# ---------------------------------------------------------------------------

@app.post("/eligibility/check", response_model=EligibilityResponse, tags=["Eligibility"])
async def eligibility_check(req: EligibilityRequest):
    """
    Run deterministic eligibility check against all schemes (or a single scheme).
    Returns matches sorted eligible-first.
    """
    # If a session_id is provided, merge the request profile over the session's stored profile
    if req.session_id and req.session_id in _sessions:
        profile = _merge_profile(_sessions[req.session_id], req.profile)
    else:
        profile = req.profile

    results = check_eligibility(profile, req.scheme_id)

    matches = [
        {
            "scheme_id": r.scheme_id,
            "name": r.name,
            "eligible": r.eligible,
            "reasons": r.reasons,
            "benefits": r.benefits,
            "official_url": r.official_url,
            "source_document": r.source_document,
        }
        for r in results
    ]
    return EligibilityResponse(matches=matches)


# ---------------------------------------------------------------------------
# /schemes/{scheme_id}/documents
# ---------------------------------------------------------------------------

@app.get(
    "/schemes/{scheme_id}/documents",
    response_model=DocumentsResponse,
    tags=["Documents"],
)
async def scheme_documents(
    scheme_id: str,
    session_id: Optional[str] = Query(None),
):
    """
    Return required, available, and missing documents for a scheme.
    Cross-references the session profile's documents_available if session_id is supplied.
    """
    profile: Optional[UserProfile] = None
    if session_id and session_id in _sessions:
        profile = _sessions[session_id]

    try:
        result = get_required_documents(scheme_id, profile)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return DocumentsResponse(
        scheme_id=result.scheme_id,
        scheme_name=result.scheme_name,
        required_documents=result.required_documents,
        available_documents=result.available_documents,
        missing_documents=result.missing_documents,
        official_url=result.official_url,
        source_document=result.source_document,
    )


# ---------------------------------------------------------------------------
# /application/package
# ---------------------------------------------------------------------------

@app.post(
    "/application/package",
    response_model=ApplicationPackageResponse,
    tags=["Application"],
)
async def application_package(req: ApplicationPackageRequest):
    """
    Generate a structured application package for the session's current profile
    and the requested scheme. Does NOT submit anything to any government portal.
    """
    profile = _get_or_create_session(req.session_id)

    try:
        pkg = generate_application_package(profile, req.scheme_id, req.session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return ApplicationPackageResponse(
        scheme_id=pkg.scheme_id,
        scheme_name=pkg.scheme_name,
        package_id=pkg.package_id,
        checklist=[{"document": c.document, "status": c.status} for c in pkg.checklist],
        application_data=pkg.application_data,
        download_url=pkg.download_url,
        submission_instructions=pkg.submission_instructions,
        missing_profile_fields=pkg.missing_profile_fields,
        completeness_pct=pkg.completeness_pct,
    )


# ---------------------------------------------------------------------------
# /status/check
# ---------------------------------------------------------------------------

@app.post("/status/check", response_model=StatusResponse, tags=["Status"])
async def status_check(req: StatusRequest):
    """
    Look up application status by registration number.
    Returns portal URL for the citizen to check themselves.
    Never fabricates a status.
    """
    result = check_application_status(req.registration_number)
    return StatusResponse(
        registration_number=result.registration_number,
        status=result.status,
        last_updated=result.last_updated,
        source=result.source,
        portal_url=result.portal_url,
        found=result.found,
    )


# ---------------------------------------------------------------------------
# /tools/explain-field  (utility endpoint for the frontend)
# ---------------------------------------------------------------------------

@app.post("/tools/explain-field", tags=["Utilities"])
async def explain_field(req: FormFieldRequest):
    """Return a plain-language explanation of a document or form field."""
    return {"field_name": req.field_name, "explanation": explain_form_field(req.field_name)}


# ---------------------------------------------------------------------------
# /schemes  (convenience — list all loaded schemes)
# ---------------------------------------------------------------------------

@app.get("/schemes", tags=["Utilities"])
async def list_schemes():
    """List all schemes currently loaded from the knowledge base."""
    schemes = get_all_schemes()
    return {
        "count": len(schemes),
        "schemes": [
            {
                "scheme_id": s["scheme_id"],
                "name": s["name"],
                "state": s.get("state"),
                "income_limit": s.get("income_limit"),
                "min_disability_percentage": s.get("min_disability_percentage"),
                "education_levels": s.get("education_levels", []),
                "official_url": s.get("official_url"),
            }
            for s in schemes
        ],
    }


# ---------------------------------------------------------------------------
# /tools/reload  (dev only — force reload scheme cache after Person 2 adds files)
# ---------------------------------------------------------------------------

@app.post("/tools/reload", tags=["Dev"])
async def reload_knowledge_base():
    """Force reload the scheme knowledge base from disk. Use during development."""
    reload_schemes()
    schemes = get_all_schemes()
    return {"message": f"Reloaded {len(schemes)} schemes from knowledge base."}


# ---------------------------------------------------------------------------
# POST /applications  — create a new RPwD application session
# ---------------------------------------------------------------------------

class CreateApplicationRequest(BaseModel):
    session_id: Optional[str] = None


@app.post("/applications", tags=["RPwD Applications"])
async def create_application(req: CreateApplicationRequest):
    """
    Start a new RPwD application session.
    Returns the application_id used for all subsequent /applications/{id} calls.
    """
    session_id = req.session_id or str(uuid.uuid4())
    app_obj = rpwd_state.create_application(session_id)
    return {
        "application_id": app_obj.application_id,
        "session_id": session_id,
        "status": app_obj.status,
        "missing_fields": rpwd_state.get_missing_field_paths(app_obj),
        "next_question": rpwd_state.get_next_question(app_obj),
    }


# ---------------------------------------------------------------------------
# /health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["Health"])
async def health():
    schemes = get_all_schemes()
    return {
        "status": "ok",
        "schemes_loaded": len(schemes),
        "sessions_active": len(_sessions),
        "rpwd_applications": len(rpwd_state._store),
    }

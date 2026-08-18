"""
RPwD application API routes.

Implements the full API contract from the RPwD Shared Schema & API Blueprint (section 6):
  GET    /applications/{application_id}
  PATCH  /applications/{application_id}
  POST   /applications/{application_id}/validate
  POST   /applications/{application_id}/confirm
  POST   /applications/{application_id}/generate-pdf
  GET    /applications/{application_id}/pdf

The frontend must not call internal tools directly.
This router is the only public interface for RPwD application state.
"""

from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, HTTPException

from backend.schemas.api_models import (
    ApplicationGetResponse,
    ApplicationPatchRequest,
    ApplicationPatchResponse,
    ValidationResponse,
    ConfirmRequest,
    ConfirmResponse,
    GeneratePdfResponse,
    GetPdfResponse,
)
from backend.schemas.enums import ApplicationStatus
from backend.services import application_state as state_svc
from backend.services.validation import validate_application
from backend.services.pdf_generator import generate_application_pdf

router = APIRouter(prefix="/applications", tags=["RPwD Applications"])

# ─────────────────────────────────────────────────────────────────────────────
# Shared lookup helper
# ─────────────────────────────────────────────────────────────────────────────

def _get_or_404(application_id: str):
    app = state_svc.get_application(application_id)
    if app is None:
        raise HTTPException(
            status_code=404,
            detail=f"Application '{application_id}' not found."
        )
    return app


# ─────────────────────────────────────────────────────────────────────────────
# GET /applications/{application_id}
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/{application_id}", response_model=ApplicationGetResponse)
async def get_application(application_id: str):
    """
    Return the current state of an RPwD application including
    completion percentage and list of missing required fields.
    """
    app = _get_or_404(application_id)
    return ApplicationGetResponse(
        application_id=app.application_id,
        status=app.status,
        application=app,
        completion_percentage=app.metadata.completion_percentage,
        missing_fields=state_svc.get_missing_field_paths(app),
    )


# ─────────────────────────────────────────────────────────────────────────────
# PATCH /applications/{application_id}
# ─────────────────────────────────────────────────────────────────────────────

@router.patch("/{application_id}", response_model=ApplicationPatchResponse)
async def patch_application(application_id: str, req: ApplicationPatchRequest):
    """
    Merge a partial field update into the canonical RPwDApplication.
    All merging logic is deterministic — the agent may extract values
    but this endpoint owns state.

    Example body:
      {"updates": {"education_and_occupation": {"educational_status": "Graduate"}}}
    """
    app = _get_or_404(application_id)

    # Block updates on a confirmed/generated application
    if app.status in (ApplicationStatus.PDF_GENERATED,):
        raise HTTPException(
            status_code=409,
            detail="Application PDF has already been generated. No further updates are allowed."
        )

    updated = state_svc.merge_updates(app, req.updates)

    return ApplicationPatchResponse(
        application=updated,
        missing_fields=state_svc.get_missing_field_paths(updated),
    )


# ─────────────────────────────────────────────────────────────────────────────
# POST /applications/{application_id}/validate
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/{application_id}/validate", response_model=ValidationResponse)
async def validate_app(application_id: str):
    """
    Run deterministic validation on the current application state.
    Returns which fields are missing, which have invalid values,
    and which conditional requirements are active.
    """
    app = _get_or_404(application_id)
    result = validate_application(app)

    return ValidationResponse(
        valid=result.valid,
        missing_fields=result.missing_fields,
        invalid_fields=result.invalid_fields,
        conditional_requirements=result.conditional_requirements,
    )


# ─────────────────────────────────────────────────────────────────────────────
# POST /applications/{application_id}/confirm
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/{application_id}/confirm", response_model=ConfirmResponse)
async def confirm_application(application_id: str, req: ConfirmRequest):
    """
    Record the applicant's declaration confirmation.
    Requires all required fields to be complete — validation is enforced here.
    PDF generation is unlocked only after confirmation.
    """
    app = _get_or_404(application_id)

    if not req.confirmed:
        raise HTTPException(
            status_code=400,
            detail="confirmed must be true to confirm the declaration."
        )

    try:
        confirmed_app = state_svc.confirm_application(app, req.application_place)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return ConfirmResponse(
        status=confirmed_app.status,
        ready_for_pdf=confirmed_app.status == ApplicationStatus.CONFIRMED,
    )


# ─────────────────────────────────────────────────────────────────────────────
# POST /applications/{application_id}/generate-pdf
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/{application_id}/generate-pdf", response_model=GeneratePdfResponse)
async def generate_pdf(application_id: str):
    """
    Generate the RPwD application-preparation PDF.
    Only allowed after the applicant has confirmed the declaration.
    The PDF is an application-preparation summary — Sahayak does NOT submit
    anything to the government.
    """
    app = _get_or_404(application_id)

    try:
        result = generate_application_pdf(app)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Advance status to pdf_generated
    app.status = ApplicationStatus.PDF_GENERATED
    state_svc.save_application(app)

    return GeneratePdfResponse(
        application_id=result.application_id,
        status=ApplicationStatus.PDF_GENERATED,
        pdf_object_key=result.pdf_object_key,
        download_url=result.download_url,
        generated_at=result.generated_at,
    )


# ─────────────────────────────────────────────────────────────────────────────
# GET /applications/{application_id}/pdf
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/{application_id}/pdf", response_model=GetPdfResponse)
async def get_pdf(application_id: str):
    """
    Return the download URL for a previously generated PDF.
    For the prototype, the URL does not expire (no S3 signed URLs yet).
    Person 1 wires real S3 signed URLs here.
    """
    app = _get_or_404(application_id)

    if app.status != ApplicationStatus.PDF_GENERATED:
        raise HTTPException(
            status_code=404,
            detail=(
                "No PDF has been generated for this application yet. "
                f"Current status: {app.status}."
            )
        )

    # Prototype: reconstruct download URL from application_id
    # In production: retrieve signed URL from S3 via storage service
    expires_at = (
        datetime.now(timezone.utc) + timedelta(hours=24)
    ).isoformat()

    # Find the most recent generated file for this application
    from pathlib import Path
    pdf_dir = Path(__file__).resolve().parents[2] / "generated_packages"
    safe_id = application_id[:8]
    candidates = sorted(
        list(pdf_dir.glob(f"rpwd_{safe_id}_*.pdf")) +
        list(pdf_dir.glob(f"rpwd_{safe_id}_*.json")),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not candidates:
        raise HTTPException(
            status_code=404,
            detail="PDF file not found on server. Try generating again."
        )

    return GetPdfResponse(
        status=ApplicationStatus.PDF_GENERATED,
        download_url=f"/downloads/{candidates[0].name}",
        expires_at=expires_at,
    )

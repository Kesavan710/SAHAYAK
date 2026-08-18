"""
Application package tool.

Generates a structured, downloadable application package for a citizen
who is ready to apply for a scheme.

IMPORTANT: This tool prepares an application package — it does NOT submit
anything to a government portal. The citizen must complete authentication,
OTP, and CAPTCHA steps themselves on the official portal.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field

from backend.models.user_profile import UserProfile, FIELD_LABELS
from backend.tools.scheme_loader import get_scheme_by_id
from backend.tools.documents import get_required_documents


# ---------------------------------------------------------------------------
# Output directory for generated packages
# ---------------------------------------------------------------------------

_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "generated_packages"
_OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class ChecklistItem:
    document: str
    status: str  # "available" | "missing"


@dataclass
class ApplicationPackage:
    scheme_id: str
    scheme_name: str
    package_id: str
    generated_at: str
    checklist: List[ChecklistItem]
    application_data: Dict[str, str]   # human-readable label → value
    download_url: str
    submission_instructions: str
    missing_profile_fields: List[str]
    completeness_pct: int              # 0–100, for the frontend progress bar


# ---------------------------------------------------------------------------
# Submission instruction builder (data-driven per scheme)
# ---------------------------------------------------------------------------

def _build_submission_instructions(scheme: dict, profile: UserProfile) -> str:
    portal = scheme.get("application_portal", scheme.get("official_url", "the official portal"))
    deadline = scheme.get("deadline_note", "Check the official portal for current deadlines.")
    lines = [
        f"HOW TO SUBMIT — {scheme['name']}",
        "",
        f"1. Visit the application portal: {portal}",
        "2. Register or log in with your Aadhaar number.",
        "   ⚠  Sahayak will never ask for or store your Aadhaar OTP or password.",
        "      You must complete this authentication step yourself.",
        "3. Complete the CAPTCHA verification on the portal yourself.",
        "4. Fill in the application form using the details in this package.",
        "5. Upload scanned copies of each document in the checklist.",
        "6. Submit the form and note down your application/registration number.",
        "7. Keep a copy of the acknowledgement receipt.",
        "",
        f"Deadline note: {deadline}",
        "",
        "IMPORTANT: Sahayak has NOT submitted this application on your behalf.",
        "Submission status can only be confirmed by the government portal itself.",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Application data builder
# ---------------------------------------------------------------------------

def _build_application_data(profile: UserProfile) -> Dict[str, str]:
    """
    Map profile fields to human-readable labels and string values.
    Only includes fields that are set — empty fields are listed in missing_profile_fields.
    """
    data: Dict[str, str] = {}
    raw = profile.dict(exclude_none=True)

    for field_key, value in raw.items():
        label = FIELD_LABELS.get(field_key, field_key.replace("_", " ").title())
        if field_key == "annual_family_income":
            data[label] = f"₹{int(value):,}"
        elif field_key == "disability_percentage":
            data[label] = f"{value}%"
        elif field_key == "documents_available":
            data[label] = ", ".join(value) if value else "None listed"
        else:
            data[label] = str(value)

    return data


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_application_package(
    profile: UserProfile,
    scheme_id: str,
    session_id: Optional[str] = None,
) -> ApplicationPackage:
    """
    Generate a structured application package for a citizen + scheme.

    Args:
        profile:    The citizen's profile (should be as complete as possible).
        scheme_id:  The target scheme.
        session_id: Optional session identifier for the download filename.

    Returns:
        ApplicationPackage with checklist, application_data, download_url,
        and submission instructions.

    Raises:
        ValueError: If scheme_id is not found.
    """
    scheme = get_scheme_by_id(scheme_id)
    if scheme is None:
        raise ValueError(f"Scheme '{scheme_id}' not found in knowledge base.")

    # Build document checklist
    doc_result = get_required_documents(scheme_id, profile)
    checklist = [
        ChecklistItem(document=doc, status="available")
        for doc in doc_result.available_documents
    ] + [
        ChecklistItem(document=doc, status="missing")
        for doc in doc_result.missing_documents
    ]

    # Build application data dict
    application_data = _build_application_data(profile)

    # Missing profile fields
    missing_fields = profile.missing_fields_for_application()

    # Completeness: profile fields + documents
    total_docs = len(checklist)
    available_docs = sum(1 for c in checklist if c.status == "available")
    total_profile = len(FIELD_LABELS) - 1  # exclude documents_available key
    filled_profile = len([v for k, v in profile.dict().items()
                          if v is not None and k != "documents_available"])
    completeness = int(
        ((available_docs + filled_profile) / max(total_docs + total_profile, 1)) * 100
    )

    # Submission instructions
    instructions = _build_submission_instructions(scheme, profile)

    # Persist package as JSON
    package_id = str(uuid.uuid4())[:8]
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    filename = f"package_{scheme_id}_{session_id or 'session'}_{timestamp}_{package_id}.json"
    output_path = _OUTPUT_DIR / filename

    package_payload = {
        "package_id": package_id,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "scheme_id": scheme_id,
        "scheme_name": scheme["name"],
        "checklist": [{"document": c.document, "status": c.status} for c in checklist],
        "application_data": application_data,
        "submission_instructions": instructions,
        "missing_profile_fields": missing_fields,
        "completeness_pct": completeness,
        "official_url": scheme.get("official_url", ""),
        "source_document": scheme.get("source_document", ""),
        "disclaimer": (
            "Sahayak has NOT submitted this application. "
            "You must complete government authentication, OTP, and CAPTCHA steps yourself."
        ),
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(package_payload, f, ensure_ascii=False, indent=2)

    # The download URL will be served by FastAPI's static files route
    download_url = f"/downloads/{filename}"

    return ApplicationPackage(
        scheme_id=scheme_id,
        scheme_name=scheme["name"],
        package_id=package_id,
        generated_at=package_payload["generated_at"],
        checklist=checklist,
        application_data=application_data,
        download_url=download_url,
        submission_instructions=instructions,
        missing_profile_fields=missing_fields,
        completeness_pct=completeness,
    )

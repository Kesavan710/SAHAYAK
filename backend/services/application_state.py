"""
Application state service.

Owns:
  - In-memory application store (keyed by application_id)
  - Merge logic: partial dict updates → canonical RPwDApplication
  - Missing-field detection with conditional rules
  - Completion percentage calculation
  - Status transitions

The LLM extracts values; this module owns merging and state tracking.
"""

from __future__ import annotations

import copy
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from backend.schemas.rpwd_application import (
    RPwDApplication, Applicant, Addresses, Address,
    EducationAndOccupation, Identification, Disability,
    PreviousApplication, PreviousCertificate, DocumentAvailability,
    Guardian, Declaration, Metadata,
)
from backend.schemas.enums import ApplicationStatus, OnsetType


# ---------------------------------------------------------------------------
# In-memory store  (application_id → RPwDApplication)
# ---------------------------------------------------------------------------

_store: Dict[str, RPwDApplication] = {}


def create_application(session_id: str) -> RPwDApplication:
    app = RPwDApplication(session_id=session_id, status=ApplicationStatus.DRAFT)
    _store[app.application_id] = app
    return app


def get_application(application_id: str) -> Optional[RPwDApplication]:
    return _store.get(application_id)


def get_application_by_session(session_id: str) -> Optional[RPwDApplication]:
    """Return the most recent application for a session, or None."""
    matches = [a for a in _store.values() if a.session_id == session_id]
    if not matches:
        return None
    return sorted(matches, key=lambda a: a.metadata.created_at, reverse=True)[0]


def save_application(app: RPwDApplication) -> RPwDApplication:
    app.metadata.updated_at = datetime.utcnow().isoformat() + "Z"
    app.metadata.completion_percentage = calculate_completion(app)
    _store[app.application_id] = app
    return app


# ---------------------------------------------------------------------------
# Deep merge helper
# ---------------------------------------------------------------------------

def _deep_merge(base: dict, updates: dict) -> dict:
    """
    Recursively merge updates into base.
    None values in updates are ignored — they don't overwrite existing data.
    """
    result = copy.deepcopy(base)
    for key, value in updates.items():
        if value is None:
            continue  # never overwrite existing data with None
        if (
            isinstance(value, dict)
            and key in result
            and isinstance(result[key], dict)
        ):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def merge_updates(
    app: RPwDApplication,
    updates: dict,
) -> RPwDApplication:
    """
    Merge a partial update dict (as received from agent extraction or PATCH request)
    into the canonical RPwDApplication and return the updated object.

    The update dict uses the same nested structure as RPwDApplication:
      {"applicant": {"first_name": "Venu", "age": 21}, "disability": {"onset_type": "from_birth"}}
    """
    current = app.model_dump()
    merged = _deep_merge(current, updates)

    # Re-parse through Pydantic to trigger all validators and normalisers
    updated_app = RPwDApplication(**merged)

    # Preserve system-managed fields
    updated_app.application_id = app.application_id
    updated_app.session_id = app.session_id
    updated_app.metadata.created_at = app.metadata.created_at

    # Advance status if appropriate
    updated_app.status = _compute_status(updated_app)

    return save_application(updated_app)


# ---------------------------------------------------------------------------
# Required field definitions
# ---------------------------------------------------------------------------

# (dot-path label, human-readable question the agent should ask)
_ALWAYS_REQUIRED: List[Tuple[str, str]] = [
    ("applicant.first_name",                     "What is your first name?"),
    ("applicant.father_name",                    "What is your father's name?"),
    ("applicant.mother_name",                    "What is your mother's name?"),
    ("applicant.date_of_birth",                  "What is your date of birth?"),
    ("applicant.gender",                         "What is your gender?"),
    ("addresses.permanent_address.address_line", "What is your permanent address (street/house)?"),
    ("addresses.permanent_address.village_town_city", "Which city or village do you live in?"),
    ("addresses.permanent_address.district",     "Which district is your permanent address in?"),
    ("addresses.permanent_address.state",        "Which state is your permanent address in?"),
    ("addresses.permanent_address.pin_code",     "What is the PIN code for your permanent address?"),
    ("addresses.same_as_permanent",              None),   # boolean — always has a value (False default)
    ("education_and_occupation.educational_status", "What is your highest level of education?"),
    ("education_and_occupation.occupation",      "What is your current occupation?"),
    ("disability.disability_type",               "What type of disability do you have?"),
    ("disability.onset_type",                    "Was your disability present from birth, or did it occur later?"),
    ("previous_application.previously_applied",  "Have you applied for a disability certificate before?"),
    ("previous_certificate.previously_issued",   "Has a disability certificate ever been issued to you before?"),
    ("documents.passport_photos_available",      "Do you have passport-size photographs available?"),
    ("documents.residence_proof",                "What document do you have as proof of residence (e.g. Aadhaar, ration card, utility bill)?"),
    ("guardian.has_guardian",                    "Do you have a guardian or representative who will assist you?"),
    ("declaration.application_place",            "In which city or place are you filling this application?"),
]

# Conditional fields — (condition_fn, dot-path, question)
# condition_fn takes the RPwDApplication and returns True if this field is required
_CONDITIONAL: List[Tuple, str, str] = []  # populated below via helper


def _add_conditional(condition_fn, field_path: str, question: str):
    _CONDITIONAL.append((condition_fn, field_path, question))


_add_conditional(
    lambda a: a.addresses.same_as_permanent is False,
    "addresses.communication_address.address_line",
    "What is your communication address (if different from permanent address)?"
)
_add_conditional(
    lambda a: a.disability.onset_type == OnsetType.SINCE_YEAR or
               a.disability.onset_type == "since_year",
    "disability.onset_year",
    "In which year did your disability occur or was it diagnosed?"
)
_add_conditional(
    lambda a: a.previous_application.previously_applied is True,
    "previous_application.authority",
    "Which authority or office did you previously apply to?"
)
_add_conditional(
    lambda a: a.previous_application.previously_applied is True,
    "previous_application.district",
    "In which district did you previously apply?"
)
_add_conditional(
    lambda a: a.previous_certificate.previously_issued is True,
    "previous_certificate.certificate_available",
    "Do you still have the previously issued certificate available?"
)
_add_conditional(
    lambda a: a.guardian.has_guardian is True,
    "guardian.full_name",
    "What is your guardian's full name?"
)
_add_conditional(
    lambda a: a.guardian.has_guardian is True,
    "guardian.relationship_to_applicant",
    "What is the guardian's relationship to you?"
)
_add_conditional(
    lambda a: a.guardian.has_guardian is True,
    "guardian.contact_number",
    "What is the guardian's contact number?"
)


# ---------------------------------------------------------------------------
# Missing field detection (with conditional rules applied)
# ---------------------------------------------------------------------------

def _get_nested(obj: RPwDApplication, dot_path: str):
    """Traverse dot-path on a Pydantic model and return the leaf value."""
    parts = dot_path.split(".")
    current = obj
    for part in parts:
        if current is None:
            return None
        if isinstance(current, dict):
            current = current.get(part)
        else:
            current = getattr(current, part, None)
    return current


def get_missing_fields(app: RPwDApplication) -> List[Tuple[str, str]]:
    """
    Return list of (field_path, question) for fields that are required but not yet filled.
    Applies all four conditional rules from the blueprint:
      - same_as_permanent=True → skip communication_address
      - previously_applied=False → skip authority/district/result
      - onset_type=from_birth → skip onset_year
      - has_guardian=False → skip guardian details
    """
    missing: List[Tuple[str, str]] = []

    for field_path, question in _ALWAYS_REQUIRED:
        if question is None:
            continue  # boolean fields with defaults are never "missing"
        value = _get_nested(app, field_path)
        if value is None or value == "":
            missing.append((field_path, question))

    for condition_fn, field_path, question in _CONDITIONAL:
        try:
            if condition_fn(app):
                value = _get_nested(app, field_path)
                if value is None or value == "":
                    missing.append((field_path, question))
        except Exception:
            continue  # condition evaluation failed — skip safely

    return missing


def get_next_question(app: RPwDApplication) -> Optional[str]:
    """Return the single most relevant next question, or None if complete."""
    missing = get_missing_fields(app)
    return missing[0][1] if missing else None


def get_missing_field_paths(app: RPwDApplication) -> List[str]:
    """Return just the field paths (no questions) — used by API responses."""
    return [path for path, _ in get_missing_fields(app)]


# ---------------------------------------------------------------------------
# Completion percentage
# ---------------------------------------------------------------------------

def calculate_completion(app: RPwDApplication) -> int:
    """
    Calculate what percentage of required fields are filled.
    Conditional fields that don't apply are counted as complete.
    """
    always_total = len([q for _, q in _ALWAYS_REQUIRED if q is not None])
    always_filled = always_total - len([
        p for p, q in _ALWAYS_REQUIRED
        if q is not None and (_get_nested(app, p) is None or _get_nested(app, p) == "")
    ])

    # For conditionals: count applicable ones and how many are filled
    conditional_applicable = 0
    conditional_filled = 0
    for condition_fn, field_path, _ in _CONDITIONAL:
        try:
            if condition_fn(app):
                conditional_applicable += 1
                val = _get_nested(app, field_path)
                if val is not None and val != "":
                    conditional_filled += 1
        except Exception:
            continue

    total = always_total + conditional_applicable
    filled = always_filled + conditional_filled

    return int((filled / total) * 100) if total > 0 else 0


# ---------------------------------------------------------------------------
# Status transitions
# ---------------------------------------------------------------------------

def _compute_status(app: RPwDApplication) -> ApplicationStatus:
    """Advance status based on current data state. Never go backwards."""
    if app.status in (ApplicationStatus.PDF_GENERATED, ApplicationStatus.ERROR):
        return app.status
    if app.status == ApplicationStatus.CONFIRMED:
        return ApplicationStatus.CONFIRMED

    missing = get_missing_fields(app)
    if not missing and not app.declaration.confirmed:
        return ApplicationStatus.READY_FOR_REVIEW
    if not missing and app.declaration.confirmed:
        return ApplicationStatus.CONFIRMED
    if any(_get_nested(app, p) is not None for p, _ in _ALWAYS_REQUIRED if _ is not None):
        return ApplicationStatus.COLLECTING_INFORMATION
    return ApplicationStatus.DRAFT


def confirm_application(
    app: RPwDApplication,
    application_place: str,
) -> RPwDApplication:
    """
    Mark the application as confirmed by the user.
    Requires all required fields to be complete first.
    """
    from backend.services.validation import validate_application
    result = validate_application(app)
    if not result.valid:
        raise ValueError(
            f"Cannot confirm — required fields missing: {result.missing_fields}"
        )
    app.declaration.confirmed = True
    app.declaration.application_place = application_place
    app.declaration.generated_date = datetime.utcnow().isoformat() + "Z"
    app.status = ApplicationStatus.CONFIRMED
    return save_application(app)

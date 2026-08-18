"""
Deterministic validation service for RPwDApplication.

Rule: the agent may suggest/extract values.
      Validation belongs entirely to this deterministic code.

validate_application() is the single entry point called before:
  - advancing status to ready_for_review
  - allowing declaration confirmation
  - allowing PDF generation
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List

from backend.schemas.rpwd_application import RPwDApplication
from backend.schemas.enums import OnsetType
from backend.services.application_state import (
    get_missing_fields,
    _get_nested,
)


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class ValidationResult:
    valid: bool
    missing_fields: List[str] = field(default_factory=list)
    invalid_fields: List[str] = field(default_factory=list)
    conditional_requirements: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Individual field validators
# ---------------------------------------------------------------------------

def _validate_dob(app: RPwDApplication, errors: List[str], invalid: List[str]):
    dob = app.applicant.date_of_birth
    if dob is None:
        return
    try:
        from datetime import datetime, date
        parsed = datetime.strptime(dob, "%Y-%m-%d").date()
        if parsed > date.today():
            errors.append("Date of birth cannot be in the future.")
            invalid.append("applicant.date_of_birth")
        if parsed.year < 1900:
            errors.append("Date of birth year is not realistic (before 1900).")
            invalid.append("applicant.date_of_birth")
    except ValueError:
        errors.append(
            f"Date of birth '{dob}' is not in a recognised format (expected YYYY-MM-DD)."
        )
        invalid.append("applicant.date_of_birth")


def _validate_pin_code(app: RPwDApplication, errors: List[str], invalid: List[str]):
    pin = _get_nested(app, "addresses.permanent_address.pin_code")
    if pin is None:
        return
    if not re.fullmatch(r"\d{6}", str(pin).strip()):
        errors.append(
            f"PIN code '{pin}' is not valid — must be exactly 6 digits."
        )
        invalid.append("addresses.permanent_address.pin_code")


def _validate_onset_year(app: RPwDApplication, errors: List[str], invalid: List[str]):
    if app.disability.onset_type not in (OnsetType.SINCE_YEAR, "since_year"):
        return
    year = app.disability.onset_year
    if year is None:
        return  # missing check handled by get_missing_fields
    from datetime import date
    current_year = date.today().year
    if not (1900 <= year <= current_year):
        errors.append(
            f"Onset year {year} is not realistic. "
            f"Expected a year between 1900 and {current_year}."
        )
        invalid.append("disability.onset_year")


def _validate_contact_number(app: RPwDApplication, errors: List[str], invalid: List[str]):
    if not app.guardian.has_guardian:
        return
    contact = app.guardian.contact_number
    if contact is None:
        return  # missing check handled by get_missing_fields
    # Accept Indian mobile numbers: optional +91 prefix, then 10 digits starting with 6-9
    cleaned = re.sub(r"[\s\-\(\)]", "", str(contact))
    if cleaned.startswith("+91"):
        cleaned = cleaned[3:]
    if cleaned.startswith("91") and len(cleaned) == 12:
        cleaned = cleaned[2:]
    if not re.fullmatch(r"[6-9]\d{9}", cleaned):
        errors.append(
            f"Guardian contact number '{contact}' does not appear to be a valid "
            "Indian mobile number."
        )
        invalid.append("guardian.contact_number")


def _validate_declaration(app: RPwDApplication, errors: List[str], invalid: List[str]):
    """Declaration can only be confirmed if all required fields are present."""
    if app.declaration.confirmed:
        missing = get_missing_fields(app)
        if missing:
            paths = [p for p, _ in missing]
            errors.append(
                "Declaration cannot be confirmed while required fields are missing: "
                + ", ".join(paths)
            )
            invalid.append("declaration.confirmed")


def _collect_conditional_requirements(app: RPwDApplication) -> List[str]:
    """
    Return human-readable descriptions of which conditional rules are currently active.
    Used by the API response to help the frontend show context.
    """
    notes = []
    if app.addresses.same_as_permanent is False:
        notes.append(
            "Communication address is required because it differs from permanent address."
        )
    if app.disability.onset_type in (OnsetType.SINCE_YEAR, "since_year"):
        notes.append("Onset year is required because disability did not occur from birth.")
    if app.previous_application.previously_applied is True:
        notes.append(
            "Previous application authority, district, and result are required "
            "because you have applied before."
        )
    if app.previous_certificate.previously_issued is True:
        notes.append(
            "Certificate availability is required because a certificate was previously issued."
        )
    if app.guardian.has_guardian is True:
        notes.append(
            "Guardian details (name, relationship, contact) are required "
            "because a guardian is present."
        )
    return notes


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate_application(app: RPwDApplication) -> ValidationResult:
    """
    Run all deterministic validation checks on an RPwDApplication.

    Returns a ValidationResult indicating:
      - valid: True only if no required fields are missing and no field values are invalid
      - missing_fields: dot-path list of unfilled required/conditional fields
      - invalid_fields: dot-path list of fields with bad values
      - conditional_requirements: active conditional rules as human-readable strings
      - errors: plain-language error messages for the agent/user
    """
    errors: List[str] = []
    invalid: List[str] = []

    # Run field-level validators
    _validate_dob(app, errors, invalid)
    _validate_pin_code(app, errors, invalid)
    _validate_onset_year(app, errors, invalid)
    _validate_contact_number(app, errors, invalid)
    _validate_declaration(app, errors, invalid)

    # Get missing required fields
    missing_pairs = get_missing_fields(app)
    missing_paths = [p for p, _ in missing_pairs]

    # Collect active conditional rules
    conditional = _collect_conditional_requirements(app)

    valid = len(missing_paths) == 0 and len(invalid) == 0

    return ValidationResult(
        valid=valid,
        missing_fields=missing_paths,
        invalid_fields=invalid,
        conditional_requirements=conditional,
        errors=errors,
    )

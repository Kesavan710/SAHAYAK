"""
Eligibility tool — deterministic, auditable, no LLM guessing.

The LLM explains eligibility to the user.
This code IS the source of truth for eligibility thresholds.

check_eligibility(profile, scheme_id?) is the only public entry point
called by the FastAPI layer and by the Foundry agent tool routing.
"""

from typing import List, Optional
from dataclasses import dataclass, field

from backend.models.user_profile import UserProfile
from backend.tools.scheme_loader import get_all_schemes, get_scheme_by_id


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class CriterionResult:
    criterion: str          # human-readable criterion name
    passed: bool
    detail: str             # plain-language explanation surfaced to the LLM


@dataclass
class SchemeMatch:
    scheme_id: str
    name: str
    eligible: bool
    reasons: List[str]          # plain-language pass/fail reasons
    benefits: List[str]
    official_url: str
    source_document: str
    matched_criteria: List[CriterionResult] = field(default_factory=list)
    failed_criteria: List[CriterionResult] = field(default_factory=list)
    missing_profile_fields: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Individual criterion checkers
# ---------------------------------------------------------------------------

def _check_state(profile: UserProfile, scheme: dict) -> CriterionResult:
    scheme_state = scheme.get("state", "All India")
    if scheme_state == "All India":
        return CriterionResult(
            criterion="State",
            passed=True,
            detail="This is a central/all-India scheme — open to all states."
        )
    if profile.state is None:
        return CriterionResult(
            criterion="State",
            passed=False,
            detail="State not provided — cannot verify residency requirement."
        )
    passed = profile.state.strip().lower() == scheme_state.strip().lower()
    return CriterionResult(
        criterion="State",
        passed=passed,
        detail=(
            f"Scheme is for {scheme_state}. Your state: {profile.state}."
            if not passed
            else f"Resident of {profile.state} — matches scheme requirement."
        )
    )


def _check_disability_percentage(profile: UserProfile, scheme: dict) -> Optional[CriterionResult]:
    minimum = scheme.get("min_disability_percentage")
    if minimum is None:
        return None  # scheme has no disability % requirement
    if profile.disability_percentage is None:
        return CriterionResult(
            criterion="Disability Percentage",
            passed=False,
            detail=f"Disability percentage not provided. This scheme requires {minimum}% or above."
        )
    passed = profile.disability_percentage >= minimum
    return CriterionResult(
        criterion="Disability Percentage",
        passed=passed,
        detail=(
            f"Your disability percentage is {profile.disability_percentage}%, "
            f"which meets the minimum requirement of {minimum}%."
            if passed
            else
            f"Your disability percentage is {profile.disability_percentage}%. "
            f"This scheme requires at least {minimum}%."
        )
    )


def _check_income(profile: UserProfile, scheme: dict) -> Optional[CriterionResult]:
    limit = scheme.get("income_limit")
    if limit is None:
        return None
    if profile.annual_family_income is None:
        return CriterionResult(
            criterion="Family Income",
            passed=False,
            detail=f"Annual family income not provided. Limit is ₹{limit:,}."
        )
    passed = profile.annual_family_income <= limit
    return CriterionResult(
        criterion="Family Income",
        passed=passed,
        detail=(
            f"Annual family income ₹{profile.annual_family_income:,} is within the limit of ₹{limit:,}."
            if passed
            else
            f"Annual family income ₹{profile.annual_family_income:,} exceeds the limit of ₹{limit:,}."
        )
    )


def _check_education(profile: UserProfile, scheme: dict) -> Optional[CriterionResult]:
    allowed = scheme.get("education_levels")
    if not allowed:
        return None
    if profile.education is None:
        return CriterionResult(
            criterion="Education Level",
            passed=False,
            detail=f"Education level not provided. Scheme covers: {', '.join(allowed)}."
        )
    passed = profile.education in allowed
    return CriterionResult(
        criterion="Education Level",
        passed=passed,
        detail=(
            f"Education level '{profile.education}' is eligible for this scheme."
            if passed
            else
            f"Education level '{profile.education}' is not covered. "
            f"Scheme covers: {', '.join(allowed)}."
        )
    )


def _check_disability_type(profile: UserProfile, scheme: dict) -> Optional[CriterionResult]:
    allowed = scheme.get("eligible_disability_types")
    if not allowed:
        return None
    if profile.disability_type is None:
        return None  # not blocking — type not always required
    passed = profile.disability_type in allowed
    return CriterionResult(
        criterion="Disability Type",
        passed=passed,
        detail=(
            f"Disability type '{profile.disability_type}' is eligible."
            if passed
            else
            f"Disability type '{profile.disability_type}' is not covered by this scheme. "
            f"Eligible types: {', '.join(allowed)}."
        )
    )


def _check_category(profile: UserProfile, scheme: dict) -> Optional[CriterionResult]:
    allowed = scheme.get("eligible_categories")
    if not allowed:
        return None
    if profile.category is None:
        return None  # category not always required
    passed = profile.category in allowed
    return CriterionResult(
        criterion="Social Category",
        passed=passed,
        detail=(
            f"Category '{profile.category}' is eligible."
            if passed
            else
            f"Category '{profile.category}' is not covered. Eligible: {', '.join(allowed)}."
        )
    )


# ---------------------------------------------------------------------------
# Core evaluation function
# ---------------------------------------------------------------------------

def _evaluate_scheme(profile: UserProfile, scheme: dict) -> SchemeMatch:
    """Run all criteria checks for a single scheme against a user profile."""
    checks = [
        _check_state(profile, scheme),
        _check_disability_percentage(profile, scheme),
        _check_income(profile, scheme),
        _check_education(profile, scheme),
        _check_disability_type(profile, scheme),
        _check_category(profile, scheme),
    ]

    # Filter out None (criteria not applicable to this scheme)
    results = [c for c in checks if c is not None]

    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]

    # Determine overall eligibility
    eligible = len(failed) == 0 and len(results) > 0

    # Collect plain-language reasons for the LLM to surface to the user
    reasons = [r.detail for r in results]

    # Track which profile fields were missing (so agent can ask for them)
    missing_fields = profile.missing_fields_for_eligibility()

    return SchemeMatch(
        scheme_id=scheme["scheme_id"],
        name=scheme["name"],
        eligible=eligible,
        reasons=reasons,
        benefits=scheme.get("benefits", []),
        official_url=scheme.get("official_url", ""),
        source_document=scheme.get("source_document", ""),
        matched_criteria=passed,
        failed_criteria=failed,
        missing_profile_fields=missing_fields,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def check_eligibility(
    profile: UserProfile,
    scheme_id: Optional[str] = None
) -> List[SchemeMatch]:
    """
    Check a user profile against one or all schemes.

    Args:
        profile:   The citizen's profile built up during conversation.
        scheme_id: If provided, check only that scheme.
                   If None, check all loaded schemes and return ranked results.

    Returns:
        List of SchemeMatch objects sorted: eligible first, then by name.
    """
    if scheme_id:
        scheme = get_scheme_by_id(scheme_id)
        if scheme is None:
            return []
        return [_evaluate_scheme(profile, scheme)]

    schemes = get_all_schemes()
    results = [_evaluate_scheme(profile, s) for s in schemes]

    # Sort: eligible matches first, then alphabetically by name
    results.sort(key=lambda r: (not r.eligible, r.name))
    return results

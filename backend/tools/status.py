"""
Application status tool.

For the hackathon prototype, this performs a best-effort lookup
against known government status portals. In production this would
integrate with actual NSP / state portal APIs.

IMPORTANT: Never fabricate a status. If the number is not found or
the portal is unreachable, say so clearly — never guess or invent a status.
"""

from dataclasses import dataclass
from typing import Optional
import re


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class StatusResult:
    registration_number: str
    status: str
    last_updated: str
    source: str
    portal_url: str
    found: bool


# ---------------------------------------------------------------------------
# Registration number pattern registry
# Used to route a number to the correct portal based on its format.
# ---------------------------------------------------------------------------

_PORTAL_PATTERNS = [
    {
        "name": "National Scholarship Portal (NSP)",
        "pattern": r"^NSP\d{10,}$",
        "check_url_template": "https://scholarships.gov.in/fresh/checkApplicationStatus?appId={number}",
        "portal_url": "https://scholarships.gov.in",
    },
    {
        "name": "Karnataka Social Welfare Department",
        "pattern": r"^KA[A-Z]{2}\d{6,}$",
        "check_url_template": "https://sw.kar.nic.in/scholarship/status?ref={number}",
        "portal_url": "https://sw.kar.nic.in/scholarship",
    },
    {
        "name": "AICTE Saksham (NSP)",
        "pattern": r"^AICTE\d{8,}$",
        "check_url_template": "https://scholarships.gov.in/fresh/checkApplicationStatus?appId={number}",
        "portal_url": "https://scholarships.gov.in",
    },
]

_FALLBACK_PORTAL = {
    "name": "National Scholarship Portal (NSP)",
    "portal_url": "https://scholarships.gov.in",
    "check_url_template": "https://scholarships.gov.in/fresh/checkApplicationStatus?appId={number}",
}


def _detect_portal(registration_number: str) -> dict:
    """Match a registration number to its portal using pattern matching."""
    cleaned = registration_number.strip().upper().replace(" ", "")
    for portal in _PORTAL_PATTERNS:
        if re.match(portal["pattern"], cleaned):
            return portal
    return _FALLBACK_PORTAL


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def check_application_status(registration_number: str) -> StatusResult:
    """
    Look up the status of an application by registration number.

    For the prototype, this does not make a live HTTP call to the government
    portal (that would require authentication/CAPTCHA the AI cannot complete).
    Instead it:
      1. Validates the registration number format.
      2. Identifies the correct portal.
      3. Returns a clear "check here" result with the portal URL.

    Args:
        registration_number: The reference number from the application acknowledgement.

    Returns:
        StatusResult — always set found=False for prototype with guidance
        on where the citizen must check themselves.
    """
    if not registration_number or not registration_number.strip():
        return StatusResult(
            registration_number=registration_number,
            status="Invalid — registration number is empty.",
            last_updated="N/A",
            source="Sahayak validation",
            portal_url="",
            found=False,
        )

    portal = _detect_portal(registration_number)
    check_url = portal["check_url_template"].format(number=registration_number.strip())

    return StatusResult(
        registration_number=registration_number.strip(),
        status=(
            "Sahayak cannot retrieve live application status — the government portal "
            "requires authentication that you must complete yourself. "
            f"Please visit {check_url} to check your status directly."
        ),
        last_updated="Live — check the portal for real-time status.",
        source=portal["name"],
        portal_url=portal["portal_url"],
        found=False,
    )

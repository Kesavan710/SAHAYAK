"""
Documents tool — resolves required, available, and missing documents
for a given scheme and user profile.

Strictly data-driven: the source of truth for required documents
is the scheme JSON, not the LLM.
"""

from typing import List, Optional
from dataclasses import dataclass

from backend.models.user_profile import UserProfile
from backend.tools.scheme_loader import get_scheme_by_id


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class DocumentResult:
    scheme_id: str
    scheme_name: str
    required_documents: List[str]
    available_documents: List[str]
    missing_documents: List[str]
    official_url: str
    source_document: str


# ---------------------------------------------------------------------------
# Normalisation helper
# ---------------------------------------------------------------------------

def _normalise(doc: str) -> str:
    """Lowercase and strip for fuzzy matching of document names."""
    return doc.lower().strip()


def _is_available(required_doc: str, available_docs: List[str]) -> bool:
    """
    Check whether a required document is in the user's available list.
    Uses simple substring matching to handle minor naming variations
    (e.g. "Disability Certificate (SADAREM/UDID)" matches "Disability Certificate").
    """
    req_norm = _normalise(required_doc)
    for avail in available_docs:
        avail_norm = _normalise(avail)
        # Either exact match or one contains the other
        if req_norm == avail_norm or avail_norm in req_norm or req_norm in avail_norm:
            return True
    return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_required_documents(
    scheme_id: str,
    profile: Optional[UserProfile] = None
) -> DocumentResult:
    """
    Return required, available, and missing documents for a scheme.

    Args:
        scheme_id: The scheme to look up.
        profile:   If provided, cross-reference documents_available to
                   determine which documents the citizen still needs.
                   If None, all required documents are listed as missing.

    Returns:
        DocumentResult with the three lists and scheme metadata.

    Raises:
        ValueError: If scheme_id is not found in the knowledge base.
    """
    scheme = get_scheme_by_id(scheme_id)
    if scheme is None:
        raise ValueError(f"Scheme '{scheme_id}' not found in knowledge base.")

    required: List[str] = scheme.get("documents", [])
    available_raw: List[str] = (
        profile.documents_available or [] if profile else []
    )

    available: List[str] = []
    missing: List[str] = []

    for doc in required:
        if _is_available(doc, available_raw):
            available.append(doc)
        else:
            missing.append(doc)

    return DocumentResult(
        scheme_id=scheme["scheme_id"],
        scheme_name=scheme["name"],
        required_documents=required,
        available_documents=available,
        missing_documents=missing,
        official_url=scheme.get("official_url", ""),
        source_document=scheme.get("source_document", ""),
    )


def explain_form_field(field_name: str) -> str:
    """
    Return a plain-language explanation of a document or form field name.
    Used by the agent when a citizen asks "what is this?" about a document.
    """
    explanations = {
        "disability certificate (sadarem/udid)": (
            "An official certificate issued by a government-recognised medical authority "
            "confirming your disability type and percentage. In Karnataka, this can be obtained "
            "from SADAREM (district hospitals) or as a UDID card from the UDID portal (udid.gov.in)."
        ),
        "disability certificate": (
            "An official certificate confirming your type and percentage of disability, "
            "issued by a government medical authority such as a Civil Surgeon or CMO."
        ),
        "income certificate": (
            "A certificate issued by a Tahsildar (or equivalent) confirming your family's "
            "annual income. Required to verify you meet the income limit for this scheme."
        ),
        "bonafide certificate": (
            "A letter from your college or institution confirming that you are a currently "
            "enrolled student, stating your course and year of study."
        ),
        "bonafide certificate from institution": (
            "A letter from your college or institution confirming that you are a currently "
            "enrolled student, stating your course and year of study."
        ),
        "bank passbook (first page)": (
            "A photocopy of the first page of your bank passbook, showing your name, "
            "account number, IFSC code, and bank branch — used for direct benefit transfer."
        ),
        "bank account details (aadhaar-linked account preferred)": (
            "Your bank account number and IFSC code. Linking it to Aadhaar allows the "
            "scholarship to be transferred directly to your account via DBT."
        ),
        "aadhaar card": (
            "Your 12-digit Aadhaar number issued by UIDAI. Used for identity verification. "
            "You must complete OTP/biometric verification yourself on the government portal."
        ),
        "passport size photograph": (
            "A recent colour photograph of yourself, typically 3.5 cm × 4.5 cm, "
            "with a white or light background — similar to what you'd use for a passport."
        ),
        "previous year marks card": (
            "Your official mark sheet from the previous academic year, issued by your "
            "university or board, showing the subjects and marks obtained."
        ),
        "marks card": (
            "Your official mark sheet issued by your university or board."
        ),
        "admission letter / enrollment proof": (
            "The letter you received when you were admitted to your course, "
            "or any official document confirming your enrollment."
        ),
        "institution verification letter": (
            "A letter from your institution's financial aid or scholarship office "
            "verifying your enrollment details for the scholarship application."
        ),
        "aicte institution approval letter": (
            "A document showing that your institution is approved by AICTE to offer "
            "your course. Your institution's administration will have this on record."
        ),
    }
    key = field_name.lower().strip()
    return explanations.get(key, f"No plain-language explanation available for '{field_name}'.")

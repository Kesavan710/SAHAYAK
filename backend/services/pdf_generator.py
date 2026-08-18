"""
PDF generator service for RPwD application preparation package.

Consumes only a CONFIRMED RPwDApplication object.
Generates a structured, readable PDF summary the applicant can take
to a cyber centre or authorised operator.

IMPORTANT: This PDF is an application-preparation summary only.
It does NOT constitute an official government application.
It does NOT claim to issue or substitute a disability certificate.

Uses reportlab for PDF generation with fallback to JSON if not installed.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from backend.schemas.rpwd_application import RPwDApplication
from backend.schemas.enums import ApplicationStatus

# Output directory
_PDF_DIR = Path(__file__).resolve().parents[2] / "generated_packages"
_PDF_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# ReportLab helpers
# ─────────────────────────────────────────────────────────────────────────────

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    )
    _REPORTLAB = True
except ImportError:
    _REPORTLAB = False


def _colour(hex_str: str):
    """Convert hex colour to reportlab Color."""
    from reportlab.lib import colors as rl_colors
    h = hex_str.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return rl_colors.Color(r / 255, g / 255, b / 255)


# ─────────────────────────────────────────────────────────────────────────────
# Section builders
# ─────────────────────────────────────────────────────────────────────────────

def _na(value) -> str:
    """Return value as string, or 'Not provided' if None/empty."""
    if value is None or str(value).strip() == "":
        return "Not provided"
    return str(value)


def _bool_str(value: Optional[bool]) -> str:
    if value is True:
        return "Yes"
    if value is False:
        return "No"
    return "Not answered"


def _section_rows(app: RPwDApplication) -> list[tuple[str, list[tuple[str, str]]]]:
    """
    Build ordered sections → rows for the PDF table.
    Returns list of (section_title, [(label, value), ...]).
    """
    a = app.applicant
    addr = app.addresses
    pa = addr.permanent_address
    ca = addr.communication_address
    edu = app.education_and_occupation
    dis = app.disability
    prev_app = app.previous_application
    prev_cert = app.previous_certificate
    docs = app.documents
    gdn = app.guardian
    decl = app.declaration

    sections = []

    # 1 — Applicant
    sections.append(("Applicant Details", [
        ("First Name",   _na(a.first_name)),
        ("Middle Name",  _na(a.middle_name)),
        ("Last Name",    _na(a.last_name)),
        ("Father's Name", _na(a.father_name)),
        ("Mother's Name", _na(a.mother_name)),
        ("Date of Birth", _na(a.date_of_birth)),
        ("Age",          _na(a.age)),
        ("Gender",       _na(a.gender)),
    ]))

    # 2 — Permanent Address
    if pa:
        sections.append(("Permanent Address", [
            ("Street / House No.", _na(pa.address_line)),
            ("Locality",           _na(pa.locality)),
            ("City / Town / Village", _na(pa.village_town_city)),
            ("District",           _na(pa.district)),
            ("State",              _na(pa.state)),
            ("PIN Code",           _na(pa.pin_code)),
        ]))

    # 3 — Communication Address
    if addr.same_as_permanent:
        sections.append(("Communication Address", [
            ("Same as Permanent Address", "Yes"),
        ]))
    elif ca:
        sections.append(("Communication Address", [
            ("Street / House No.", _na(ca.address_line)),
            ("Locality",           _na(ca.locality)),
            ("City / Town / Village", _na(ca.village_town_city)),
            ("District",           _na(ca.district)),
            ("State",              _na(ca.state)),
            ("PIN Code",           _na(ca.pin_code)),
            ("Residing since",     _na(addr.communication_address_since)),
        ]))

    # 4 — Education & Occupation
    sections.append(("Education & Occupation", [
        ("Educational Status", _na(edu.educational_status)),
        ("Occupation",         _na(edu.occupation)),
    ]))

    # 5 — Identification
    ident = app.identification
    if ident.identification_mark_1 or ident.identification_mark_2:
        sections.append(("Identification Marks", [
            ("Mark 1", _na(ident.identification_mark_1)),
            ("Mark 2", _na(ident.identification_mark_2)),
        ]))

    # 6 — Disability
    sections.append(("Disability Details", [
        ("Type of Disability",   _na(dis.disability_type)),
        ("Description",          _na(dis.disability_description)),
        ("Onset",                _na(dis.onset_type)),
        ("Year of Onset",        _na(dis.onset_year) if dis.onset_type not in
                                  ("from_birth", "OnsetType.FROM_BIRTH") else "N/A (from birth)"),
    ]))

    # 7 — Previous Application
    sections.append(("Previous Application / Certificate", [
        ("Previously Applied",   _bool_str(prev_app.previously_applied)),
        ("Authority",            _na(prev_app.authority) if prev_app.previously_applied else "N/A"),
        ("District",             _na(prev_app.district) if prev_app.previously_applied else "N/A"),
        ("Previous Result",      _na(prev_app.result) if prev_app.previously_applied else "N/A"),
        ("Certificate Previously Issued", _bool_str(prev_cert.previously_issued)),
        ("Certificate Available", _bool_str(prev_cert.certificate_available)
                                  if prev_cert.previously_issued else "N/A"),
    ]))

    # 8 — Documents
    sections.append(("Documents Available", [
        ("Residence Proof",      _na(docs.residence_proof)),
        ("Identity Document",    _na(docs.identity_document)),
        ("Aadhaar Available",    _bool_str(docs.aadhaar_available)),
        ("Passport Photos",      _bool_str(docs.passport_photos_available)),
        ("Medical Reports",      _bool_str(docs.medical_reports_available)),
    ]))

    # 9 — Guardian (only if applicable)
    if gdn.has_guardian:
        sections.append(("Guardian Details", [
            ("Has Guardian",         "Yes"),
            ("Guardian Name",        _na(gdn.full_name)),
            ("Relationship",         _na(gdn.relationship_to_applicant)),
            ("Contact Number",       _na(gdn.contact_number)),
        ]))
    else:
        sections.append(("Guardian", [
            ("Has Guardian", "No"),
        ]))

    # 10 — Declaration
    sections.append(("Declaration", [
        ("Applicant Confirmed",  _bool_str(decl.confirmed)),
        ("Place of Application", _na(decl.application_place)),
        ("Date Generated",       _na(decl.generated_date)),
    ]))

    return sections


# ─────────────────────────────────────────────────────────────────────────────
# ReportLab PDF builder
# ─────────────────────────────────────────────────────────────────────────────

def _build_pdf_reportlab(app: RPwDApplication, output_path: Path) -> None:
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    SAHAYAK_BLUE = _colour("#1A56A0")
    LIGHT_GREY   = _colour("#F5F5F5")
    MID_GREY     = _colour("#CCCCCC")

    title_style = ParagraphStyle(
        "SahayakTitle",
        parent=styles["Title"],
        textColor=SAHAYAK_BLUE,
        fontSize=20,
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "SahayakSubtitle",
        parent=styles["Normal"],
        textColor=colors.grey,
        fontSize=10,
        spaceAfter=2,
    )
    section_style = ParagraphStyle(
        "SahayakSection",
        parent=styles["Heading2"],
        textColor=SAHAYAK_BLUE,
        fontSize=11,
        spaceBefore=14,
        spaceAfter=4,
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        textColor=colors.red,
        fontSize=8,
        leading=12,
        spaceBefore=12,
    )
    notice_style = ParagraphStyle(
        "Notice",
        parent=styles["Normal"],
        textColor=_colour("#7B3F00"),
        fontSize=9,
        leading=13,
        spaceBefore=8,
        borderPad=6,
        backColor=_colour("#FFF8E7"),
    )

    story = []

    # Header
    story.append(Paragraph("SAHAYAK", title_style))
    story.append(Paragraph(
        "RPwD Application Preparation Summary",
        subtitle_style
    ))
    story.append(Paragraph(
        f"Application ID: {app.application_id} &nbsp;&nbsp; "
        f"Generated: {app.declaration.generated_date or datetime.now(timezone.utc).isoformat()}",
        styles["Normal"]
    ))
    story.append(HRFlowable(width="100%", thickness=1,
                             color=SAHAYAK_BLUE, spaceAfter=8))

    # Important notice box
    story.append(Paragraph(
        "⚠ IMPORTANT NOTICE: This is an application-preparation summary only. "
        "Sahayak has NOT submitted any application to the government on your behalf. "
        "You must take this document to an authorised operator or cyber centre, "
        "and complete all authentication, OTP, and CAPTCHA steps yourself on the "
        "official UDID / SADAREM portal.",
        notice_style
    ))

    # Sections
    sections = _section_rows(app)
    col_widths = [6 * cm, 10.5 * cm]

    table_style = TableStyle([
        ("BACKGROUND",  (0, 0), (0, -1), LIGHT_GREY),
        ("TEXTCOLOR",   (0, 0), (0, -1), colors.HexColor("#333333")),
        ("FONTNAME",    (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",    (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("LEADING",     (0, 0), (-1, -1), 14),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, _colour("#FAFAFA")]),
        ("GRID",        (0, 0), (-1, -1), 0.5, MID_GREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
        ("WORDWRAP",    (1, 0), (1, -1), True),
    ])

    for section_title, rows in sections:
        story.append(Paragraph(section_title, section_style))
        table_data = [[label, value] for label, value in rows]
        t = Table(table_data, colWidths=col_widths)
        t.setStyle(table_style)
        story.append(t)

    # Footer disclaimer
    story.append(Spacer(1, 0.5 * cm))
    story.append(HRFlowable(width="100%", thickness=0.5,
                             color=colors.grey, spaceAfter=4))
    story.append(Paragraph(
        "This document was prepared by Sahayak (AI-assisted government accessibility tool) "
        "for informational purposes only. Sahayak does not issue disability certificates, "
        "medically assess applicants, or submit government applications. "
        "All government authentication and submission steps must be completed by the applicant.",
        disclaimer_style
    ))

    doc.build(story)


# ─────────────────────────────────────────────────────────────────────────────
# JSON fallback
# ─────────────────────────────────────────────────────────────────────────────

def _build_json_fallback(app: RPwDApplication, output_path: Path) -> None:
    """Fallback when reportlab is not installed — writes a structured JSON summary."""
    payload = {
        "title": "Sahayak — RPwD Application Preparation Summary",
        "disclaimer": (
            "This is an application-preparation summary only. "
            "Sahayak has NOT submitted any application to the government. "
            "Complete all authentication/OTP/CAPTCHA steps yourself on the official portal."
        ),
        "application_id": app.application_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": app.status,
        "data": app.model_dump(),
    }
    output_path.with_suffix(".json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

class PdfResult:
    def __init__(self, application_id: str, pdf_path: Path, generated_at: str):
        self.application_id = application_id
        self.pdf_path = pdf_path
        self.generated_at = generated_at
        # S3-style object key (placeholder — Person 1 wires real S3 here)
        self.pdf_object_key = (
            f"applications/{application_id}/generated/rpwd_application_summary"
            + (".pdf" if _REPORTLAB else ".json")
        )
        self.download_url = f"/downloads/{pdf_path.name}"


def generate_application_pdf(app: RPwDApplication) -> PdfResult:
    """
    Generate the RPwD application-preparation PDF (or JSON fallback).

    Args:
        app: A CONFIRMED RPwDApplication. Raises ValueError if not confirmed.

    Returns:
        PdfResult with file path, object key, and download URL.
    """
    if app.status not in (
        ApplicationStatus.CONFIRMED, ApplicationStatus.PDF_GENERATED
    ):
        raise ValueError(
            f"PDF can only be generated for a confirmed application. "
            f"Current status: {app.status}. "
            "The applicant must confirm the declaration first."
        )

    generated_at = datetime.now(timezone.utc).isoformat()
    uid = str(uuid.uuid4())[:8]
    safe_id = app.application_id[:8]

    if _REPORTLAB:
        filename = f"rpwd_{safe_id}_{uid}.pdf"
        output_path = _PDF_DIR / filename
        _build_pdf_reportlab(app, output_path)
    else:
        filename = f"rpwd_{safe_id}_{uid}.json"
        output_path = _PDF_DIR / filename
        _build_json_fallback(app, output_path)

    return PdfResult(
        application_id=app.application_id,
        pdf_path=output_path,
        generated_at=generated_at,
    )

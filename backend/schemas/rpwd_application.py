"""
RPwDApplication — canonical data schema for the disability certificate application feature.

This is the shared contract for all five team members.
Field names must not be changed unilaterally — see blueprint doc section 10.

The LLM extracts values; deterministic backend code owns validation and state.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator

from backend.schemas.enums import (
    ApplicationStatus, Gender, OnsetType,
    EducationalStatus, OccupationType, DisabilityType,
    DISABILITY_TYPE_NORMALISE, GENDER_NORMALISE, EDUCATION_NORMALISE,
)


# ---------------------------------------------------------------------------
# Sub-objects
# ---------------------------------------------------------------------------

class Applicant(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    date_of_birth: Optional[str] = None          # stored as YYYY-MM-DD string
    age: Optional[int] = None                    # derived from DOB; do not set independently
    gender: Optional[Gender] = None

    @field_validator("gender", mode="before")
    @classmethod
    def normalise_gender(cls, v):
        if v is None:
            return v
        if isinstance(v, Gender):
            return v
        mapped = GENDER_NORMALISE.get(str(v).lower().strip())
        return mapped if mapped else v

    @field_validator("date_of_birth", mode="before")
    @classmethod
    def normalise_dob(cls, v):
        """Accept common date formats and normalise to YYYY-MM-DD."""
        if v is None:
            return v
        if isinstance(v, date):
            return v.strftime("%Y-%m-%d")
        s = str(v).strip()
        # Try DD/MM/YYYY and DD-MM-YYYY
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%Y/%m/%d"):
            try:
                return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return s  # return as-is; validation layer will flag malformed dates

    @model_validator(mode="after")
    def derive_age(self) -> "Applicant":
        """Calculate age from DOB if DOB is set and age is not explicitly provided."""
        if self.date_of_birth and self.age is None:
            try:
                dob = datetime.strptime(self.date_of_birth, "%Y-%m-%d").date()
                today = date.today()
                self.age = today.year - dob.year - (
                    (today.month, today.day) < (dob.month, dob.day)
                )
            except ValueError:
                pass
        return self


class Address(BaseModel):
    address_line: Optional[str] = None
    locality: Optional[str] = None
    village_town_city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pin_code: Optional[str] = None


class Addresses(BaseModel):
    permanent_address: Optional[Address] = None
    communication_address: Optional[Address] = None
    same_as_permanent: bool = False
    communication_address_since: Optional[str] = None


class EducationAndOccupation(BaseModel):
    educational_status: Optional[EducationalStatus] = None
    occupation: Optional[OccupationType] = None

    @field_validator("educational_status", mode="before")
    @classmethod
    def normalise_education(cls, v):
        if v is None:
            return v
        if isinstance(v, EducationalStatus):
            return v
        mapped = EDUCATION_NORMALISE.get(str(v).lower().strip())
        return mapped if mapped else v

    @field_validator("occupation", mode="before")
    @classmethod
    def normalise_occupation(cls, v):
        if v is None:
            return v
        if isinstance(v, OccupationType):
            return v
        mapping = {
            "student": OccupationType.STUDENT,
            "studying": OccupationType.STUDENT,
            "employed": OccupationType.EMPLOYED,
            "job": OccupationType.EMPLOYED,
            "working": OccupationType.EMPLOYED,
            "self employed": OccupationType.SELF_EMPLOYED,
            "self-employed": OccupationType.SELF_EMPLOYED,
            "business": OccupationType.SELF_EMPLOYED,
            "unemployed": OccupationType.UNEMPLOYED,
            "no job": OccupationType.UNEMPLOYED,
            "homemaker": OccupationType.HOMEMAKER,
            "housewife": OccupationType.HOMEMAKER,
            "retired": OccupationType.RETIRED,
        }
        return mapping.get(str(v).lower().strip(), v)


class Identification(BaseModel):
    identification_mark_1: Optional[str] = None
    identification_mark_2: Optional[str] = None


class Disability(BaseModel):
    disability_type: Optional[DisabilityType] = None
    disability_description: Optional[str] = None
    onset_type: Optional[OnsetType] = None
    onset_year: Optional[int] = None

    @field_validator("disability_type", mode="before")
    @classmethod
    def normalise_disability_type(cls, v):
        if v is None:
            return v
        if isinstance(v, DisabilityType):
            return v
        mapped = DISABILITY_TYPE_NORMALISE.get(str(v).lower().strip())
        return mapped if mapped else v

    @field_validator("onset_type", mode="before")
    @classmethod
    def normalise_onset_type(cls, v):
        if v is None:
            return v
        if isinstance(v, OnsetType):
            return v
        s = str(v).lower().strip()
        if s in ("from_birth", "birth", "congenital", "since birth", "born with"):
            return OnsetType.FROM_BIRTH
        if s in ("since_year", "acquired", "accident", "later", "since"):
            return OnsetType.SINCE_YEAR
        return v


class PreviousApplication(BaseModel):
    previously_applied: Optional[bool] = None
    authority: Optional[str] = None
    district: Optional[str] = None
    result: Optional[str] = None


class PreviousCertificate(BaseModel):
    previously_issued: Optional[bool] = None
    certificate_available: Optional[bool] = None


class DocumentAvailability(BaseModel):
    residence_proof: Optional[str] = None       # document type name
    identity_document: Optional[str] = None
    aadhaar_available: Optional[bool] = None
    passport_photos_available: Optional[bool] = None
    medical_reports_available: Optional[bool] = None


class Guardian(BaseModel):
    has_guardian: Optional[bool] = None
    full_name: Optional[str] = None
    relationship_to_applicant: Optional[str] = None
    contact_number: Optional[str] = None


class Declaration(BaseModel):
    confirmed: bool = False
    application_place: Optional[str] = None
    generated_date: Optional[str] = None        # set by backend at PDF generation


class Metadata(BaseModel):
    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z"
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z"
    )
    completion_percentage: int = 0


# ---------------------------------------------------------------------------
# Root canonical object
# ---------------------------------------------------------------------------

class RPwDApplication(BaseModel):
    """
    Canonical RPwD application object.
    All partial updates are merged into this object by deterministic backend logic.
    The PDF generator consumes only the confirmed version of this object.
    """
    application_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: Optional[str] = None
    status: ApplicationStatus = ApplicationStatus.DRAFT

    applicant: Applicant = Field(default_factory=Applicant)
    addresses: Addresses = Field(default_factory=Addresses)
    education_and_occupation: EducationAndOccupation = Field(
        default_factory=EducationAndOccupation
    )
    identification: Identification = Field(default_factory=Identification)
    disability: Disability = Field(default_factory=Disability)
    previous_application: PreviousApplication = Field(default_factory=PreviousApplication)
    previous_certificate: PreviousCertificate = Field(default_factory=PreviousCertificate)
    documents: DocumentAvailability = Field(default_factory=DocumentAvailability)
    guardian: Guardian = Field(default_factory=Guardian)
    declaration: Declaration = Field(default_factory=Declaration)
    metadata: Metadata = Field(default_factory=Metadata)

    class Config:
        use_enum_values = True

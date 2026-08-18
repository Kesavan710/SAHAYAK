"""
User profile schema for Sahayak.
This is the single source of truth for citizen data collected during conversation.
All fields are optional so the profile can be built incrementally as the agent asks questions.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, validator


class UserProfile(BaseModel):
    name: Optional[str] = Field(None, description="Citizen's full name")
    date_of_birth: Optional[str] = Field(None, description="Date of birth in YYYY-MM-DD format")
    state: Optional[str] = Field(None, description="State of residence, e.g. Karnataka")
    district: Optional[str] = Field(None, description="District of residence")
    education: Optional[str] = Field(
        None,
        description="Highest education level: 'Class 10', 'Class 12', 'Diploma', 'UG', 'PG', 'PhD'"
    )
    year: Optional[int] = Field(
        None, ge=1, le=6,
        description="Current year of study (1–6 for UG/PG programs)"
    )
    disability_type: Optional[str] = Field(
        None,
        description="Type of disability: 'visual', 'hearing', 'locomotor', 'intellectual', 'multiple', 'other'"
    )
    disability_percentage: Optional[int] = Field(
        None, ge=0, le=100,
        description="Disability percentage as certified (0–100)"
    )
    annual_family_income: Optional[int] = Field(
        None, ge=0,
        description="Annual family income in INR"
    )
    category: Optional[str] = Field(
        None,
        description="Social category: 'General', 'OBC', 'SC', 'ST', 'EWS'"
    )
    documents_available: Optional[List[str]] = Field(
        default_factory=list,
        description="List of document names the citizen currently has in hand"
    )

    @validator("education")
    def normalise_education(cls, v):
        if v is None:
            return v
        mapping = {
            "bsc": "UG", "ba": "UG", "bcom": "UG", "be": "UG", "btech": "UG",
            "ug": "UG", "undergraduate": "UG", "degree": "UG",
            "msc": "PG", "ma": "PG", "mcom": "PG", "me": "PG", "mtech": "PG",
            "pg": "PG", "postgraduate": "PG", "masters": "PG",
            "phd": "PhD", "doctorate": "PhD",
            "diploma": "Diploma",
            "class 10": "Class 10", "sslc": "Class 10", "10th": "Class 10",
            "class 12": "Class 12", "puc": "Class 12", "12th": "Class 12", "hsc": "Class 12",
        }
        return mapping.get(v.lower().strip(), v)

    @validator("disability_type")
    def normalise_disability_type(cls, v):
        if v is None:
            return v
        mapping = {
            "blind": "visual", "visually impaired": "visual", "low vision": "visual",
            "deaf": "hearing", "hard of hearing": "hearing",
            "ortho": "locomotor", "orthopedic": "locomotor", "physical": "locomotor",
            "mental": "intellectual", "cognitive": "intellectual",
        }
        return mapping.get(v.lower().strip(), v.lower().strip())

    @validator("category")
    def normalise_category(cls, v):
        if v is None:
            return v
        mapping = {
            "general": "General", "gen": "General", "ur": "General", "open": "General",
            "obc": "OBC", "other backward class": "OBC",
            "sc": "SC", "scheduled caste": "SC", "dalit": "SC",
            "st": "ST", "scheduled tribe": "ST", "tribal": "ST",
            "ews": "EWS", "economically weaker section": "EWS",
        }
        return mapping.get(v.lower().strip(), v)

    def missing_fields_for_eligibility(self) -> List[str]:
        """Returns fields still needed to run a basic eligibility check."""
        required = ["state", "education", "disability_percentage", "annual_family_income"]
        return [f for f in required if getattr(self, f) is None]

    def missing_fields_for_application(self) -> List[str]:
        """Returns fields needed to generate a complete application package."""
        required = [
            "name", "date_of_birth", "state", "district",
            "education", "disability_type", "disability_percentage",
            "annual_family_income", "category"
        ]
        return [f for f in required if getattr(self, f) is None]

    class Config:
        # Allow extra fields to be ignored (future-proofing for Foundry tool calls)
        extra = "ignore"


# Human-readable labels used by the application package screen
FIELD_LABELS: dict = {
    "name": "Full Name",
    "date_of_birth": "Date of Birth",
    "state": "State",
    "district": "District",
    "education": "Education Level",
    "year": "Year of Study",
    "disability_type": "Type of Disability",
    "disability_percentage": "Disability Percentage",
    "annual_family_income": "Annual Family Income (₹)",
    "category": "Social Category",
    "documents_available": "Documents Available",
}

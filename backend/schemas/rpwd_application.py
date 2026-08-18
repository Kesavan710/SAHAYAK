"""
RPwD Application Schema
Master shared data schema for Rights of Persons with Disabilities application preparation.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class Gender(str, Enum):
    """Gender categories"""
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    TRANSGENDER = "Transgender"


class EducationalStatus(str, Enum):
    """Educational qualification levels"""
    ILLITERATE = "Illiterate"
    PRIMARY = "Primary"
    SECONDARY = "Secondary"
    HIGHER_SECONDARY = "Higher Secondary"
    GRADUATE = "Graduate"
    POST_GRADUATE = "Post Graduate"
    PROFESSIONAL = "Professional"


class Occupation(str, Enum):
    """Occupation categories"""
    STUDENT = "Student"
    EMPLOYED = "Employed"
    SELF_EMPLOYED = "Self-Employed"
    UNEMPLOYED = "Unemployed"
    RETIRED = "Retired"
    HOMEMAKER = "Homemaker"


class OnsetType(str, Enum):
    """Disability onset type"""
    FROM_BIRTH = "from_birth"
    SINCE_YEAR = "since_year"


class ApplicationStatus(str, Enum):
    """Application processing status"""
    DRAFT = "draft"
    COLLECTING_INFORMATION = "collecting_information"
    READY_FOR_REVIEW = "ready_for_review"
    CONFIRMED = "confirmed"
    PDF_GENERATED = "pdf_generated"
    ERROR = "error"


# Sub-schemas

class Applicant(BaseModel):
    """Applicant personal information"""
    first_name: str = Field(..., min_length=1)
    middle_name: Optional[str] = None
    last_name: str
    father_name: str
    mother_name: str
    date_of_birth: date
    age: Optional[int] = None  # Derived from DOB
    gender: Gender
    
    @validator('age', always=True)
    def calculate_age(cls, v, values):
        if 'date_of_birth' in values:
            dob = values['date_of_birth']
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            return age
        return v


class Address(BaseModel):
    """Address information"""
    house_address_line: str
    locality: str
    village_town_city: str
    district: str
    state: str
    pin: str = Field(..., pattern=r'^\d{6}$')


class Addresses(BaseModel):
    """Permanent and communication addresses"""
    permanent_address: Address
    communication_address: Optional[Address] = None
    same_as_permanent: bool = Field(default=False)
    communication_address_since: Optional[str] = None


class EducationAndOccupation(BaseModel):
    """Education and occupation details"""
    educational_status: EducationalStatus
    occupation: Occupation


class Identification(BaseModel):
    """Identification marks"""
    identification_mark_1: Optional[str] = None
    identification_mark_2: Optional[str] = None


class Disability(BaseModel):
    """Disability information"""
    disability_type: str  # User's stated disability type
    disability_description: Optional[str] = None
    onset_type: OnsetType
    onset_year: Optional[int] = None
    
    @validator('onset_year')
    def validate_onset_year(cls, v, values):
        if values.get('onset_type') == OnsetType.SINCE_YEAR and v is None:
            raise ValueError('onset_year is required when onset_type is since_year')
        if values.get('onset_type') == OnsetType.FROM_BIRTH and v is not None:
            raise ValueError('onset_year should not be provided when onset_type is from_birth')
        return v


class PreviousApplication(BaseModel):
    """Previous application details"""
    previously_applied: bool
    authority: Optional[str] = None
    district: Optional[str] = None
    result: Optional[str] = None
    
    @validator('authority', 'district', 'result')
    def validate_conditional_fields(cls, v, values, field):
        if values.get('previously_applied') and v is None:
            raise ValueError(f'{field.name} is required when previously_applied is True')
        return v


class PreviousCertificate(BaseModel):
    """Previous certificate information"""
    previously_issued: bool
    certificate_available: Optional[bool] = None
    
    @validator('certificate_available')
    def validate_certificate(cls, v, values):
        if values.get('previously_issued') and v is None:
            raise ValueError('certificate_available is required when previously_issued is True')
        return v


class Document(BaseModel):
    """Document information"""
    document_type: str
    available: bool
    s3_key: Optional[str] = None


class Documents(BaseModel):
    """Required documents"""
    residence_proof: Document
    identity_document: Optional[Document] = None
    aadhaar_available: Optional[bool] = None
    passport_photos_available: bool
    medical_reports_available: Optional[bool] = None


class Guardian(BaseModel):
    """Guardian/representative information"""
    has_guardian: bool
    full_name: Optional[str] = None
    relationship_to_applicant: Optional[str] = None
    contact_number: Optional[str] = None
    
    @validator('full_name', 'relationship_to_applicant', 'contact_number')
    def validate_guardian_fields(cls, v, values, field):
        if values.get('has_guardian') and v is None:
            raise ValueError(f'{field.name} is required when has_guardian is True')
        return v


class Declaration(BaseModel):
    """Declaration and confirmation"""
    confirmed: bool = False
    application_place: Optional[str] = None
    generated_date: Optional[datetime] = None


class Metadata(BaseModel):
    """Application metadata"""
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    completion_percentage: int = Field(default=0, ge=0, le=100)


# Main application schema

class RPwDApplication(BaseModel):
    """
    Rights of Persons with Disabilities Application
    Canonical data structure for RPwD application preparation.
    """
    application_id: str
    session_id: str
    status: ApplicationStatus = Field(default=ApplicationStatus.DRAFT)
    
    # Main sections
    applicant: Optional[Applicant] = None
    addresses: Optional[Addresses] = None
    education_and_occupation: Optional[EducationAndOccupation] = None
    identification: Optional[Identification] = None
    disability: Optional[Disability] = None
    previous_application: Optional[PreviousApplication] = None
    previous_certificate: Optional[PreviousCertificate] = None
    documents: Optional[Documents] = None
    guardian: Optional[Guardian] = None
    declaration: Optional[Declaration] = None
    
    # Metadata
    metadata: Metadata = Field(default_factory=Metadata)
    
    class Config:
        json_schema_extra = {
            "example": {
                "application_id": "app_123456",
                "session_id": "sess_abc789",
                "status": "collecting_information",
                "applicant": {
                    "first_name": "Venu",
                    "last_name": "Kumar",
                    "father_name": "Ravi Kumar",
                    "mother_name": "Lakshmi",
                    "date_of_birth": "2002-05-15",
                    "age": 21,
                    "gender": "Male"
                },
                "disability": {
                    "disability_type": "Visual Impairment",
                    "onset_type": "from_birth"
                }
            }
        }


# Request/Response models for API

class ChatRequest(BaseModel):
    """Chat request for conversational information collection"""
    session_id: Optional[str] = None
    message: str = Field(..., min_length=1)
    language: str = Field(default="en")


class ChatResponse(BaseModel):
    """Chat response with extracted information"""
    session_id: str
    assistant_message: str
    application: Optional[RPwDApplication] = None
    missing_fields: List[str] = Field(default_factory=list)
    next_question: Optional[str] = None
    status: ApplicationStatus


class ApplicationUpdateRequest(BaseModel):
    """Request to update application fields"""
    updates: dict


class ValidationResponse(BaseModel):
    """Application validation result"""
    valid: bool
    missing_fields: List[str] = Field(default_factory=list)
    invalid_fields: List[str] = Field(default_factory=list)
    conditional_requirements: List[str] = Field(default_factory=list)


class ConfirmRequest(BaseModel):
    """Confirmation request"""
    confirmed: bool
    application_place: str


class PDFGenerationResponse(BaseModel):
    """PDF generation response"""
    application_id: str
    status: ApplicationStatus
    pdf_object_key: str
    download_url: str
    generated_at: datetime


__all__ = [
    'RPwDApplication',
    'ApplicationStatus',
    'Gender',
    'EducationalStatus',
    'Occupation',
    'OnsetType',
    'ChatRequest',
    'ChatResponse',
    'ApplicationUpdateRequest',
    'ValidationResponse',
    'ConfirmRequest',
    'PDFGenerationResponse',
]

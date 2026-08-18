"""
Application Request/Response Models
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from .user_profile import UserProfile


class ApplicationRequest(BaseModel):
    """Request to generate application package"""
    
    scheme_id: str = Field(..., description="Scheme identifier")
    user_profile: UserProfile
    output_format: str = Field(default="both", pattern="^(pdf|json|both)$")
    
    class Config:
        schema_extra = {
            "example": {
                "scheme_id": "pm-kisan",
                "output_format": "both"
            }
        }


class ApplicationResponse(BaseModel):
    """Response with application package"""
    
    success: bool
    application_id: str
    scheme_id: str
    form_data: Dict[str, Any]
    document_checklist: Dict[str, List[Dict[str, Any]]]
    submission_steps: List[Dict[str, Any]]
    output_files: Dict[str, Any]
    important_notes: List[str]
    next_action: str


class EligibilityCheckRequest(BaseModel):
    """Request to check eligibility"""
    
    scheme_id: str
    user_profile: UserProfile


class EligibilityCheckResponse(BaseModel):
    """Response with eligibility result"""
    
    eligible: bool
    scheme_id: str
    scheme_name: str
    checks: List[Dict[str, Any]]
    summary: str
    next_steps: str


class DocumentsRequest(BaseModel):
    """Request for required documents"""
    
    scheme_id: str
    user_category: Optional[str] = None


class StatusCheckRequest(BaseModel):
    """Request to check application status"""
    
    scheme_id: str
    application_id: str
    mobile_or_aadhaar: Optional[str] = None


__all__ = [
    'ApplicationRequest',
    'ApplicationResponse',
    'EligibilityCheckRequest',
    'EligibilityCheckResponse',
    'DocumentsRequest',
    'StatusCheckRequest',
]

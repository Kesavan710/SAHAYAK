"""
User Profile Data Models
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date
from enum import Enum


class Gender(str, Enum):
    """Gender options"""
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class CasteCategory(str, Enum):
    """Caste/Category options"""
    GENERAL = "General"
    OBC = "OBC"
    SC = "SC"
    ST = "ST"
    EWS = "EWS"


class UserProfile(BaseModel):
    """Complete user profile for scheme eligibility and applications"""
    
    # Basic Information
    full_name: str = Field(..., min_length=2, max_length=100)
    father_name: Optional[str] = Field(None, max_length=100)
    mother_name: Optional[str] = Field(None, max_length=100)
    date_of_birth: Optional[date] = None
    age: int = Field(..., ge=0, le=150)
    gender: Gender
    
    # Contact Information
    mobile: str = Field(..., pattern=r'^[6-9]\d{9}$', description="10-digit Indian mobile number")
    email: Optional[str] = Field(None, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    
    # Address
    address: str = Field(..., min_length=10, max_length=500)
    district: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    pincode: str = Field(..., pattern=r'^\d{6}$')
    
    # Identity Documents
    aadhaar: Optional[str] = Field(None, pattern=r'^\d{12}$', description="12-digit Aadhaar number")
    
    # Bank Details
    bank_account_number: Optional[str] = Field(None, min_length=9, max_length=18)
    bank_ifsc: Optional[str] = Field(None, pattern=r'^[A-Z]{4}0[A-Z0-9]{6}$')
    bank_name: Optional[str] = None
    bank_branch: Optional[str] = None
    
    # Socio-Economic Details
    annual_family_income: float = Field(..., ge=0, description="Annual family income in INR")
    caste_category: CasteCategory
    occupation: Optional[str] = None
    
    # Special Categories
    is_bpl: bool = Field(default=False, description="Has BPL card")
    has_ration_card: bool = Field(default=False)
    disability_percentage: int = Field(default=0, ge=0, le=100)
    
    # Agricultural Details (if applicable)
    is_farmer: bool = Field(default=False)
    land_holding_acres: Optional[float] = Field(None, ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "full_name": "Rajesh Kumar",
                "father_name": "Suresh Kumar",
                "date_of_birth": "1985-05-15",
                "age": 39,
                "gender": "Male",
                "mobile": "9876543210",
                "email": "rajesh.kumar@example.com",
                "address": "123, Main Street, Village Rampur",
                "district": "Varanasi",
                "state": "Uttar Pradesh",
                "pincode": "221001",
                "aadhaar": "123456789012",
                "bank_account_number": "1234567890",
                "bank_ifsc": "SBIN0001234",
                "annual_family_income": 120000,
                "caste_category": "OBC",
                "occupation": "Farmer",
                "is_bpl": False,
                "has_ration_card": True,
                "is_farmer": True,
                "land_holding_acres": 2.5
            }
        }


class ProfileUpdate(BaseModel):
    """Model for updating specific profile fields"""
    
    full_name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    annual_family_income: Optional[float] = None
    occupation: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_ifsc: Optional[str] = None
    is_bpl: Optional[bool] = None
    disability_percentage: Optional[int] = None
    land_holding_acres: Optional[float] = None


__all__ = ['UserProfile', 'ProfileUpdate', 'Gender', 'CasteCategory']

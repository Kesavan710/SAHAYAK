"""
Form Field Explainer Tool
Helps users understand and fill complex form fields.
"""

from typing import Dict, Any, Optional


# Common form field explanations database
FIELD_EXPLANATIONS = {
    # Aadhaar related
    "aadhaar": {
        "description": "Your 12-digit Aadhaar number",
        "example": "1234 5678 9012",
        "tips": [
            "Enter numbers only, without spaces",
            "Aadhaar card must be linked to your mobile number",
            "Ensure name on Aadhaar matches other documents"
        ]
    },
    "aadhaar_seeding": {
        "description": "Whether your Aadhaar is linked to your bank account",
        "explanation": "Aadhaar seeding means your Aadhaar number is registered with your bank account. This is required for direct benefit transfer (DBT).",
        "how_to_check": "Check your bank passbook or contact bank. Many banks show Aadhaar seeding status in mobile app.",
        "tips": [
            "Visit your bank branch with Aadhaar card to link if not done",
            "Process usually takes 24-48 hours"
        ]
    },
    
    # Bank related
    "ifsc": {
        "description": "Indian Financial System Code - your bank branch's unique 11-character code",
        "example": "SBIN0001234",
        "how_to_find": [
            "Check your bank passbook (usually on first page)",
            "Look at your cancelled cheque",
            "Search online: 'IFSC code [Bank Name] [Branch Name]'",
            "Use bank's mobile app or website"
        ],
        "format": "First 4 letters = Bank code, 5th character = 0, Last 6 characters = Branch code"
    },
    "bank_account_number": {
        "description": "Your bank account number (9-18 digits)",
        "tips": [
            "Enter the account number printed on your passbook or cheque",
            "Do NOT enter IFSC code here",
            "Double-check for accuracy - wrong number will delay payments"
        ]
    },
    
    # Income related
    "annual_income": {
        "description": "Total income of all family members in one year",
        "explanation": "Add up income from all sources: salary, business, agriculture, rent, etc.",
        "tips": [
            "Include income of all family members living together",
            "If you have an income certificate, use that amount",
            "For farmers: include value of crops sold in the year"
        ]
    },
    "income_certificate": {
        "description": "Official certificate from Tehsildar/Revenue Officer stating your family's annual income",
        "how_to_get": [
            "Visit your Tehsildar/Taluka office",
            "Apply online through state portal (varies by state)",
            "Required documents: Ration card, salary slips, land records",
            "Usually issued within 15 days"
        ]
    },
    
    # Land/Agriculture related
    "land_holding": {
        "description": "Total agricultural land owned by your family in acres or hectares",
        "explanation": "This is the total area of land you own for farming, as per land records (7/12, Pattadar Passbook, etc.)",
        "tips": [
            "Check your land records document",
            "Include all plots owned by family members",
            "1 hectare = 2.47 acres"
        ],
        "example": "2.5 acres or 1.0 hectare"
    },
    "khasra_number": {
        "description": "Survey/plot number of your agricultural land",
        "explanation": "Each agricultural plot has a unique number in government records. This is called Khasra/Survey/Plot number.",
        "how_to_find": "Check your land ownership document (7/12 extract, Pattadar Passbook, RoR)"
    },
    
    # Category/Caste related
    "caste_category": {
        "description": "Your social category as per government records",
        "options": ["General", "OBC (Other Backward Classes)", "SC (Scheduled Caste)", "ST (Scheduled Tribe)", "EWS (Economically Weaker Section)"],
        "tips": [
            "Select the category mentioned on your caste certificate",
            "If you don't have a caste certificate and belong to General category, select 'General'",
            "For OBC/SC/ST/EWS, you need a valid caste certificate"
        ]
    },
    "caste_certificate": {
        "description": "Official certificate stating your caste/category",
        "who_needs": "Required for SC/ST/OBC/EWS applicants",
        "how_to_get": [
            "Apply at Tehsildar/SDM office",
            "Apply online through state portal",
            "Required documents: Birth certificate, school certificates, parents' caste certificates"
        ]
    },
    
    # Disability related
    "disability_certificate": {
        "description": "Certificate from medical board stating type and percentage of disability",
        "explanation": "Issued by authorized medical board after examination. States type of disability and percentage (40% minimum for most benefits).",
        "how_to_get": [
            "Visit District Hospital or Medical College",
            "Request disability assessment",
            "Medical board will examine and issue certificate"
        ]
    },
    "udid": {
        "description": "Unique Disability ID - a unique number for persons with disabilities",
        "explanation": "UDID is a national database for persons with disabilities. The card has a unique ID number.",
        "how_to_get": [
            "Apply online at: swavlambancard.gov.in",
            "Visit nearest UDID enrollment center",
            "Requires disability certificate"
        ]
    },
}


def explain_form_field(
    scheme_id: str,
    field_name: str,
    user_context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Explain what a form field means and how to fill it.
    
    Args:
        scheme_id: The scheme whose form is being filled
        field_name: The form field to explain
        user_context: Optional additional context
        
    Returns:
        Dictionary with field explanation and guidance
    """
    try:
        # Normalize field name for lookup
        field_key = field_name.lower().replace(" ", "_").replace("-", "_")
        
        # Check if we have an explanation for this field
        if field_key in FIELD_EXPLANATIONS:
            explanation = FIELD_EXPLANATIONS[field_key]
            
            return {
                "field_name": field_name,
                "scheme_id": scheme_id,
                "found": True,
                **explanation,
                "user_context": user_context
            }
        
        # Search for partial matches
        for key, value in FIELD_EXPLANATIONS.items():
            if key in field_key or field_key in key:
                return {
                    "field_name": field_name,
                    "scheme_id": scheme_id,
                    "found": True,
                    "note": f"Showing explanation for similar field: {key}",
                    **value,
                    "user_context": user_context
                }
        
        # No explanation found
        return {
            "field_name": field_name,
            "scheme_id": scheme_id,
            "found": False,
            "message": f"No specific explanation found for '{field_name}'. Please provide more context or rephrase the field name.",
            "suggestion": "Try describing what the field asks for, or check the form's help text.",
            "user_context": user_context
        }
        
    except Exception as e:
        return {
            "field_name": field_name,
            "scheme_id": scheme_id,
            "error": str(e),
            "message": "Error explaining field. Please try again."
        }


__all__ = ['explain_form_field']

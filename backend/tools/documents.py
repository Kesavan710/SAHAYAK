"""
Required Documents Tool
Returns list of documents needed for a scheme application.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional


def load_scheme_documents(scheme_id: str) -> Dict[str, Any]:
    """Load document requirements from scheme data."""
    schemes_path = Path(__file__).parent.parent / "knowledge" / "schemes"
    scheme_file = schemes_path / f"{scheme_id}.json"
    
    if scheme_file.exists():
        with open(scheme_file, 'r') as f:
            data = json.load(f)
            return data.get("required_documents", {})
    
    # Fallback: Generic document list
    return {
        "mandatory": [
            {
                "name": "Aadhaar Card",
                "description": "12-digit Aadhaar number and card copy",
                "format": "PDF or JPEG scan"
            },
            {
                "name": "Income Certificate",
                "description": "Certificate from Tehsildar/Revenue Officer showing annual family income",
                "format": "Original certificate (PDF scan)"
            },
            {
                "name": "Address Proof",
                "description": "Ration card, Voter ID, or electricity bill",
                "format": "PDF or JPEG scan"
            },
            {
                "name": "Bank Account Details",
                "description": "Bank passbook first page or cancelled cheque",
                "format": "PDF or JPEG scan"
            },
        ],
        "optional": [
            {
                "name": "Caste Certificate",
                "description": "Required for SC/ST/OBC applicants",
                "format": "Original certificate from competent authority"
            }
        ]
    }


def get_required_documents(
    scheme_id: str,
    user_category: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get list of required documents for a scheme application.
    
    Args:
        scheme_id: Unique identifier for the scheme
        user_category: Optional category for category-specific documents
        
    Returns:
        Dictionary with mandatory and optional document lists
    """
    try:
        # Load base document requirements
        doc_requirements = load_scheme_documents(scheme_id)
        
        mandatory = doc_requirements.get("mandatory", [])
        optional = doc_requirements.get("optional", [])
        
        # Add category-specific documents
        if user_category:
            category_docs = doc_requirements.get("category_specific", {})
            if user_category in category_docs:
                for doc in category_docs[user_category]:
                    # Add to mandatory if marked as required
                    if doc.get("required", False):
                        mandatory.append(doc)
                    else:
                        optional.append(doc)
        
        # Add helpful tips
        tips = [
            "Ensure all documents are clear and readable",
            "File size should be less than 2MB per document",
            "Accepted formats: PDF, JPEG, PNG",
            "Keep original documents ready for verification",
            "Self-attested copies are usually acceptable",
        ]
        
        return {
            "scheme_id": scheme_id,
            "mandatory_documents": mandatory,
            "optional_documents": optional,
            "total_mandatory": len(mandatory),
            "total_optional": len(optional),
            "tips": tips,
            "note": "Document requirements may vary by state. Check with local authorities for state-specific requirements."
        }
        
    except Exception as e:
        return {
            "scheme_id": scheme_id,
            "error": str(e),
            "message": "Error loading document requirements. Please verify scheme ID.",
            "mandatory_documents": [],
            "optional_documents": []
        }


__all__ = ['get_required_documents']

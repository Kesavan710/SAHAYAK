"""
Application Package Generator Tool
Creates pre-filled application forms and checklists.
"""

import json
from typing import Dict, Any
from datetime import datetime
from pathlib import Path


def generate_application_package(
    scheme_id: str,
    user_profile: Dict[str, Any],
    output_format: str = "both"
) -> Dict[str, Any]:
    """
    Generate a pre-filled application package for a scheme.
    
    Args:
        scheme_id: The scheme to apply for
        user_profile: Complete user profile data
        output_format: 'pdf', 'json', or 'both'
        
    Returns:
        Dictionary with application package details and download links
    """
    try:
        # Generate timestamp for unique file naming
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        application_id = f"{scheme_id}_{timestamp}"
        
        # Pre-filled form data
        form_data = {
            "application_id": application_id,
            "scheme_id": scheme_id,
            "submission_date": datetime.now().isoformat(),
            "applicant_details": {
                "full_name": user_profile.get("full_name", ""),
                "father_name": user_profile.get("father_name", ""),
                "mother_name": user_profile.get("mother_name", ""),
                "date_of_birth": user_profile.get("date_of_birth", ""),
                "gender": user_profile.get("gender", ""),
                "age": user_profile.get("age", ""),
            },
            "contact_details": {
                "mobile": user_profile.get("mobile", ""),
                "email": user_profile.get("email", ""),
                "address": user_profile.get("address", ""),
                "district": user_profile.get("district", ""),
                "state": user_profile.get("state", ""),
                "pincode": user_profile.get("pincode", ""),
            },
            "identity_proof": {
                "aadhaar": user_profile.get("aadhaar", ""),
            },
            "bank_details": {
                "account_number": user_profile.get("bank_account_number", ""),
                "ifsc_code": user_profile.get("bank_ifsc", ""),
                "bank_name": user_profile.get("bank_name", ""),
                "branch_name": user_profile.get("bank_branch", ""),
            },
            "socio_economic_details": {
                "annual_family_income": user_profile.get("annual_family_income", 0),
                "caste_category": user_profile.get("caste_category", ""),
                "occupation": user_profile.get("occupation", ""),
                "is_bpl": user_profile.get("is_bpl", False),
            }
        }
        
        # Document checklist
        checklist = {
            "mandatory_documents": [
                {"name": "Aadhaar Card", "status": "required", "uploaded": False},
                {"name": "Income Certificate", "status": "required", "uploaded": False},
                {"name": "Address Proof", "status": "required", "uploaded": False},
                {"name": "Bank Passbook/Cancelled Cheque", "status": "required", "uploaded": False},
                {"name": "Passport Size Photo", "status": "required", "uploaded": False},
            ],
            "optional_documents": [
                {"name": "Caste Certificate", "status": "if_applicable", "uploaded": False},
                {"name": "Disability Certificate", "status": "if_applicable", "uploaded": False},
                {"name": "BPL Card", "status": "if_applicable", "uploaded": False},
            ]
        }
        
        # Add category-specific documents
        if user_profile.get("caste_category") in ["SC", "ST", "OBC", "EWS"]:
            checklist["mandatory_documents"].append({
                "name": f"{user_profile['caste_category']} Certificate",
                "status": "required",
                "uploaded": False
            })
        
        # Step-by-step submission instructions
        submission_steps = [
            {
                "step": 1,
                "title": "Review Pre-filled Form",
                "description": "Check all details in the generated form for accuracy",
                "action": "Verify personal details, bank information, and other fields"
            },
            {
                "step": 2,
                "title": "Gather Required Documents",
                "description": "Collect all mandatory documents listed in the checklist",
                "action": "Scan/photograph all documents in clear, readable format"
            },
            {
                "step": 3,
                "title": "Visit Official Portal",
                "description": f"Go to the official application portal for {scheme_id}",
                "action": "Create account if needed, or login with existing credentials",
                "portal_url": f"https://schemes.gov.in/{scheme_id}/apply"  # Mock URL
            },
            {
                "step": 4,
                "title": "Upload Documents",
                "description": "Upload all required documents as per portal guidelines",
                "action": "Follow file size and format requirements (usually PDF/JPEG, max 2MB)"
            },
            {
                "step": 5,
                "title": "Fill Online Form",
                "description": "Use the pre-filled data to complete the online form",
                "action": "Copy information from the generated form, double-check all entries"
            },
            {
                "step": 6,
                "title": "Review and Submit",
                "description": "Review all information and documents before final submission",
                "action": "Click 'Preview' to see full application, then 'Submit'"
            },
            {
                "step": 7,
                "title": "Save Application ID",
                "description": "After submission, save the application/reference ID",
                "action": "Take screenshot, print acknowledgment, or save PDF receipt"
            },
            {
                "step": 8,
                "title": "Track Status",
                "description": "Use application ID to track application status",
                "action": "Check portal regularly or use the status checker tool"
            }
        ]
        
        # Important notes
        notes = [
            "⚠️ IMPORTANT: This agent CANNOT submit applications on your behalf",
            "You must visit the official government portal to submit your application",
            "Keep all original documents ready for offline verification if required",
            "Application processing time varies by scheme (typically 15-30 days)",
            "You will receive updates via SMS/email on registered mobile/email",
            "For queries, contact the scheme helpline or visit district office"
        ]
        
        # Generate file paths (mock - in production, actually generate PDF)
        output_files = {}
        if output_format in ["pdf", "both"]:
            output_files["pdf"] = {
                "filename": f"{application_id}_application.pdf",
                "path": f"/downloads/{application_id}_application.pdf",
                "size": "~500KB",
                "note": "PDF generation would happen here in production"
            }
        
        if output_format in ["json", "both"]:
            output_files["json"] = {
                "filename": f"{application_id}_data.json",
                "data": form_data,
                "note": "JSON data for programmatic use"
            }
        
        return {
            "success": True,
            "application_id": application_id,
            "scheme_id": scheme_id,
            "generated_at": datetime.now().isoformat(),
            "form_data": form_data,
            "document_checklist": checklist,
            "submission_steps": submission_steps,
            "output_files": output_files,
            "important_notes": notes,
            "next_action": f"Visit the official portal to submit your application: https://schemes.gov.in/{scheme_id}/apply"
        }
        
    except Exception as e:
        return {
            "success": False,
            "scheme_id": scheme_id,
            "error": str(e),
            "message": "Error generating application package. Please check your profile data and try again."
        }


__all__ = ['generate_application_package']

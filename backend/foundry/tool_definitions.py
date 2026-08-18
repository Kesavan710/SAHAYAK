"""
Function Tool Definitions for Sahayak Agent
Defines the schemas for the five custom tools the LLM can call.
"""

from azure.ai.projects.models import FunctionTool


def get_function_tools():
    """
    Returns the list of FunctionTool definitions for the Sahayak agent.
    
    These tools allow the LLM to call deterministic Python functions for:
    1. check_eligibility - Check if user qualifies for a scheme
    2. get_required_documents - Get list of documents needed for a scheme
    3. explain_form_field - Explain what a form field means and how to fill it
    4. generate_application_package - Create a pre-filled application package
    5. check_application_status - Check status of submitted application
    """
    
    tools = [
        # Tool 1: Eligibility Checker
        FunctionTool(
            name="check_eligibility",
            description=(
                "Check if a user is eligible for a specific government scheme based on their profile. "
                "This tool evaluates income limits, age requirements, disability percentage, caste/category, "
                "occupation, and other criteria against the scheme's eligibility rules. "
                "Always use this tool when a user asks 'Am I eligible for X scheme?' "
                "Returns a deterministic yes/no answer with specific reasons."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "scheme_id": {
                        "type": "string",
                        "description": "The unique identifier of the scheme (e.g., 'pm-kisan', 'ayushman-bharat')"
                    },
                    "user_profile": {
                        "type": "object",
                        "description": "User's profile information for eligibility checking",
                        "properties": {
                            "age": {"type": "integer", "description": "User's age in years"},
                            "annual_family_income": {"type": "number", "description": "Annual family income in INR"},
                            "state": {"type": "string", "description": "State of residence"},
                            "district": {"type": "string", "description": "District of residence"},
                            "caste_category": {
                                "type": "string",
                                "enum": ["General", "OBC", "SC", "ST", "EWS"],
                                "description": "Caste/reservation category"
                            },
                            "disability_percentage": {
                                "type": "integer",
                                "description": "Disability percentage (0-100), if applicable"
                            },
                            "occupation": {"type": "string", "description": "Current occupation"},
                            "is_bpl": {"type": "boolean", "description": "Whether user has BPL card"},
                            "has_ration_card": {"type": "boolean", "description": "Whether user has ration card"},
                        },
                        "required": ["age", "annual_family_income", "state"]
                    }
                },
                "required": ["scheme_id", "user_profile"]
            }
        ),
        
        # Tool 2: Required Documents Fetcher
        FunctionTool(
            name="get_required_documents",
            description=(
                "Get the complete list of documents required to apply for a specific scheme. "
                "Returns document names, descriptions, and whether they are mandatory or optional. "
                "Use this when user asks 'What documents do I need for X scheme?' "
                "or before generating an application package."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "scheme_id": {
                        "type": "string",
                        "description": "The unique identifier of the scheme"
                    },
                    "user_category": {
                        "type": "string",
                        "description": "Optional: User's category (e.g., 'SC', 'Farmer', 'Disabled') for category-specific document lists",
                        "enum": ["General", "OBC", "SC", "ST", "EWS", "Farmer", "Disabled", "Senior Citizen", "Woman"]
                    }
                },
                "required": ["scheme_id"]
            }
        ),
        
        # Tool 3: Form Field Explainer
        FunctionTool(
            name="explain_form_field",
            description=(
                "Explain what a specific form field means and how to fill it correctly. "
                "Provides clear guidance on complex fields like 'Aadhaar seeding status', "
                "'Land holding details', 'Bank IFSC code', etc. "
                "Use this when user asks 'What does X field mean?' or 'How do I fill Y?'"
            ),
            parameters={
                "type": "object",
                "properties": {
                    "scheme_id": {
                        "type": "string",
                        "description": "The scheme ID whose form is being filled"
                    },
                    "field_name": {
                        "type": "string",
                        "description": "The name or label of the form field to explain"
                    },
                    "user_context": {
                        "type": "string",
                        "description": "Optional: Additional context about user's situation"
                    }
                },
                "required": ["scheme_id", "field_name"]
            }
        ),
        
        # Tool 4: Application Package Generator
        FunctionTool(
            name="generate_application_package",
            description=(
                "Generate a pre-filled application package for a scheme including: "
                "1) PDF with pre-filled form fields, 2) Document checklist, "
                "3) Step-by-step submission instructions. "
                "Use this when user says 'Help me apply' or 'Generate my application'. "
                "Requires user profile to pre-fill the form."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "scheme_id": {
                        "type": "string",
                        "description": "The scheme to generate application for"
                    },
                    "user_profile": {
                        "type": "object",
                        "description": "Complete user profile for pre-filling the form",
                        "properties": {
                            "full_name": {"type": "string"},
                            "father_name": {"type": "string"},
                            "mother_name": {"type": "string"},
                            "date_of_birth": {"type": "string", "format": "date"},
                            "gender": {"type": "string", "enum": ["Male", "Female", "Other"]},
                            "mobile": {"type": "string"},
                            "email": {"type": "string"},
                            "aadhaar": {"type": "string"},
                            "address": {"type": "string"},
                            "district": {"type": "string"},
                            "state": {"type": "string"},
                            "pincode": {"type": "string"},
                            "bank_account_number": {"type": "string"},
                            "bank_ifsc": {"type": "string"},
                            "annual_family_income": {"type": "number"},
                            "caste_category": {"type": "string"},
                        },
                        "required": ["full_name", "mobile", "state", "district"]
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["pdf", "json", "both"],
                        "description": "Format for the application package",
                        "default": "both"
                    }
                },
                "required": ["scheme_id", "user_profile"]
            }
        ),
        
        # Tool 5: Application Status Checker
        FunctionTool(
            name="check_application_status",
            description=(
                "Check the current status of a submitted application. "
                "Queries the government portal or database to get real-time status. "
                "Use when user asks 'What is my application status?' or 'Has my application been approved?' "
                "Note: This is informational only - the agent cannot modify application status."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "scheme_id": {
                        "type": "string",
                        "description": "The scheme the application was submitted for"
                    },
                    "application_id": {
                        "type": "string",
                        "description": "The application/reference ID provided after submission"
                    },
                    "mobile_or_aadhaar": {
                        "type": "string",
                        "description": "User's mobile number or Aadhaar number for verification"
                    }
                },
                "required": ["scheme_id", "application_id"]
            }
        ),
    ]
    
    return tools


__all__ = ['get_function_tools']

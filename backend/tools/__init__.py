"""
Sahayak Custom Tools
Local Python implementations of the five custom function tools.
"""

from .eligibility import check_eligibility
from .documents import get_required_documents
from .form_helper import explain_form_field
from .application import generate_application_package
from .status import check_application_status

# Tool dispatch mapping for the runner
TOOL_DISPATCH = {
    "check_eligibility": check_eligibility,
    "get_required_documents": get_required_documents,
    "explain_form_field": explain_form_field,
    "generate_application_package": generate_application_package,
    "check_application_status": check_application_status,
}

__all__ = [
    'check_eligibility',
    'get_required_documents',
    'explain_form_field',
    'generate_application_package',
    'check_application_status',
    'TOOL_DISPATCH',
]

"""
Application Router - Application package generation
"""

from fastapi import APIRouter, HTTPException
from models.application import ApplicationRequest, ApplicationResponse
from tools.application import generate_application_package

router = APIRouter()


@router.post("/application/package", response_model=ApplicationResponse)
async def create_application_package(request: ApplicationRequest):
    """
    Generate pre-filled application package.
    Returns form data, document checklist, and submission instructions.
    
    Fast path without LLM - useful for direct application generation from UI.
    The agent can also call this during conversations.
    """
    try:
        # Convert profile to dict
        profile_dict = request.user_profile.dict()
        
        # Generate package
        result = generate_application_package(
            scheme_id=request.scheme_id,
            user_profile=profile_dict,
            output_format=request.output_format
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Error generating application package")
            )
        
        return ApplicationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating application: {str(e)}"
        )


__all__ = ['router']

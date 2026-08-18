"""
Status Router - Application status checking
"""

from fastapi import APIRouter, HTTPException
from models.application import StatusCheckRequest
from tools.status import check_application_status

router = APIRouter()


@router.post("/status/check")
async def check_status(request: StatusCheckRequest):
    """
    Check application status.
    Fast path without LLM - queries status directly.
    
    The agent can also call this during conversations.
    """
    try:
        result = check_application_status(
            scheme_id=request.scheme_id,
            application_id=request.application_id,
            mobile_or_aadhaar=request.mobile_or_aadhaar
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Error checking status")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error checking status: {str(e)}"
        )


@router.get("/status/{scheme_id}/{application_id}")
async def check_status_get(scheme_id: str, application_id: str, mobile: str = None):
    """
    GET version of status check for simple queries.
    """
    try:
        result = check_application_status(
            scheme_id=scheme_id,
            application_id=application_id,
            mobile_or_aadhaar=mobile
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Error checking status")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error checking status: {str(e)}"
        )


__all__ = ['router']

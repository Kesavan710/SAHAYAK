"""
Eligibility Router - Direct eligibility checking
"""

from fastapi import APIRouter, HTTPException
from models.application import EligibilityCheckRequest, EligibilityCheckResponse
from tools.eligibility import check_eligibility

router = APIRouter()


@router.post("/eligibility/check", response_model=EligibilityCheckResponse)
async def check_eligibility_endpoint(request: EligibilityCheckRequest):
    """
    Fast path for eligibility checking without LLM round trip.
    Use this when you want deterministic eligibility results.
    
    The agent can also call this same function during conversations.
    """
    try:
        # Convert profile to dict
        profile_dict = request.user_profile.dict()
        
        # Call tool directly
        result = check_eligibility(
            scheme_id=request.scheme_id,
            user_profile=profile_dict
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Eligibility check failed")
            )
        
        return EligibilityCheckResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error checking eligibility: {str(e)}"
        )


__all__ = ['router']

"""
Documents Router - Required documents listing
"""

from fastapi import APIRouter, HTTPException
from models.application import DocumentsRequest
from tools.documents import get_required_documents

router = APIRouter()


@router.get("/schemes/{scheme_id}/documents")
async def get_documents(scheme_id: str, user_category: str = None):
    """
    Get list of required documents for a scheme.
    Fast path without LLM - useful for UI to show document checklist.
    
    Query parameters:
    - user_category: Optional filter for category-specific documents (e.g., 'SC', 'Farmer')
    """
    try:
        result = get_required_documents(
            scheme_id=scheme_id,
            user_category=user_category
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Error fetching documents")
            )
        
        return {
            "success": True,
            **result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching documents: {str(e)}"
        )


@router.post("/schemes/{scheme_id}/documents")
async def get_documents_post(scheme_id: str, request: DocumentsRequest):
    """
    POST version of documents endpoint for complex requests.
    """
    try:
        result = get_required_documents(
            scheme_id=scheme_id,
            user_category=request.user_category
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Error fetching documents")
            )
        
        return {
            "success": True,
            **result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching documents: {str(e)}"
        )


__all__ = ['router']

"""
Profile Router - User profile management
"""

from fastapi import APIRouter, HTTPException
from models.user_profile import UserProfile, ProfileUpdate
from typing import Dict

router = APIRouter()

# In-memory profile storage (for hackathon)
# In production, use a database
user_profiles: Dict[str, UserProfile] = {}


@router.post("/profile")
async def create_or_update_profile(profile: UserProfile, user_id: str = None):
    """
    Create or update user profile.
    Profile data is used for eligibility checks and application generation.
    """
    try:
        # Generate user_id if not provided
        if not user_id:
            import uuid
            user_id = f"user_{uuid.uuid4().hex[:8]}"
        
        # Store profile
        user_profiles[user_id] = profile
        
        return {
            "success": True,
            "user_id": user_id,
            "message": "Profile saved successfully",
            "profile": profile.dict()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving profile: {str(e)}"
        )


@router.get("/profile/{user_id}")
async def get_profile(user_id: str):
    """Get user profile by user_id"""
    
    if user_id not in user_profiles:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )
    
    return {
        "success": True,
        "user_id": user_id,
        "profile": user_profiles[user_id].dict()
    }


@router.patch("/profile/{user_id}")
async def update_profile(user_id: str, updates: ProfileUpdate):
    """Update specific fields in user profile"""
    
    if user_id not in user_profiles:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )
    
    # Update only provided fields
    current_profile = user_profiles[user_id]
    update_data = updates.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_profile, field, value)
    
    user_profiles[user_id] = current_profile
    
    return {
        "success": True,
        "user_id": user_id,
        "message": "Profile updated successfully",
        "updated_fields": list(update_data.keys()),
        "profile": current_profile.dict()
    }


@router.delete("/profile/{user_id}")
async def delete_profile(user_id: str):
    """Delete user profile"""
    
    if user_id not in user_profiles:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )
    
    del user_profiles[user_id]
    
    return {
        "success": True,
        "user_id": user_id,
        "message": "Profile deleted successfully"
    }


__all__ = ['router']

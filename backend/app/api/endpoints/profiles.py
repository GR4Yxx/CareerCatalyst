from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Any
from bson import ObjectId

from ...models.user import User
from ...models.profile import Profile, ProfileCreate, ProfileUpdate
from ...services import profile_service
from ..endpoints.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=Profile, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create a new profile for the current user.
    """
    # Ensure the user can only create a profile for themselves
    profile_data.user_id = ObjectId(current_user.id)
    
    try:
        profile = await profile_service.create_profile(profile_data)
        return profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=Profile)
async def get_my_profile(current_user: User = Depends(get_current_user)) -> Any:
    """
    Get the current user's profile.
    """
    profile = await profile_service.get_profile_by_user_id(current_user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile

@router.put("/me", response_model=Profile)
async def update_my_profile(
    profile_update: ProfileUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update the current user's profile.
    """
    # Get current profile
    profile = await profile_service.get_profile_by_user_id(current_user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Update profile
    updated_profile = await profile_service.update_profile(profile.id, profile_update)
    if not updated_profile:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )
    
    return updated_profile

@router.get("/{profile_id}", response_model=Profile)
async def get_profile(
    profile_id: str,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a profile by ID.
    """
    profile = await profile_service.get_profile_by_id(profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile 
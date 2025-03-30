from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from ..db.mongodb import get_database
from ..models.profile import ProfileCreate, ProfileInDB, Profile, ProfileUpdate

async def get_profile_by_user_id(user_id: str) -> Optional[Profile]:
    """Get a profile by user ID"""
    db = get_database()
    profile_data = await db["profiles"].find_one({"user_id": ObjectId(user_id)})
    
    if profile_data:
        return Profile(**profile_data)
    return None

async def get_profile_by_id(profile_id: str) -> Optional[Profile]:
    """Get a profile by profile ID"""
    db = get_database()
    profile_data = await db["profiles"].find_one({"_id": ObjectId(profile_id)})
    
    if profile_data:
        return Profile(**profile_data)
    return None

async def create_profile(profile: ProfileCreate) -> Profile:
    """Create a new profile"""
    db = get_database()
    
    # Check if profile already exists for this user
    existing_profile = await db["profiles"].find_one({"user_id": profile.user_id})
    if existing_profile:
        raise ValueError("Profile already exists for this user")
    
    # Create profile document
    profile_in_db = ProfileInDB(
        **profile.dict(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Insert into database
    result = await db["profiles"].insert_one(profile_in_db.dict(by_alias=True))
    
    # Get created profile
    created_profile = await db["profiles"].find_one({"_id": result.inserted_id})
    
    return Profile(**created_profile)

async def update_profile(profile_id: str, profile_update: ProfileUpdate) -> Optional[Profile]:
    """Update an existing profile"""
    db = get_database()
    
    # Check if profile exists
    profile = await get_profile_by_id(profile_id)
    if not profile:
        return None
    
    # Prepare update data
    update_data = profile_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    # Update profile
    await db["profiles"].update_one(
        {"_id": ObjectId(profile_id)},
        {"$set": update_data}
    )
    
    # Get updated profile
    updated_profile = await db["profiles"].find_one({"_id": ObjectId(profile_id)})
    
    return Profile(**updated_profile)

async def delete_profile(profile_id: str) -> bool:
    """Delete a profile"""
    db = get_database()
    
    result = await db["profiles"].delete_one({"_id": ObjectId(profile_id)})
    
    return result.deleted_count > 0

async def list_profiles(skip: int = 0, limit: int = 100) -> List[Profile]:
    """List profiles with pagination"""
    db = get_database()
    
    profiles = []
    cursor = db["profiles"].find().skip(skip).limit(limit)
    
    async for profile in cursor:
        profiles.append(Profile(**profile))
    
    return profiles 
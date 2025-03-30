from datetime import datetime, timedelta
from typing import Optional, List
from bson import ObjectId
from jose import jwt
from passlib.context import CryptContext
from ..core.config import settings
from ..db.mongodb import get_database
from ..models.user import UserCreate, UserInDB, User
from ..models.job import Job
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# User operations
async def get_user_by_email(email: str) -> Optional[UserInDB]:
    db = get_database()
    user = await db["users"].find_one({"email": email})
    if user:
        return UserInDB(**user)
    return None

async def get_user_by_id(user_id: str) -> Optional[UserInDB]:
    db = get_database()
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if user:
        return UserInDB(**user)
    return None

async def create_user(user: UserCreate) -> User:
    db = get_database()
    
    # Check if user already exists
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise ValueError("Email already registered")
    
    # Create new user
    user_in_db = UserInDB(
        **user.dict(),
        hashed_password=get_password_hash(user.password),
        created_at=datetime.utcnow()
    )
    
    # Insert into database
    new_user = await db["users"].insert_one(user_in_db.dict(by_alias=True, exclude={"id"}))
    
    # Get the created user
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    
    # Return user without password
    return User(
        _id=str(created_user["_id"]),
        email=created_user["email"],
        name=created_user["name"],
        created_at=created_user["created_at"],
        last_login=created_user.get("last_login")
    )

async def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
    user = await get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    # Update last login
    db = get_database()
    await db["users"].update_one(
        {"_id": ObjectId(user.id)},
        {"$set": {"last_login": datetime.utcnow()}}
    )
    
    return user

# Saved jobs functionality
async def get_saved_jobs(user_id: str) -> List[Job]:
    """
    Get all jobs saved by a user
    
    Args:
        user_id: ID of the user
        
    Returns:
        List of saved jobs
    """
    db = get_database()
    try:
        # Get user's saved job IDs
        user = await db["users"].find_one(
            {"_id": ObjectId(user_id)},
            {"saved_jobs": 1}
        )
        
        if not user or "saved_jobs" not in user or not user["saved_jobs"]:
            return []
            
        # Convert saved_jobs to a list of ObjectIds
        saved_job_ids = [ObjectId(job_id) for job_id in user["saved_jobs"]]
        
        # Fetch all the saved jobs
        jobs = []
        cursor = db["jobs"].find({"_id": {"$in": saved_job_ids}})
        
        async for job_doc in cursor:
            jobs.append(Job(**job_doc))
            
        return jobs
        
    except Exception as e:
        logger.error(f"Error getting saved jobs for user {user_id}: {str(e)}")
        return []

async def add_saved_job(user_id: str, job_id: str) -> bool:
    """
    Add a job to user's saved jobs
    
    Args:
        user_id: ID of the user
        job_id: ID of the job to save
        
    Returns:
        True if job was saved successfully, False otherwise
    """
    db = get_database()
    try:
        # Update user document, adding job_id to saved_jobs array if not already present
        result = await db["users"].update_one(
            {"_id": ObjectId(user_id), "saved_jobs": {"$ne": job_id}},
            {"$addToSet": {"saved_jobs": job_id}}
        )
        
        # Return true if document was modified (job was added)
        return result.modified_count > 0
        
    except Exception as e:
        logger.error(f"Error saving job {job_id} for user {user_id}: {str(e)}")
        return False

async def remove_saved_job(user_id: str, job_id: str) -> bool:
    """
    Remove a job from user's saved jobs
    
    Args:
        user_id: ID of the user
        job_id: ID of the job to remove
        
    Returns:
        True if job was removed successfully, False otherwise
    """
    db = get_database()
    try:
        # Update user document, removing job_id from saved_jobs array
        result = await db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"saved_jobs": job_id}}
        )
        
        # Return true if document was modified (job was removed)
        return result.modified_count > 0
        
    except Exception as e:
        logger.error(f"Error removing saved job {job_id} for user {user_id}: {str(e)}")
        return False 
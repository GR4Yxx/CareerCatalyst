from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId
from jose import jwt
from passlib.context import CryptContext
from ..core.config import settings
from ..db.mongodb import get_database
from ..models.user import UserCreate, UserInDB, User

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
from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from .user import PyObjectId

class ProfileBase(BaseModel):
    user_id: PyObjectId


class ProfileCreate(ProfileBase):
    pass


class ProfileInDB(ProfileBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Profile fields can be expanded as needed
    bio: Optional[str] = None
    job_title: Optional[str] = None
    location: Optional[str] = None
    industry: Optional[str] = None
    years_experience: Optional[int] = None
    education: Optional[List[Dict[str, Any]]] = None
    
    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
    
    @field_serializer('id')
    def serialize_id(self, id: PyObjectId) -> str:
        return str(id)
    
    @field_serializer('user_id')
    def serialize_user_id(self, user_id: PyObjectId) -> str:
        return str(user_id)


class Profile(ProfileBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime
    
    # Profile fields
    bio: Optional[str] = None
    job_title: Optional[str] = None
    location: Optional[str] = None
    industry: Optional[str] = None
    years_experience: Optional[int] = None
    education: Optional[List[Dict[str, Any]]] = None
    
    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True
    }


class ProfileUpdate(BaseModel):
    bio: Optional[str] = None
    job_title: Optional[str] = None
    location: Optional[str] = None
    industry: Optional[str] = None
    years_experience: Optional[int] = None
    education: Optional[List[Dict[str, Any]]] = None 
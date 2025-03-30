from pydantic import BaseModel, Field, field_serializer
from typing import Optional, Dict, Any, List
from datetime import datetime
from bson import ObjectId
from .user import PyObjectId

class ResumeBase(BaseModel):
    profile_id: PyObjectId
    original_filename: str
    file_type: str


class ResumeCreate(ResumeBase):
    pass


class ResumeInDB(ResumeBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    file_id: str  # Reference to GridFS file
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_current: bool = True
    parsed_content: Optional[Dict[str, Any]] = Field(default_factory=dict)

    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
    
    @field_serializer('id')
    def serialize_id(self, id: PyObjectId) -> str:
        return str(id)
    
    @field_serializer('profile_id')
    def serialize_profile_id(self, profile_id: PyObjectId) -> str:
        return str(profile_id)


class Resume(ResumeBase):
    id: str = Field(alias="_id")
    file_id: str
    created_at: datetime
    is_current: bool
    parsed_content: Optional[Dict[str, Any]] = {}

    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True
    }


class ResumeVersionBase(BaseModel):
    resume_id: PyObjectId
    job_id: PyObjectId
    version_name: str
    optimization_score: float = 0.0


class ResumeVersionCreate(ResumeVersionBase):
    optimized_content: Dict[str, Any]


class ResumeVersionInDB(ResumeVersionBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    optimized_content: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
    
    @field_serializer('id')
    def serialize_id(self, id: PyObjectId) -> str:
        return str(id)
    
    @field_serializer('resume_id')
    def serialize_resume_id(self, resume_id: PyObjectId) -> str:
        return str(resume_id)
    
    @field_serializer('job_id')
    def serialize_job_id(self, job_id: PyObjectId) -> str:
        return str(job_id)


class ResumeVersion(ResumeVersionBase):
    id: str = Field(alias="_id")
    optimized_content: Dict[str, Any]
    created_at: datetime

    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True
    }


class ResumeWithVersions(Resume):
    versions: List[ResumeVersion] = [] 
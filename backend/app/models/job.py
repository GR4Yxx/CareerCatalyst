from pydantic import BaseModel, Field, field_serializer
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId
from .user import PyObjectId

class JobBase(BaseModel):
    title: str
    company: str
    location: str
    url: str
    job_description: str
    
    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

class JobCreate(JobBase):
    pass

class JobInDB(JobBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
    extracted_skills: List[str] = []
    relevance_score: Optional[float] = None
    
    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
    
    @field_serializer('id')
    def serialize_id(self, id: PyObjectId) -> str:
        return str(id)

class Job(JobBase):
    id: str = Field(alias="_id")
    fetched_at: datetime
    extracted_skills: List[str] = []
    relevance_score: Optional[float] = None
    source: Optional[str] = None
    source_id: Optional[str] = None
    
    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True
    }

class JobRecommendation(BaseModel):
    id: str = Field(alias="_id")
    title: str
    company: str
    location: str
    url: str
    job_description: str
    fetched_at: datetime
    extracted_skills: List[str] = []
    relevance_score: Optional[float] = None
    match_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    source: Optional[str] = None
    source_id: Optional[str] = None
    match_explanation: Optional[str] = None
    
    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True
    } 
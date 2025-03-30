from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class SkillCategory(str, Enum):
    TECHNICAL = "technical"
    SOFT = "soft"
    DOMAIN = "domain"
    CERTIFICATION = "certification"

class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class Skill(BaseModel):
    id: Optional[str] = None
    name: str
    category: SkillCategory
    confidence: float = Field(ge=0.0, le=1.0)
    level: Optional[SkillLevel] = None
    description: Optional[str] = None

class UserSkill(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    profile_id: Optional[str] = None
    resume_id: str
    skills: List[Skill]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SkillAnalysisResult(BaseModel):
    technical_skills: List[Skill] = []
    soft_skills: List[Skill] = []
    domain_knowledge: List[Skill] = []
    certifications: List[Skill] = []
    
    def all_skills(self) -> List[Skill]:
        return self.technical_skills + self.soft_skills + self.domain_knowledge + self.certifications 
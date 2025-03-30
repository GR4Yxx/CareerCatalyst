from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List, Dict, Any, Optional

from ...models.user import User
from ...models.skill import Skill, UserSkill, SkillAnalysisResult
from ...services import skill_service, resume_service
from ..endpoints.auth import get_current_user

router = APIRouter()

@router.get("/resume/{resume_id}", response_model=Optional[UserSkill])
async def get_skills_by_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get skills extracted from a specific resume.
    """
    # Check if the resume exists and belongs to the user
    resume = await resume_service.get_resume_by_id(resume_id)
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found."
        )
    
    # Get skills
    skills = await skill_service.get_skills_by_resume(resume_id)
    return skills

@router.post("/analyze/{resume_id}", response_model=UserSkill)
async def analyze_resume_skills(
    resume_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """
    Manually trigger skill analysis for a resume.
    """
    # Check if the resume exists and belongs to the user
    resume = await resume_service.get_resume_by_id(resume_id)
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found."
        )
    
    # Get the resume file content
    file_data = await resume_service.download_resume(resume_id)
    
    if not file_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume file not found."
        )
    
    # Determine if linked to profile or user
    profile_id = getattr(resume, "profile_id", None)
    user_id = getattr(resume, "user_id", None) or current_user.id
    
    # Run skill analysis
    user_skill = await skill_service.analyze_resume_skills(
        resume_id=resume_id,
        file_content=file_data["content"],
        file_type=file_data["file_type"],
        profile_id=profile_id,
        user_id=user_id
    )
    
    return user_skill

@router.get("/user", response_model=List[UserSkill])
async def get_user_skills(
    current_user: User = Depends(get_current_user)
):
    """
    Get all skills for the current user.
    """
    skills = await skill_service.get_skills_by_user(current_user.id)
    return skills

@router.get("/profile/{profile_id}", response_model=List[UserSkill])
async def get_profile_skills(
    profile_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get all skills for a specific profile.
    """
    skills = await skill_service.get_skills_by_profile(profile_id)
    return skills 
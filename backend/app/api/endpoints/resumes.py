from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any, Optional
import io

from ...models.user import User
from ...models.resume import Resume, ResumeVersion, ResumeWithVersions
from ...services import resume_service, profile_service, skill_service
from ..endpoints.auth import get_current_user

router = APIRouter()

@router.post("/upload", response_model=Resume, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    profile_id: Optional[str] = Form(None),
    analyze_skills: bool = Form(True),
    background_tasks: BackgroundTasks = None,
    current_user: User = Depends(get_current_user)
):
    """
    Upload a new resume.
    If profile_id is provided, links to that profile, otherwise links directly to the user.
    Extracts and analyzes skills using Gemini if analyze_skills is True.
    """
    # Validate file type
    allowed_types = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain"
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF, Word, and text documents are allowed."
        )
    
    # Read file content
    file_content = await file.read()
    
    # Upload resume
    try:
        if profile_id:
            # Link to profile if provided
            resume = await resume_service.upload_resume(
                file_content=file_content,
                original_filename=file.filename,
                file_type=file.content_type,
                profile_id=profile_id
            )
            
            # Analyze skills if requested
            if analyze_skills:
                # Run skill analysis in background
                background_tasks.add_task(
                    skill_service.analyze_resume_skills,
                    resume_id=resume.id,
                    file_content=file_content,
                    file_type=file.content_type,
                    profile_id=profile_id
                )
        else:
            # Otherwise link directly to user
            resume = await resume_service.upload_resume(
                file_content=file_content,
                original_filename=file.filename,
                file_type=file.content_type,
                user_id=current_user.id
            )
            
            # Analyze skills if requested
            if analyze_skills:
                # Run skill analysis in background
                background_tasks.add_task(
                    skill_service.analyze_resume_skills,
                    resume_id=resume.id,
                    file_content=file_content,
                    file_type=file.content_type,
                    user_id=current_user.id
                )
        return resume
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/user/current", response_model=Resume)
async def get_current_user_resume(
    current_user: User = Depends(get_current_user)
):
    """
    Get the current resume for the authenticated user.
    """
    resume = await resume_service.get_current_resume(user_id=current_user.id)
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No current resume found for this user."
        )
    
    return resume

@router.get("/user", response_model=List[Resume])
async def get_user_resumes(
    current_user: User = Depends(get_current_user)
):
    """
    Get all resumes for the authenticated user.
    """
    resumes = await resume_service.get_resumes_by_user(current_user.id)
    return resumes

@router.get("/user/count", response_model=int)
async def get_user_resume_count(
    current_user: User = Depends(get_current_user)
):
    """
    Get the count of resumes for the authenticated user.
    """
    resumes = await resume_service.get_resumes_by_user(current_user.id)
    return len(resumes)

@router.get("/profile/{profile_id}", response_model=List[Resume])
async def get_resumes_by_profile(
    profile_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get all resumes for a profile.
    """
    resumes = await resume_service.get_resumes_by_profile(profile_id)
    return resumes

@router.get("/profile/{profile_id}/current", response_model=Resume)
async def get_current_resume(
    profile_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get the current resume for a profile.
    """
    resume = await resume_service.get_current_resume(profile_id)
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No current resume found for this profile."
        )
    
    return resume

@router.get("/{resume_id}", response_model=ResumeWithVersions)
async def get_resume_with_versions(
    resume_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a resume with all its versions.
    """
    resume = await resume_service.get_resume_with_versions(resume_id)
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found."
        )
    
    return resume

@router.get("/{resume_id}/download")
async def download_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Download a resume file.
    """
    file_data = await resume_service.download_resume(resume_id)
    
    if not file_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found or unable to download file."
        )
    
    # Create file-like object
    file_obj = io.BytesIO(file_data["content"])
    
    return StreamingResponse(
        file_obj,
        media_type=file_data["file_type"],
        headers={"Content-Disposition": f"attachment; filename={file_data['filename']}"}
    )

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a resume and all its versions.
    """
    result = await resume_service.delete_resume(resume_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found or unable to delete."
        )
    
    return None

@router.post("/{resume_id}/versions", response_model=ResumeVersion)
async def create_resume_version(
    resume_id: str,
    job_id: str,
    optimized_content: Dict[str, Any],
    version_name: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Create an optimized version of a resume for a specific job.
    """
    # Check if resume exists
    resume = await resume_service.get_resume_by_id(resume_id)
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found."
        )
    
    # Generate version name if not provided
    if not version_name:
        version_name = f"Version {len(await resume_service.get_resume_versions(resume_id)) + 1}"
    
    # Create resume version
    version = await resume_service.create_resume_version(
        resume_id=resume_id,
        job_id=job_id,
        optimized_content=optimized_content,
        version_name=version_name
    )
    
    return version 
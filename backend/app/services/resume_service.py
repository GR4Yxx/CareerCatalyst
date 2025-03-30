from datetime import datetime
from typing import Optional, List, Dict, Any, BinaryIO
from bson import ObjectId

from ..db.mongodb import get_database
from ..utils import gridfs
from ..models.resume import ResumeCreate, ResumeInDB, Resume, ResumeVersionCreate, ResumeVersionInDB, ResumeVersion, ResumeWithVersions

async def upload_resume(
    profile_id: str,
    file_content: bytes,
    original_filename: str,
    file_type: str
) -> Resume:
    """
    Upload a new resume for a profile
    """
    db = get_database()
    resumes_collection = db["resumes"]
    
    # Set all existing resumes for this profile to not current
    await resumes_collection.update_many(
        {"profile_id": ObjectId(profile_id)},
        {"$set": {"is_current": False}}
    )
    
    # Upload file to GridFS
    metadata = {
        "profile_id": profile_id,
        "file_type": file_type,
        "upload_date": datetime.utcnow()
    }
    
    file_id = await gridfs.upload_file(file_content, original_filename, metadata)
    
    # Create resume document
    resume_data = ResumeInDB(
        profile_id=ObjectId(profile_id),
        original_filename=original_filename,
        file_type=file_type,
        file_id=file_id,
        created_at=datetime.utcnow(),
        is_current=True,
        parsed_content={}  # Will be filled by parser service
    )
    
    # Insert into database
    result = await resumes_collection.insert_one(resume_data.dict(by_alias=True))
    
    # Get the created resume
    created_resume = await resumes_collection.find_one({"_id": result.inserted_id})
    
    return Resume(**created_resume)

async def get_current_resume(profile_id: str) -> Optional[Resume]:
    """
    Get the current resume for a profile
    """
    db = get_database()
    resumes_collection = db["resumes"]
    
    resume_data = await resumes_collection.find_one({
        "profile_id": ObjectId(profile_id),
        "is_current": True
    })
    
    if resume_data:
        return Resume(**resume_data)
    return None

async def get_resume_by_id(resume_id: str) -> Optional[Resume]:
    """
    Get a resume by its ID
    """
    db = get_database()
    resumes_collection = db["resumes"]
    
    resume_data = await resumes_collection.find_one({"_id": ObjectId(resume_id)})
    
    if resume_data:
        return Resume(**resume_data)
    return None

async def download_resume(resume_id: str) -> Optional[Dict[str, Any]]:
    """
    Download a resume file by resume ID
    """
    db = get_database()
    resumes_collection = db["resumes"]
    
    # Get the resume document
    resume_data = await resumes_collection.find_one({"_id": ObjectId(resume_id)})
    
    if not resume_data:
        return None
    
    # Download the file from GridFS
    file_content = await gridfs.download_file(resume_data["file_id"])
    
    if not file_content:
        return None
    
    return {
        "content": file_content,
        "filename": resume_data["original_filename"],
        "file_type": resume_data["file_type"]
    }

async def get_resumes_by_profile(profile_id: str) -> List[Resume]:
    """
    Get all resumes for a profile
    """
    db = get_database()
    resumes_collection = db["resumes"]
    
    cursor = resumes_collection.find({"profile_id": ObjectId(profile_id)}).sort("created_at", -1)
    resumes = await cursor.to_list(length=None)
    
    return [Resume(**resume) for resume in resumes]

async def delete_resume(resume_id: str) -> bool:
    """
    Delete a resume and its file
    """
    db = get_database()
    resumes_collection = db["resumes"]
    resume_versions_collection = db["resume_versions"]
    
    # Get the resume
    resume_data = await resumes_collection.find_one({"_id": ObjectId(resume_id)})
    
    if not resume_data:
        return False
    
    # Delete the file from GridFS
    result = await gridfs.delete_file(resume_data["file_id"])
    
    if not result:
        return False
    
    # Delete all resume versions
    await resume_versions_collection.delete_many({"resume_id": ObjectId(resume_id)})
    
    # Delete the resume document
    delete_result = await resumes_collection.delete_one({"_id": ObjectId(resume_id)})
    
    return delete_result.deleted_count > 0

async def create_resume_version(
    resume_id: str,
    job_id: str,
    optimized_content: Dict[str, Any],
    version_name: str
) -> ResumeVersion:
    """
    Create an optimized version of a resume for a specific job
    """
    db = get_database()
    resume_versions_collection = db["resume_versions"]
    
    version_data = ResumeVersionInDB(
        resume_id=ObjectId(resume_id),
        job_id=ObjectId(job_id),
        version_name=version_name,
        optimized_content=optimized_content,
        optimization_score=optimized_content.get("score", 0.0),
        created_at=datetime.utcnow()
    )
    
    result = await resume_versions_collection.insert_one(version_data.dict(by_alias=True))
    
    created_version = await resume_versions_collection.find_one({"_id": result.inserted_id})
    
    return ResumeVersion(**created_version)

async def get_resume_versions(resume_id: str) -> List[ResumeVersion]:
    """
    Get all versions of a resume
    """
    db = get_database()
    resume_versions_collection = db["resume_versions"]
    
    cursor = resume_versions_collection.find({"resume_id": ObjectId(resume_id)}).sort("created_at", -1)
    versions = await cursor.to_list(length=None)
    
    return [ResumeVersion(**version) for version in versions]

async def get_resume_with_versions(resume_id: str) -> Optional[ResumeWithVersions]:
    """
    Get a resume with all its versions
    """
    resume = await get_resume_by_id(resume_id)
    
    if not resume:
        return None
    
    versions = await get_resume_versions(resume_id)
    
    return ResumeWithVersions(
        **resume.dict(),
        versions=versions
    ) 
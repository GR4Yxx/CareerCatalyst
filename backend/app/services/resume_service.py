from datetime import datetime
from typing import Optional, List, Dict, Any, BinaryIO
from bson import ObjectId

from ..db.mongodb import get_database
from ..utils import gridfs
from ..models.resume import ResumeCreate, ResumeInDB, Resume, ResumeVersionCreate, ResumeVersionInDB, ResumeVersion, ResumeWithVersions

async def upload_resume(
    file_content: bytes,
    original_filename: str,
    file_type: str,
    profile_id: str = None,
    user_id: str = None
) -> Resume:
    """
    Upload a new resume for a profile or user
    """
    if not profile_id and not user_id:
        raise ValueError("Either profile_id or user_id must be provided")
    
    db = get_database()
    resumes_collection = db["resumes"]
    
    # Set all existing resumes to not current
    if profile_id:
        await resumes_collection.update_many(
            {"profile_id": ObjectId(profile_id)},
            {"$set": {"is_current": False}}
        )
    elif user_id:
        await resumes_collection.update_many(
            {"user_id": ObjectId(user_id)},
            {"$set": {"is_current": False}}
        )
    
    # Upload file to GridFS
    metadata = {
        "file_type": file_type,
        "upload_date": datetime.utcnow()
    }
    
    if profile_id:
        metadata["profile_id"] = profile_id
    if user_id:
        metadata["user_id"] = user_id
    
    file_id = await gridfs.upload_file(file_content, original_filename, metadata)
    
    # Create resume document
    resume_data = {
        "original_filename": original_filename,
        "file_type": file_type,
        "file_id": file_id,
        "created_at": datetime.utcnow(),
        "is_current": True,
        "parsed_content": {}  # Will be filled by parser service
    }
    
    if profile_id:
        resume_data["profile_id"] = ObjectId(profile_id)
    if user_id:
        resume_data["user_id"] = ObjectId(user_id)
    
    # Insert into database
    result = await resumes_collection.insert_one(resume_data)
    
    # Get the created resume
    created_resume = await resumes_collection.find_one({"_id": result.inserted_id})
    
    # Convert ObjectId fields to strings before passing to Resume model
    if created_resume:
        if "_id" in created_resume and isinstance(created_resume["_id"], ObjectId):
            created_resume["_id"] = str(created_resume["_id"])
        if "user_id" in created_resume and isinstance(created_resume["user_id"], ObjectId):
            created_resume["user_id"] = str(created_resume["user_id"])
        if "profile_id" in created_resume and isinstance(created_resume["profile_id"], ObjectId):
            created_resume["profile_id"] = str(created_resume["profile_id"])
    
    return Resume(**created_resume)

async def get_current_resume(profile_id: str = None, user_id: str = None) -> Optional[Resume]:
    """
    Get the current resume for a profile or user
    """
    if not profile_id and not user_id:
        raise ValueError("Either profile_id or user_id must be provided")
    
    db = get_database()
    resumes_collection = db["resumes"]
    
    query = {"is_current": True}
    if profile_id:
        query["profile_id"] = ObjectId(profile_id)
    elif user_id:
        query["user_id"] = ObjectId(user_id)
    
    resume_data = await resumes_collection.find_one(query)
    
    if resume_data:
        # Convert ObjectId fields to strings
        if "_id" in resume_data and isinstance(resume_data["_id"], ObjectId):
            resume_data["_id"] = str(resume_data["_id"])
        if "user_id" in resume_data and isinstance(resume_data["user_id"], ObjectId):
            resume_data["user_id"] = str(resume_data["user_id"])
        if "profile_id" in resume_data and isinstance(resume_data["profile_id"], ObjectId):
            resume_data["profile_id"] = str(resume_data["profile_id"])
        
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
        # Convert ObjectId fields to strings
        if "_id" in resume_data and isinstance(resume_data["_id"], ObjectId):
            resume_data["_id"] = str(resume_data["_id"])
        if "user_id" in resume_data and isinstance(resume_data["user_id"], ObjectId):
            resume_data["user_id"] = str(resume_data["user_id"])
        if "profile_id" in resume_data and isinstance(resume_data["profile_id"], ObjectId):
            resume_data["profile_id"] = str(resume_data["profile_id"])
        
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
    
    # Convert ObjectId fields to strings before passing to Resume model
    formatted_resumes = []
    for resume in resumes:
        # Manual conversion of MongoDB ObjectIds to strings
        if "_id" in resume and isinstance(resume["_id"], ObjectId):
            resume["_id"] = str(resume["_id"])
        if "user_id" in resume and isinstance(resume["user_id"], ObjectId):
            resume["user_id"] = str(resume["user_id"])
        if "profile_id" in resume and isinstance(resume["profile_id"], ObjectId):
            resume["profile_id"] = str(resume["profile_id"])
        
        formatted_resumes.append(Resume(**resume))
    
    return formatted_resumes

async def get_resumes_by_user(user_id: str) -> List[Resume]:
    """
    Get all resumes for a user
    """
    db = get_database()
    resumes_collection = db["resumes"]
    
    cursor = resumes_collection.find({"user_id": ObjectId(user_id)}).sort("created_at", -1)
    resumes = await cursor.to_list(length=None)
    
    # Convert ObjectId fields to strings before passing to Resume model
    formatted_resumes = []
    for resume in resumes:
        # Manual conversion of MongoDB ObjectIds to strings
        if "_id" in resume and isinstance(resume["_id"], ObjectId):
            resume["_id"] = str(resume["_id"])
        if "user_id" in resume and isinstance(resume["user_id"], ObjectId):
            resume["user_id"] = str(resume["user_id"])
        if "profile_id" in resume and isinstance(resume["profile_id"], ObjectId):
            resume["profile_id"] = str(resume["profile_id"])
        
        formatted_resumes.append(Resume(**resume))
    
    return formatted_resumes

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
    
    # Convert ObjectId fields to strings
    if created_version:
        if "_id" in created_version and isinstance(created_version["_id"], ObjectId):
            created_version["_id"] = str(created_version["_id"])
        if "resume_id" in created_version and isinstance(created_version["resume_id"], ObjectId):
            created_version["resume_id"] = str(created_version["resume_id"])
        if "job_id" in created_version and isinstance(created_version["job_id"], ObjectId):
            created_version["job_id"] = str(created_version["job_id"])
    
    return ResumeVersion(**created_version)

async def get_resume_versions(resume_id: str) -> List[ResumeVersion]:
    """
    Get all versions of a resume
    """
    db = get_database()
    resume_versions_collection = db["resume_versions"]
    
    cursor = resume_versions_collection.find({"resume_id": ObjectId(resume_id)}).sort("created_at", -1)
    versions = await cursor.to_list(length=None)
    
    # Convert ObjectId fields to strings before passing to ResumeVersion model
    formatted_versions = []
    for version in versions:
        # Manual conversion of MongoDB ObjectIds to strings
        if "_id" in version and isinstance(version["_id"], ObjectId):
            version["_id"] = str(version["_id"])
        if "resume_id" in version and isinstance(version["resume_id"], ObjectId):
            version["resume_id"] = str(version["resume_id"])
        if "job_id" in version and isinstance(version["job_id"], ObjectId):
            version["job_id"] = str(version["job_id"])
        
        formatted_versions.append(ResumeVersion(**version))
    
    return formatted_versions

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
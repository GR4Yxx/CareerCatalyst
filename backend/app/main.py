import os
from fastapi import FastAPI, HTTPException, Depends, Query
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import logging
from pathlib import Path
import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the root directory path and manually load the connection string
root_dir = Path(__file__).parent.parent
env_path = root_dir / '.env'

logger.info(f"Looking for .env file at: {env_path}")

# Manual parsing of .env file to get the MongoDB URI
try:
    with open(env_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if key == "MONGO_URI":
                        logger.info(f"Found MONGO_URI in file")
                        os.environ["MONGO_URI"] = "mongodb+srv://kpatil31:Careercatalyst@2025@careercatalyst.arcl63d.mongodb.net/?retryWrites=true&w=majority"
                except ValueError:
                    continue
except FileNotFoundError:
    logger.warning(f".env file not found at {env_path}")

# Also load using dotenv for other variables
load_dotenv(dotenv_path=env_path)

# Log configuration
logger.info(f"MONGO_DB_NAME: {os.getenv('MONGO_DB_NAME', 'CareerCatalyst')}")

# Connect to MongoDB
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(mongo_uri)
db_name = os.getenv('MONGO_DB_NAME', 'CareerCatalyst')
db = client[db_name]

# Check MongoDB connection
try:
    # Ping the database to check connection
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise Exception("Database connection failed")

app = FastAPI(title="Career System API")

# Helper function to convert ObjectId to string for JSON response
def object_id_to_str(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, ObjectId):
                obj[k] = str(v)
            elif isinstance(v, (dict, list)):
                object_id_to_str(v)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, ObjectId):
                obj[i] = str(v)
            elif isinstance(v, (dict, list)):
                object_id_to_str(v)
    return obj

# Pydantic models for validation
class User(BaseModel):
    email: str
    name: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    last_login: Optional[datetime.datetime] = None

class UserInDB(User):
    id: str = Field(alias="_id")

class Profile(BaseModel):
    user_id: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

class Skill(BaseModel):
    name: str
    category: str
    subcategory: str
    taxonomy_id: str

class UserSkill(BaseModel):
    profile_id: str
    skill_id: str
    skill_name: str
    category: str
    subcategory: str
    confidence_score: float
    experience_years: float
    last_used: str
    context: List[str]

class Resume(BaseModel):
    profile_id: str
    original_filename: str
    file_path: str
    file_type: str
    parsed_content: Dict[str, Any]
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    is_current: bool = True

class ResumeVersion(BaseModel):
    resume_id: str
    job_id: str
    version_name: str
    optimized_content: Dict[str, Any]
    optimization_score: float
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

class Job(BaseModel):
    title: str
    company: str
    location: str
    description: str
    requirements: Dict[str, Any]
    salary_range: Dict[str, Any]
    source: str
    source_id: str
    posted_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    expiration_date: Optional[datetime.datetime] = None
    cached_until: Optional[datetime.datetime] = None

class UserJobInteraction(BaseModel):
    user_id: str
    job_id: str
    status: str
    match_score: float
    application_date: Optional[datetime.datetime] = None
    application_method: Optional[str] = None
    follow_up_reminder: Optional[datetime.datetime] = None
    notes: Optional[str] = None
    optimized_resume_version_id: Optional[str] = None

class CareerPath(BaseModel):
    name: str
    industry: str
    roles: List[str]

class UserCareerPlan(BaseModel):
    user_id: str
    current_role: str
    target_role: str
    selected_path_id: str
    customized_path: Dict[str, Any]
    skill_goals: List[str]
    timeline: Dict[str, Any]
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

class SkillRelationship(BaseModel):
    source_skill_id: str
    target_skill_id: str
    relationship_type: str
    strength: float

# Generic response model
class ResponseModel(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None

# API Endpoints for Users
@app.post("/users", response_model=ResponseModel)
async def create_user(user: User):
    try:
        result = db.users.insert_one(user.dict())
        return {
            "success": True,
            "data": {"id": str(result.inserted_id)},
            "message": "User created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}", response_model=ResponseModel)
async def get_user(user_id: str):
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user = object_id_to_str(user)
        return {
            "success": True,
            "data": user,
            "message": "User retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error retrieving user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users", response_model=ResponseModel)
async def get_users(skip: int = 0, limit: int = 10):
    try:
        users = list(db.users.find().skip(skip).limit(limit))
        users = object_id_to_str(users)
        return {
            "success": True,
            "data": users,
            "message": f"Retrieved {len(users)} users"
        }
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# API Endpoints for Skills
@app.post("/skills", response_model=ResponseModel)
async def create_skill(skill: Skill):
    try:
        result = db.skills.insert_one(skill.dict())
        return {
            "success": True,
            "data": {"id": str(result.inserted_id)},
            "message": "Skill created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating skill: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/skills", response_model=ResponseModel)
async def get_skills(category: Optional[str] = None, skip: int = 0, limit: int = 10):
    try:
        query = {}
        if category:
            query["category"] = category
            
        skills = list(db.skills.find(query).skip(skip).limit(limit))
        skills = object_id_to_str(skills)
        return {
            "success": True,
            "data": skills,
            "message": f"Retrieved {len(skills)} skills"
        }
    except Exception as e:
        logger.error(f"Error retrieving skills: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# API Endpoints for User Skills
@app.post("/user-skills", response_model=ResponseModel)
async def create_user_skill(user_skill: UserSkill):
    try:
        result = db.user_skills.insert_one(user_skill.dict())
        return {
            "success": True,
            "data": {"id": str(result.inserted_id)},
            "message": "User skill created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating user skill: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user-skills/profile/{profile_id}", response_model=ResponseModel)
async def get_user_skills_by_profile(profile_id: str):
    try:
        skills = list(db.user_skills.find({"profile_id": profile_id}))
        skills = object_id_to_str(skills)
        return {
            "success": True,
            "data": skills,
            "message": f"Retrieved {len(skills)} skills for profile"
        }
    except Exception as e:
        logger.error(f"Error retrieving user skills: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# API Endpoints for Jobs
@app.post("/jobs", response_model=ResponseModel)
async def create_job(job: Job):
    try:
        result = db.jobs.insert_one(job.dict())
        return {
            "success": True,
            "data": {"id": str(result.inserted_id)},
            "message": "Job created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs", response_model=ResponseModel)
async def get_jobs(
    title: Optional[str] = None, 
    company: Optional[str] = None, 
    location: Optional[str] = None,
    skip: int = 0, 
    limit: int = 10
):
    try:
        query = {}
        if title:
            query["title"] = {"$regex": title, "$options": "i"}
        if company:
            query["company"] = {"$regex": company, "$options": "i"}
        if location:
            query["location"] = {"$regex": location, "$options": "i"}
            
        jobs = list(db.jobs.find(query).skip(skip).limit(limit))
        jobs = object_id_to_str(jobs)
        return {
            "success": True,
            "data": jobs,
            "message": f"Retrieved {len(jobs)} jobs"
        }
    except Exception as e:
        logger.error(f"Error retrieving jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# API Endpoints for User Job Interactions
@app.post("/user-job-interactions", response_model=ResponseModel)
async def create_user_job_interaction(interaction: UserJobInteraction):
    try:
        result = db.user_job_interactions.insert_one(interaction.dict())
        return {
            "success": True,
            "data": {"id": str(result.inserted_id)},
            "message": "User job interaction created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating user job interaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user-job-interactions/user/{user_id}", response_model=ResponseModel)
async def get_user_job_interactions(
    user_id: str,
    status: Optional[str] = None,
    skip: int = 0, 
    limit: int = 10
):
    try:
        query = {"user_id": user_id}
        if status:
            query["status"] = status
            
        interactions = list(db.user_job_interactions.find(query).skip(skip).limit(limit))
        interactions = object_id_to_str(interactions)
        
        # Fetch job details for each interaction
        for interaction in interactions:
            if "job_id" in interaction:
                job = db.jobs.find_one({"_id": ObjectId(interaction["job_id"])})
                if job:
                    interaction["job_details"] = object_id_to_str(job)
        
        return {
            "success": True,
            "data": interactions,
            "message": f"Retrieved {len(interactions)} job interactions"
        }
    except Exception as e:
        logger.error(f"Error retrieving user job interactions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# API Endpoints for Career Paths
@app.post("/career-paths", response_model=ResponseModel)
async def create_career_path(career_path: CareerPath):
    try:
        result = db.career_paths.insert_one(career_path.dict())
        return {
            "success": True,
            "data": {"id": str(result.inserted_id)},
            "message": "Career path created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating career path: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/career-paths", response_model=ResponseModel)
async def get_career_paths(industry: Optional[str] = None):
    try:
        query = {}
        if industry:
            query["industry"] = {"$regex": industry, "$options": "i"}
            
        paths = list(db.career_paths.find(query))
        paths = object_id_to_str(paths)
        return {
            "success": True,
            "data": paths,
            "message": f"Retrieved {len(paths)} career paths"
        }
    except Exception as e:
        logger.error(f"Error retrieving career paths: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# API Endpoints for User Career Plans
@app.post("/user-career-plans", response_model=ResponseModel)
async def create_user_career_plan(plan: UserCareerPlan):
    try:
        result = db.user_career_plans.insert_one(plan.dict())
        return {
            "success": True,
            "data": {"id": str(result.inserted_id)},
            "message": "User career plan created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating user career plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user-career-plans/{user_id}", response_model=ResponseModel)
async def get_user_career_plan(user_id: str):
    try:
        plan = db.user_career_plans.find_one({"user_id": user_id})
        if not plan:
            raise HTTPException(status_code=404, detail="Career plan not found")
        
        plan = object_id_to_str(plan)
        
        # Fetch career path details
        if "selected_path_id" in plan:
            path = db.career_paths.find_one({"_id": ObjectId(plan["selected_path_id"])})
            if path:
                plan["career_path_details"] = object_id_to_str(path)
        
        return {
            "success": True,
            "data": plan,
            "message": "Career plan retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error retrieving user career plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        # Check MongoDB connection
        client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service Unavailable")

# Setup database function to create collections and indexes
@app.on_event("startup")
async def setup_database():
    try:
        # Create indexes
        db.users.create_index("email", unique=True)
        db.profiles.create_index("user_id", unique=True)
        db.user_skills.create_index([("profile_id", 1), ("skill_id", 1)], unique=True)
        db.resumes.create_index([("profile_id", 1), ("is_current", 1)])
        db.jobs.create_index("posted_date")
        db.user_job_interactions.create_index([("user_id", 1), ("job_id", 1)], unique=True)
        
        logger.info("Database setup complete")
    except Exception as e:
        logger.error(f"Error setting up database: {e}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
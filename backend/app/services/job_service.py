import os
import re
import logging
import requests
from time import sleep
from datetime import datetime
from typing import List, Dict, Set, Any, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from ..db.mongodb import get_database
from ..models.job import Job, JobInDB, JobCreate, JobRecommendation
from ..models.skill import UserSkill, Skill

# Set up logging
logger = logging.getLogger(__name__)

# API configuration
JSEARCH_API_URL = "https://jsearch.p.rapidapi.com/search"
JSEARCH_API_KEY = os.getenv("JSEARCH_API_KEY", "5e52392064msh7bca40c300ae3b2p1f89edjsn59c83a4b877e")
JSEARCH_HEADERS = {
    "X-RapidAPI-Key": JSEARCH_API_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

# Collection names
JOBS_COLLECTION = "jobs"

async def fetch_jobs(query: str, max_pages: int = 1, remote_only: bool = False) -> List[JobInDB]:
    """
    Fetch jobs from the JSearch API
    
    Args:
        query: The search query for jobs
        max_pages: Maximum number of pages to fetch
        remote_only: Whether to fetch only remote jobs
        
    Returns:
        List of job documents
    """
    db = get_database()
    jobs = []
    
    logger.info(f"Fetching jobs with query: {query}, max_pages: {max_pages}, remote_only: {remote_only}")
    
    for page in range(1, max_pages + 1):
        params = {
            "query": query,
            "page": page,
            "remote_jobs_only": "true" if remote_only else "false"
        }
        
        try:
            logger.info(f"Making API request for page {page}")
            res = requests.get(JSEARCH_API_URL, headers=JSEARCH_HEADERS, params=params)
            res.raise_for_status()
            data = res.json()
            
            for job_data in data.get("data", []):
                job = JobInDB(
                    title=job_data.get("job_title", ""),
                    company=job_data.get("employer_name", ""),
                    location=job_data.get("job_city", "") or job_data.get("job_country", ""),
                    url=job_data.get("job_apply_link", ""),
                    job_description=job_data.get("job_description", "")[:1000],  # Limit description length
                    fetched_at=datetime.utcnow(),
                    extracted_skills=extract_skills_from_job(job_data.get("job_description", ""))
                )
                jobs.append(job)
                
            logger.info(f"Fetched {len(data.get('data', []))} jobs from page {page}")
            
        except Exception as e:
            logger.error(f"Error fetching jobs for query '{query}' page {page}: {str(e)}")
        
        # Sleep to avoid hitting rate limits
        sleep(1)
    
    return jobs

def extract_skills_from_job(job_description: str) -> List[str]:
    """
    Extract potential skills from job description using a simple keyword matching approach
    
    Args:
        job_description: Text of the job description
        
    Returns:
        List of extracted skills
    """
    # A subset of common skills to match in job descriptions
    common_skills = [
        # Programming Languages
        "Python", "JavaScript", "TypeScript", "Java", "C#", "C\\+\\+", "Go", "Ruby", "PHP", "Swift", "Kotlin",
        # Web Development
        "React", "Angular", "Vue.js", "Node.js", "Express", "Django", "Flask", "FastAPI",
        "HTML", "CSS", "SASS", "LESS", "Bootstrap", "Tailwind CSS",
        # Cloud & DevOps
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CI/CD", "Jenkins", "GitHub Actions",
        # Databases
        "SQL", "MongoDB", "PostgreSQL", "MySQL", "SQLite", "Redis", "Elasticsearch",
        # Data Science & AI
        "Machine Learning", "Deep Learning", "NLP", "TensorFlow", "PyTorch", "Keras", "scikit-learn",
        "Data Analysis", "Data Visualization", "Pandas", "NumPy", "Matplotlib", "Tableau", "Power BI",
        # Soft Skills
        "Communication", "Leadership", "Teamwork", "Problem Solving", "Critical Thinking",
        "Time Management", "Adaptability", "Creativity", "Emotional Intelligence"
    ]
    
    extracted_skills = set()
    
    # Convert description to lowercase for case-insensitive matching
    description_lower = job_description.lower()
    
    for skill in common_skills:
        # Create pattern for whole word matching
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, description_lower):
            extracted_skills.add(skill)
    
    return list(extracted_skills)

async def save_jobs(jobs: List[JobInDB]) -> int:
    """
    Save jobs to the database, avoiding duplicates based on URL
    
    Args:
        jobs: List of job documents to save
        
    Returns:
        Number of jobs successfully saved
    """
    db = get_database()
    inserted_count = 0
    
    for job in jobs:
        # Check if job already exists by URL
        existing_job = await db[JOBS_COLLECTION].find_one({"url": job.url})
        
        if not existing_job:
            try:
                result = await db[JOBS_COLLECTION].insert_one(job.model_dump(by_alias=True))
                if result.inserted_id:
                    inserted_count += 1
            except Exception as e:
                logger.error(f"Error saving job {job.title}: {str(e)}")
    
    return inserted_count

async def get_all_jobs(limit: int = 100, skip: int = 0) -> List[Job]:
    """
    Get all jobs from the database with pagination
    
    Args:
        limit: Maximum number of jobs to return
        skip: Number of jobs to skip
        
    Returns:
        List of jobs
    """
    db = get_database()
    cursor = db[JOBS_COLLECTION].find().sort("fetched_at", -1).skip(skip).limit(limit)
    
    jobs = []
    async for doc in cursor:
        jobs.append(Job(**doc))
    
    return jobs

async def search_jobs(query: str, limit: int = 100) -> List[Job]:
    """
    Search jobs by query in title or description
    
    Args:
        query: Search query
        limit: Maximum number of jobs to return
        
    Returns:
        List of matching jobs
    """
    db = get_database()
    # Create text index if it doesn't exist
    await db[JOBS_COLLECTION].create_index([("title", "text"), ("job_description", "text")])
    
    cursor = db[JOBS_COLLECTION].find({"$text": {"$search": query}}).limit(limit)
    
    jobs = []
    async for doc in cursor:
        jobs.append(Job(**doc))
    
    return jobs

async def get_job_by_id(job_id: str) -> Optional[Job]:
    """
    Get a job by ID
    
    Args:
        job_id: ID of the job to get
        
    Returns:
        Job document or None if not found
    """
    db = get_database()
    try:
        doc = await db[JOBS_COLLECTION].find_one({"_id": ObjectId(job_id)})
        if doc:
            return Job(**doc)
        return None
    except Exception as e:
        logger.error(f"Error getting job {job_id}: {str(e)}")
        return None

async def get_recommended_jobs(user_skill: UserSkill, limit: int = 10) -> List[JobRecommendation]:
    """
    Get job recommendations based on user skills
    
    Args:
        user_skill: User's skills
        limit: Maximum number of recommendations to return
        
    Returns:
        List of job recommendations sorted by match score
    """
    db = get_database()
    recommendations = []
    
    # Get list of user's skill names
    user_skill_names = [skill.name for skill in user_skill.skills]
    
    # Find all jobs
    cursor = db[JOBS_COLLECTION].find().limit(100)  # Limit to recent 100 jobs for efficiency
    
    async for doc in cursor:
        job = Job(**doc)
        
        # Calculate matching skills
        job_skills = set(job.extracted_skills)
        user_skills = set(user_skill_names)
        
        matching_skills = list(job_skills.intersection(user_skills))
        missing_skills = list(job_skills - user_skills)
        
        # Calculate match score (percentage of job skills matched by user)
        if job_skills:
            match_score = len(matching_skills) / len(job_skills)
        else:
            match_score = 0
        
        # Create recommendation if there's at least one matching skill
        if matching_skills:
            recommendations.append(
                JobRecommendation(
                    job=job,
                    match_score=match_score,
                    matching_skills=matching_skills,
                    missing_skills=missing_skills
                )
            )
    
    # Sort recommendations by match score (highest first)
    recommendations.sort(key=lambda x: x.match_score, reverse=True)
    
    return recommendations[:limit]

async def run_job_scraper(queries: List[str] = None, max_pages: int = 1) -> Dict[str, Any]:
    """
    Run the job scraper on multiple queries and save results to database
    
    Args:
        queries: List of queries to search for (defaults to basic queries if None)
        max_pages: Maximum pages to fetch per query
        
    Returns:
        Dict with results summary
    """
    if queries is None:
        # Default to tech roles if no queries provided
        queries = [
            "software engineer", 
            "data scientist", 
            "web developer",
            "machine learning",
            "devops engineer",
            "cloud architect"
        ]
    
    total_fetched = 0
    total_saved = 0
    
    for query in queries:
        jobs = await fetch_jobs(query=query, max_pages=max_pages)
        total_fetched += len(jobs)
        
        if jobs:
            saved = await save_jobs(jobs)
            total_saved += saved
            logger.info(f"Saved {saved} new jobs for query '{query}'")
    
    return {
        "total_fetched": total_fetched,
        "total_saved": total_saved,
        "queries_processed": len(queries)
    } 
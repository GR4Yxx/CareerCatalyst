import os
import re
import json
import logging
import requests
from time import sleep
from datetime import datetime
from typing import List, Dict, Set, Any, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
import hashlib

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

# Create indexes when module is imported
async def create_indexes():
    """Create necessary indexes for jobs collection"""
    db = get_database()
    try:
        logger.info("Creating indexes for jobs collection...")
        # Index on source and source_id for deduplication
        await db[JOBS_COLLECTION].create_index([("source", 1), ("source_id", 1)], unique=True)
        # Text index on title and job_description for searching
        await db[JOBS_COLLECTION].create_index([("title", "text"), ("job_description", "text")])
        logger.info("Indexes created successfully")
    except Exception as e:
        logger.error(f"Error creating indexes: {str(e)}")

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

async def match_jobs_with_gemini(user_skills: List[Skill], jobs: List[Job], limit: int = 5) -> List[JobRecommendation]:
    """
    Use Gemini to analyze the match between user skills and job postings
    
    Args:
        user_skills: List of user skills
        jobs: List of job postings to evaluate
        limit: Maximum number of recommendations to return
        
    Returns:
        List of JobRecommendation objects sorted by match score
    """
    # Load Gemini API key
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        logger.warning("GEMINI_API_KEY not found in environment. Using basic job matching.")
        return await basic_job_matching(user_skills, jobs, limit)

    try:
        # Import and configure Gemini
        import google.generativeai as genai
        print(f"Configured Gemini with API key: {gemini_api_key[:4]}...{gemini_api_key[-4:]}")
        genai.configure(api_key=gemini_api_key)
        
        # Try to use the most capable model available
        try:
            model = genai.GenerativeModel('gemini-1.5-pro')
        except Exception as e:
            logger.warning(f"Error with gemini-1.5-pro model: {str(e)}. Trying gemini-pro...")
            try:
                model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                logger.error(f"Error with gemini-pro model: {str(e)}. Falling back to basic matching.")
                return await basic_job_matching(user_skills, jobs, limit)
        
        recommendations = []
        
        # Process each job (limit batch size to avoid overloading the API)
        batch_size = min(10, len(jobs))
        for i in range(0, min(len(jobs), 20), batch_size):
            batch_jobs = jobs[i:i+batch_size]
            batch_results = await process_job_batch_with_gemini(model, user_skills, batch_jobs)
            recommendations.extend(batch_results)
        
        # Sort by match score and return top recommendations
        recommendations.sort(key=lambda x: x.match_score, reverse=True)
        return recommendations[:limit]
    
    except Exception as e:
        logger.error(f"Error using Gemini for job matching: {str(e)}")
        return await basic_job_matching(user_skills, jobs, limit)

async def process_job_batch_with_gemini(model, user_skills: List[Skill], jobs: List[Job]) -> List[JobRecommendation]:
    """Process a batch of jobs with Gemini to evaluate matches"""
    
    # Extract skill names from skill objects
    skill_names = [skill.name for skill in user_skills]
    skill_text = ", ".join(skill_names)
    
    # Prepare job data
    job_data = []
    for i, job in enumerate(jobs):
        job_info = {
            "id": i,  # Use index as temporary ID for the prompt
            "title": job.title,
            "company": job.company,
            "extracted_skills": job.extracted_skills,
            "description_summary": job.job_description[:1000] if job.job_description else ""  # Limit length for API
        }
        job_data.append(job_info)
    
    job_data_json = json.dumps(job_data)
    
    # Create the prompt for Gemini
    prompt = f"""
    You are an expert career advisor and job matcher. Your task is to evaluate how well a candidate's skills match with job postings.
    
    USER SKILLS:
    {skill_text}
    
    JOB POSTINGS (in JSON format):
    {job_data_json}
    
    For each job, provide:
    1. A match score between 0.0 and 1.0 (where 1.0 is a perfect match)
    2. List of matching skills that the candidate has
    3. List of important missing skills the candidate would need
    4. A brief explanation of why this job is a good match (or not)
    
    Consider both explicit skill matches and implicit matches where skills might be related or transferable.
    
    Return your analysis as a JSON array with one object per job, using this format:
    [
      {{
        "job_id": 0,
        "match_score": 0.85,
        "matching_skills": ["Skill1", "Skill2", "Skill3"],
        "missing_skills": ["Skill4", "Skill5"],
        "match_explanation": "Brief explanation of match quality"
      }},
      // more job entries...
    ]
    
    Respond ONLY with the JSON array, no other text.
    """
    
    try:
        # Get response from Gemini
        logger.info("Sending job matching request to Gemini API")
        response = model.generate_content(prompt)
        
        if hasattr(response, 'text'):
            response_text = response.text
        else:
            response_text = str(response)
        
        # Extract JSON from response
        logger.debug(f"Raw Gemini response: {response_text[:200]}...")
        
        # Try to find JSON content in the response
        json_pattern = r'(\[.*\])'
        match = re.search(json_pattern, response_text, re.DOTALL)
        
        # Clean the string (remove any non-JSON parts)
        if match:
            json_str = match.group(1)
        else:
            # If pattern doesn't match, try to clean the response
            json_str = response_text.strip()
            # Remove markdown code blocks if present
            if json_str.startswith('```json'):
                json_str = json_str[7:]
            elif json_str.startswith('```'):
                json_str = json_str[3:]
            if json_str.endswith('```'):
                json_str = json_str[:-3]
        
        json_str = json_str.strip()
        logger.debug(f"Cleaned JSON string: {json_str[:200]}...")
        
        try:
            # Parse the analysis results
            analysis_results = json.loads(json_str)
            logger.info(f"Successfully parsed Gemini response into JSON with {len(analysis_results)} results")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {str(e)}")
            logger.debug(f"Problematic JSON string: {json_str}")
            return []
        
        # Create JobRecommendation objects
        recommendations = []
        for result in analysis_results:
            job_idx = result.get("job_id", 0)
            if job_idx < len(jobs):
                job = jobs[job_idx]
                
                try:
                    recommendation = JobRecommendation(
                        id=job.id,
                        title=job.title,
                        company=job.company,
                        location=job.location,
                        url=job.url,
                        job_description=job.job_description,
                        fetched_at=job.fetched_at,
                        extracted_skills=job.extracted_skills,
                        relevance_score=job.relevance_score,
                        match_score=float(result.get("match_score", 0)),
                        matching_skills=result.get("matching_skills", []),
                        missing_skills=result.get("missing_skills", []),
                        source=job.source,
                        source_id=job.source_id,
                        match_explanation=result.get("match_explanation", "")
                    )
                    recommendations.append(recommendation)
                except Exception as e:
                    logger.error(f"Error creating job recommendation: {str(e)}")
        
        return recommendations
    
    except Exception as e:
        logger.error(f"Error in Gemini job batch processing: {str(e)}")
        return []  # Return empty list on error

async def basic_job_matching(user_skills: List[Skill], jobs: List[Job], limit: int = 5) -> List[JobRecommendation]:
    """Basic job matching as fallback when Gemini is not available"""
    recommendations = []
    
    # Extract skill names
    skill_names = [skill.name for skill in user_skills]
    
    for job in jobs:
        job_text = ""
        if job.title:
            job_text += job.title.lower() + " "
        if job.company:
            job_text += job.company.lower() + " "
        if job.job_description:
            job_text += job.job_description.lower()
        
        # Calculate matching skills (case-insensitive match)
        matching_skills = []
        for skill in skill_names:
            # For better matching, consider variations of the skill name
            skill_variations = [
                skill.lower(),                      # exact match
                skill.lower().replace(" ", ""),     # without spaces
                skill.lower().replace(" ", "-"),    # with hyphens
                skill.lower().replace(".", ""),     # without dots
            ]
            
            for variation in skill_variations:
                if variation in job_text:
                    matching_skills.append(skill)
                    break
        
        # Deduplicate matching skills
        matching_skills = list(set(matching_skills))
        
        # Extract some keywords that might be missing skills
        common_skills = [
            "Python", "JavaScript", "Java", "React", "Angular", "Vue", "Node.js", 
            "SQL", "MongoDB", "Express", "Django", "Flask", "AWS", "Azure", "GCP", 
            "Docker", "Kubernetes", "CI/CD", "Git", "Agile", "TypeScript", "Redux",
            "REST API", "GraphQL", "NoSQL", "CSS", "HTML", "Spring", "Hibernate",
            "Microservices", "Unit Testing", "TDD", "Ruby", "Go", "Swift"
        ]
        
        missing_skills = []
        for skill in common_skills:
            skill_lower = skill.lower()
            if skill_lower in job_text and skill not in matching_skills:
                missing_skills.append(skill)
        
        # Limit to top 3 missing skills
        missing_skills = missing_skills[:3]
        
        # Calculate match score
        if matching_skills:
            match_score = len(matching_skills) / (len(matching_skills) + len(missing_skills)) if (len(matching_skills) + len(missing_skills)) > 0 else 0
            
            # Boost the score if critical skills are present in title
            if job.title:
                title_lower = job.title.lower()
                for skill in matching_skills:
                    if skill.lower() in title_lower:
                        match_score += 0.2  # Significant boost for matching title skills
                        break
            
            # Cap score at 1.0
            match_score = min(match_score, 1.0)
        else:
            match_score = 0
        
        try:
            # Create a JobRecommendation object
            recommendation = JobRecommendation(
                id=job.id,
                title=job.title,
                company=job.company,
                location=job.location,
                url=job.url,
                job_description=job.job_description,
                fetched_at=job.fetched_at,
                extracted_skills=job.extracted_skills,
                relevance_score=job.relevance_score,
                match_score=round(match_score, 2),
                matching_skills=matching_skills,
                missing_skills=missing_skills,
                source=job.source,
                source_id=job.source_id
            )
            recommendations.append(recommendation)
        except Exception as e:
            logger.error(f"Error creating job recommendation: {str(e)}")
    
    # Sort by match score
    recommendations.sort(key=lambda x: x.match_score, reverse=True)
    return recommendations[:limit] 
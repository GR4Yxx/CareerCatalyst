import asyncio
import aiohttp
import logging
import json
import sys
import os
import getpass
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Union
from pathlib import Path
import requests
import argparse
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# API Configuration 
# Use nginx endpoint for API calls
API_URL = "http://localhost"  # nginx proxy
# Direct backend access (fallback)
DIRECT_API_URL = "http://localhost:8000"  

# Set to True to use direct backend connection instead of nginx
USE_DIRECT_API = False

# Default credentials (you can override these when prompted)
DEFAULT_EMAIL = "xpjosh10@gmail.com"
DEFAULT_PASSWORD = "lol123456"

# Global variables
token = None
skill_names = []  # Make skill_names a global variable

async def get_credentials() -> tuple:
    """Prompt user for credentials with defaults"""
    print("\n=== Login to CareerCatalyst API ===")
    email = input(f"Email [{DEFAULT_EMAIL}]: ") or DEFAULT_EMAIL
    password = getpass.getpass(f"Password [use default]: ") or DEFAULT_PASSWORD
    return email, password

async def login(email: str, password: str) -> Optional[str]:
    """
    Login to the API and get a JWT token
    
    Args:
        email: User email
        password: User password
        
    Returns:
        JWT token if successful, None otherwise
    """
    logger.info(f"Logging in as {email}...")
    
    login_data = {
        "username": email,
        "password": password
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            # Try API gateway first
            try:
                async with session.post(f"{API_URL}/api/auth/login", data=login_data) as response:
                    if response.status == 200:
                        data = await response.json()
                        token = data.get("access_token")
                        if token:
                            logger.info("Login successful via API gateway")
                            print(f"Token: {token}")
                            return token
                        else:
                            logger.warning("Login response missing access_token")
                    else:
                        logger.warning(f"Login via API gateway failed: {response.status}")
            except Exception as e:
                logger.warning(f"API gateway login error: {str(e)}")
            
            # Try direct backend as fallback
            logger.info("Trying direct backend login...")
            try:
                # For direct backend, we need to use form data format
                form_data = aiohttp.FormData()
                form_data.add_field("username", email)
                form_data.add_field("password", password)
                
                async with session.post("http://localhost:8000/auth/login", data=form_data) as direct_response:
                    if direct_response.status == 200:
                        data = await direct_response.json()
                        token = data.get("access_token")
                        if token:
                            logger.info("Login successful via direct backend")
                            print(f"Token: {token}")
                            return token
                        else:
                            logger.error("Login response from direct backend missing access_token")
                    else:
                        logger.error(f"Direct backend login failed: {direct_response.status} - {await direct_response.text()}")
            except Exception as e:
                logger.error(f"Direct backend login error: {str(e)}")
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
    
    return None

async def get_user_resume(token: str) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Get the user's current resume
    
    Args:
        token: JWT token for authorization
        
    Returns:
        Tuple of resume info and resume ID if successful, (None, None) otherwise
    """
    logger.info("Fetching current resume...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            # Try direct backend first
            async with session.get(f"http://localhost:8000/resumes/current", headers=headers) as response:
                if response.status == 200:
                    resume_data = await response.json()
                    if resume_data:
                        resume_name = resume_data.get("file_name", "Unknown Resume")
                        resume_id = resume_data.get("_id")
                        logger.info(f"Got resume: {resume_name}")
                        logger.info(f"Got resume ID: {resume_id}")
                        return resume_data, resume_id
                    else:
                        logger.warning("No current resume found")
                else:
                    # Try API gateway as fallback
                    logger.warning(f"Direct backend resume fetch failed, trying API gateway...")
                    async with session.get(f"{API_URL}/api/resumes/current", headers=headers) as api_response:
                        if api_response.status == 200:
                            resume_data = await api_response.json()
                            if resume_data:
                                resume_name = resume_data.get("file_name", "Unknown Resume")
                                resume_id = resume_data.get("_id")
                                logger.info(f"Got resume: {resume_name}")
                                logger.info(f"Got resume ID: {resume_id}")
                                return resume_data, resume_id
                            else:
                                logger.warning("No current resume found via API gateway")
                        else:
                            logger.error(f"Failed to get resume: {api_response.status} - {await api_response.text()}")
    except Exception as e:
        logger.error(f"Error fetching resume: {str(e)}")
    
    return None, None

async def get_resume_skills(resume_id: str, token: str) -> Tuple[Optional[List[Dict]], List[str]]:
    """
    Get skills associated with a resume
    
    Args:
        resume_id: Resume ID to get skills for
        token: JWT token for authorization
        
    Returns:
        Tuple of skills list and skill names if successful, (None, []) otherwise
    """
    logger.info(f"Fetching skills for resume {resume_id}...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            # Try direct backend first
            async with session.get(f"http://localhost:8000/resumes/{resume_id}/skills", headers=headers) as response:
                if response.status == 200:
                    skills_data = await response.json()
                    if skills_data:
                        skill_names = [skill.get("name", "") for skill in skills_data]
                        logger.info(f"Got {len(skills_data)} skills")
                        logger.info(f"User skills: {', '.join(skill_names)}")
                        return skills_data, skill_names
                    else:
                        logger.warning("No skills found for resume")
                else:
                    # Try API gateway as fallback
                    logger.warning(f"Direct backend skills fetch failed, trying API gateway...")
                    async with session.get(f"{API_URL}/api/resumes/{resume_id}/skills", headers=headers) as api_response:
                        if api_response.status == 200:
                            skills_data = await api_response.json()
                            if skills_data:
                                skill_names = [skill.get("name", "") for skill in skills_data]
                                logger.info(f"Got {len(skills_data)} skills")
                                logger.info(f"User skills: {', '.join(skill_names)}")
                                return skills_data, skill_names
                            else:
                                logger.warning("No skills found for resume via API gateway")
                        else:
                            logger.error(f"Failed to get skills: {api_response.status} - {await api_response.text()}")
    except Exception as e:
        logger.error(f"Error fetching skills: {str(e)}")
    
    # If we couldn't get skills, return a test set
    logger.warning("Creating test skills since we couldn't fetch them")
    test_skills = [
        {"name": "Python", "confidence": 0.9},
        {"name": "JavaScript", "confidence": 0.85},
        {"name": "React", "confidence": 0.8},
        {"name": "Communication", "confidence": 0.95},
        {"name": "Problem Solving", "confidence": 0.9}
    ]
    skill_names = [skill["name"] for skill in test_skills]
    logger.info(f"Created test skills: {', '.join(skill_names)}")
    return test_skills, skill_names

async def search_jobs(session: aiohttp.ClientSession, token: str, query: str) -> Optional[List[Dict[str, Any]]]:
    """Search for jobs with a query string"""
    
    # Check if the jobs API endpoint exists
    api_base = DIRECT_API_URL if USE_DIRECT_API else API_URL
    jobs_endpoint = "/jobs" if USE_DIRECT_API else "/api/jobs"
    
    logger.info(f"Searching for jobs with query: {query}...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        params = {"query": query, "limit": 10}
        
        async with session.get(f"{api_base}{jobs_endpoint}", headers=headers, params=params) as response:
            if response.status != 200:
                # If 404, the endpoint might not exist yet
                if response.status == 404:
                    logger.warning("Jobs API endpoint not found")
                    return None
                
                error_text = await response.text()
                logger.error(f"Failed to search jobs with status {response.status}")
                logger.error(f"Error: {error_text}")
                return None
                
            data = await response.json()
            return data
    except Exception as e:
        logger.error(f"Error searching jobs: {str(e)}")
        return None

async def get_job_matches(session: aiohttp.ClientSession, token: str, resume_id: str) -> Optional[List[Dict[str, Any]]]:
    """Get job matches based on resume skills"""
    
    # Since there's no direct endpoint for job matches, we'll simulate by:
    # 1. Getting the skills from the resume
    # 2. Getting jobs and matching them based on skills
    
    # Get skills first
    skills_data, skill_names = await get_resume_skills(resume_id, token)
    if not skills_data:
        logger.error("Could not get skills data for job matching")
        return None
    
    # Now we construct a search query from the top skills (max 3)
    query_skills = skill_names[:3]
    search_query = " ".join(query_skills)
    
    # Search for jobs based on skills
    jobs = await search_jobs(session, token, search_query)
    
    if not jobs:
        # If jobs endpoint fails, we'll simulate a response for testing purposes
        logger.warning("No jobs API endpoint found. Simulating response...")
        matches = simulate_job_matches(skill_names)
        return matches
    
    return jobs

def simulate_job_matches(skills: List[str]) -> List[Dict[str, Any]]:
    """Simulate job matches based on skills (for testing when job API isn't available)"""
    
    logger.info("Generating simulated job matches based on user skills")
    
    # Create mapping of skills to relevant job types and missing skills
    skill_job_mapping = {
        "Python": {
            "jobs": ["Python Developer", "Data Scientist", "Backend Engineer", "ML Engineer"],
            "related_skills": ["Django", "Flask", "FastAPI", "NumPy", "Pandas", "TensorFlow", "PyTorch"]
        },
        "JavaScript": {
            "jobs": ["Frontend Developer", "Full Stack Developer", "Web Developer"],
            "related_skills": ["React", "Vue", "Angular", "Node.js", "Express"]
        },
        "Java": {
            "jobs": ["Java Developer", "Backend Engineer", "Android Developer"],
            "related_skills": ["Spring", "Hibernate", "Microservices", "Kafka"]
        },
        "C#": {
            "jobs": [".NET Developer", "Game Developer", "Windows Developer"],
            "related_skills": [".NET Core", "ASP.NET", "Unity", "WPF"]
        },
        "SQL": {
            "jobs": ["Database Administrator", "Data Analyst", "Backend Developer"],
            "related_skills": ["PostgreSQL", "MySQL", "Oracle", "SQL Server", "NoSQL"]
        },
        "AWS": {
            "jobs": ["Cloud Engineer", "DevOps Engineer", "Solutions Architect"],
            "related_skills": ["EC2", "S3", "Lambda", "CloudFormation", "Terraform"]
        },
        "Docker": {
            "jobs": ["DevOps Engineer", "Cloud Engineer", "Backend Developer"],
            "related_skills": ["Kubernetes", "CI/CD", "Jenkins", "GitLab CI"]
        },
        "React": {
            "jobs": ["Frontend Developer", "UI Developer", "Full Stack Developer"],
            "related_skills": ["Redux", "TypeScript", "Next.js", "React Native"]
        }
    }
    
    # Create a list of potential jobs based on user skills
    potential_jobs = []
    user_job_types = set()
    
    for skill in skills:
        if skill in skill_job_mapping:
            for job_type in skill_job_mapping[skill]["jobs"]:
                user_job_types.add(job_type)
    
    # Generate mock jobs for the relevant job types
    companies = ["TechCorp", "InnovateNow", "CodeFusion", "DataWorks", "CloudNative", "WebSolutions", "ByteForge", "NextGen Tech"]
    locations = ["Remote", "New York, NY", "San Francisco, CA", "Seattle, WA", "Austin, TX", "Boston, MA"]
    
    for job_type in user_job_types:
        # Make 1-2 mock jobs per job type
        for i in range(min(2, len(companies))):
            company = companies[i % len(companies)]
            location = locations[i % len(locations)]
            
            # Determine matching and missing skills
            matching_skills = []
            missing_skills = []
            
            # Add matching skills from the user's skills
            for skill in skills:
                if skill in skill_job_mapping and job_type in skill_job_mapping[skill]["jobs"]:
                    matching_skills.append(skill)
            
            # Add 2-3 missing skills that the user doesn't have
            for skill in skills:
                if skill in skill_job_mapping:
                    related_skills = skill_job_mapping[skill]["related_skills"]
                    for related in related_skills:
                        if related not in skills and related not in missing_skills:
                            missing_skills.append(related)
                            if len(missing_skills) >= 3:
                                break
            
            # Calculate match score based on ratio of matching to required skills
            total_required = len(matching_skills) + len(missing_skills)
            match_score = len(matching_skills) / total_required if total_required > 0 else 0
            
            job = {
                "id": str(len(potential_jobs) + 1),
                "title": f"{job_type} at {company}",
                "company": company,
                "location": location,
                "match_score": round(match_score, 2),
                "matching_skills": matching_skills,
                "missing_skills": missing_skills[:3]  # Limit to 3 missing skills
            }
            
            potential_jobs.append(job)
    
    # Sort by match score
    potential_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    
    # Return top 5 jobs
    return potential_jobs[:5]

async def display_match_results(job_matches: List[Dict[str, Any]]):
    """Display job match results in a formatted way"""
    
    print("\n")
    print("=" * 80)
    print(f"{'📊 JOB MATCHES BASED ON YOUR RESUME':^80}")
    print("=" * 80)
    
    for i, job in enumerate(job_matches):
        match_percent = int(job.get("match_score", 0) * 100)
        print(f"\n{'🏆' if i == 0 else '🔍'} Job Match #{i+1}: {job.get('title')}")
        print(f"   Company: {job.get('company', 'Unknown')}")
        print(f"   Location: {job.get('location', 'Not specified')}")
        print(f"   Match score: {match_percent}%")
        
        matching_skills = job.get("matching_skills", [])
        if matching_skills:
            print(f"   ✅ Matching skills: {', '.join(matching_skills)}")
        
        missing_skills = job.get("missing_skills", [])
        if missing_skills:
            print(f"   ❌ Missing skills: {', '.join(missing_skills)}")
        
        print(f"   {'⭐' * min(5, int(match_percent/20))}")
    
    print("\n" + "=" * 80)

async def find_job_recommendations(token: str, limit: int = 10, use_gemini: bool = True) -> List[Dict]:
    """
    Get job recommendations from the API
    
    Args:
        token: JWT token for authorization
        limit: Maximum number of recommendations to return
        use_gemini: Whether to use Gemini for enhanced matching
    
    Returns:
        List of job recommendations
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Using the recommendations endpoint with Gemini enabled
    try:
        url = f"http://localhost:8000/jobs/recommend?limit={limit}&use_gemini={str(use_gemini).lower()}"
        logger.info(f"Fetching job recommendations from: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    recommendations = await resp.json()
                    if recommendations and len(recommendations) > 0:
                        logger.info(f"Got {len(recommendations)} job recommendations")
                        return recommendations
                    else:
                        logger.warning("Recommendation endpoint returned no results")
                else:
                    logger.error(f"Failed to get recommendations: {resp.status} {await resp.text()}")
    except Exception as e:
        logger.error(f"Error fetching recommendations: {str(e)}")
    
    # Fall back to search endpoint if recommendations fail
    logger.info("Falling back to search endpoint")
    query = " ".join(skill_names[:3]) if len(skill_names) > 3 else " ".join(skill_names)
    
    try:
        url = f"http://localhost:8000/api/jobs/search?query={query}&limit={limit}"
        logger.info(f"Searching for jobs with query: {query}...")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    logger.error(f"Search failed: {resp.status} {await resp.text()}")
                    return []
    except Exception as e:
        logger.error(f"Error searching for jobs: {str(e)}")
        return []

def display_job_matches(job_matches: List[Dict]) -> None:
    """
    Display job matches with information on missing skills, matching skills,
    and a match explanation if available.
    
    Args:
        job_matches: List of job match dictionaries
    """
    if not job_matches or len(job_matches) == 0:
        print("\n❌ No job matches found.")
        return
    
    print("\n" + "=" * 80)
    print(" " * 23 + "📊 JOB MATCHES BASED ON YOUR RESUME")
    print("=" * 80)
    
    for i, job in enumerate(job_matches):
        # Highlight the first match, others are just regular
        prefix = "🏆" if i == 0 else "🔍"
        
        match_score = job.get("match_score", 0)
        match_percent = f"{int(match_score * 100)}%" if match_score is not None else "N/A"
        
        print(f"\n{prefix} Job Match #{i+1}: {job.get('title', 'Unknown Title')}")
        print(f"   Company: {job.get('company', 'Unknown Company')}")
        print(f"   Location: {job.get('location', 'Unknown Location')}")
        print(f"   Match score: {match_percent}")
        
        matching_skills = job.get('matching_skills', [])
        missing_skills = job.get('missing_skills', [])
        match_explanation = job.get('match_explanation', '')
        
        if matching_skills:
            print(f"   Matching skills: {', '.join(matching_skills)}")
        
        if missing_skills:
            print(f"   Missing skills: {', '.join(missing_skills)}")
        
        if match_explanation:
            print(f"   Match explanation: {match_explanation}")
        
        print("")
    
    print("=" * 80)

async def test_recommend_endpoint_directly(token: str) -> None:
    """
    Test the /jobs/recommend endpoint directly with Gemini
    
    Args:
        token: JWT token for authorization
    """
    logger.info("Testing the /jobs/recommend endpoint directly with Gemini...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            url = "http://localhost:8000/jobs/recommend?use_gemini=true"
            logger.info(f"Making request to: {url}")
            
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    recommendations = await response.json()
                    if recommendations and len(recommendations) > 0:
                        logger.info(f"Got {len(recommendations)} job recommendations")
                        
                        # Display the recommendations
                        print("\n" + "=" * 80)
                        print(" " * 20 + "🔍 DIRECT TEST OF JOB RECOMMENDATIONS WITH GEMINI")
                        print("=" * 80)
                        
                        display_job_matches(recommendations)
                    else:
                        logger.warning("Recommendation endpoint returned no results")
                else:
                    logger.error(f"Failed to get recommendations: {response.status} - {await response.text()}")
    except Exception as e:
        logger.error(f"Error testing recommend endpoint: {str(e)}")

async def main():
    """Main function to run the test"""
    try:
        print("\n🚀 Starting Resume to Jobs API Test\n")
        
        # Step 1: Get credentials and login
        email, password = await get_credentials()
        user_token = await login(email, password)
        if not user_token:
            logger.error("Failed to log in")
            return
        
        global token
        token = user_token
        
        # Test directly against the recommend endpoint
        await test_recommend_endpoint_directly(token)
        
        # Try to get resume and skills (may fail, but we'll continue with test skills)
        try:
            # Step 2: Get current resume
            resume_info, resume_id = await get_user_resume(token)
            
            # Step 3: Get skills from resume
            if resume_id:
                global skill_names
                user_skills, skill_names = await get_resume_skills(resume_id, token)
        except Exception as e:
            logger.warning(f"Error getting resume or skills: {str(e)}")
            logger.info("Continuing with test skills...")
        
        # Step 4: Get job recommendations using our skills
        logger.info(f"Fetching job recommendations using Gemini...")
        job_matches = await find_job_recommendations(token, limit=10, use_gemini=True)
        
        # Step 5: Display the results
        display_job_matches(job_matches)
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 
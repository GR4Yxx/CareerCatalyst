import asyncio
import logging
import json
import sys
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Add the parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent_dir)

# Import the job service functions
from app.services.job_service import fetch_jobs, save_jobs, extract_skills_from_job
from app.db.mongodb import connect_to_mongo, close_mongo_connection

async def test_fetch_jobs():
    """Test fetching jobs from the API"""
    logger.info("Testing fetch_jobs function...")
    
    # Test with a simple query
    query = "python developer"
    max_pages = 1
    
    logger.info(f"Fetching jobs for query: {query}, max_pages: {max_pages}")
    jobs = await fetch_jobs(query=query, max_pages=max_pages)
    
    logger.info(f"Fetched {len(jobs)} jobs")
    
    # Display sample of jobs
    if jobs:
        logger.info("Sample job:")
        sample_job = jobs[0]
        
        # Convert to dict for display
        sample_dict = {
            "title": sample_job.title,
            "company": sample_job.company,
            "location": sample_job.location,
            "url": sample_job.url,
            "description_snippet": sample_job.job_description[:100] + "...",
            "extracted_skills": sample_job.extracted_skills
        }
        
        logger.info(json.dumps(sample_dict, indent=2))
        
        return jobs
    else:
        logger.warning("No jobs fetched!")
        return []

async def test_extract_skills():
    """Test extracting skills from job descriptions"""
    logger.info("Testing skill extraction from job descriptions...")
    
    # Sample job descriptions
    job_descriptions = [
        """
        Requirements:
        - 3+ years of experience with Python
        - Experience with web frameworks such as Django or Flask
        - Knowledge of SQL and database design
        - Experience with JavaScript and React
        - Strong problem-solving skills and attention to detail
        """,
        """
        We are looking for a DevOps Engineer with:
        - Experience with AWS, Docker and Kubernetes
        - Knowledge of CI/CD pipelines
        - Experience with Infrastructure as Code (Terraform or CloudFormation)
        - Strong Linux administration skills
        - Good communication skills
        """
    ]
    
    for i, description in enumerate(job_descriptions):
        skills = extract_skills_from_job(description)
        logger.info(f"Job Description {i+1} - Extracted Skills: {skills}")

async def test_save_jobs():
    """Test saving jobs to the database"""
    logger.info("Testing saving jobs to the database...")
    
    # First fetch some jobs
    jobs = await test_fetch_jobs()
    
    if not jobs:
        logger.warning("No jobs to save, skipping save test")
        return
    
    # Save the jobs and check result
    saved_count = await save_jobs(jobs)
    logger.info(f"Saved {saved_count} new jobs to the database")

async def run_all_tests():
    """Run all job scraper tests"""
    logger.info("Starting job scraper tests...")
    
    # Connect to MongoDB
    await connect_to_mongo()
    
    try:
        # Test extracting skills
        await test_extract_skills()
        
        # Test fetching and saving jobs
        await test_save_jobs()
        
        logger.info("All tests completed!")
    
    except Exception as e:
        logger.error(f"Error during tests: {str(e)}")
    
    finally:
        # Close MongoDB connection
        await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(run_all_tests()) 
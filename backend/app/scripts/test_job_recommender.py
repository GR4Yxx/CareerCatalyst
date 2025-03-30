import asyncio
import logging
import json
import sys
import os
from datetime import datetime
from bson import ObjectId

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Add the parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent_dir)

# Import required models and services
from app.models.skill import Skill, UserSkill, SkillCategory
from app.services.job_service import get_recommended_jobs, run_job_scraper
from app.db.mongodb import connect_to_mongo, close_mongo_connection

async def create_test_user_skill():
    """Create a test UserSkill object for testing recommendations"""
    # Create a sample user skill profile
    skills = [
        Skill(name="Python", category=SkillCategory.TECHNICAL, confidence=0.95),
        Skill(name="JavaScript", category=SkillCategory.TECHNICAL, confidence=0.9),
        Skill(name="React", category=SkillCategory.TECHNICAL, confidence=0.85),
        Skill(name="SQL", category=SkillCategory.TECHNICAL, confidence=0.8),
        Skill(name="Docker", category=SkillCategory.TECHNICAL, confidence=0.7),
        Skill(name="AWS", category=SkillCategory.TECHNICAL, confidence=0.65),
        Skill(name="Communication", category=SkillCategory.SOFT, confidence=0.9),
        Skill(name="Problem Solving", category=SkillCategory.SOFT, confidence=0.85),
        Skill(name="Teamwork", category=SkillCategory.SOFT, confidence=0.8),
    ]
    
    user_skill = UserSkill(
        user_id=str(ObjectId()),  # Generate a random user ID
        resume_id=str(ObjectId()),  # Generate a random resume ID
        skills=skills
    )
    
    return user_skill

async def test_job_recommendation():
    """Test the job recommendation feature"""
    logger.info("Testing job recommendation...")
    
    # Create a test user skill profile
    user_skill = await create_test_user_skill()
    
    logger.info(f"Created test user with {len(user_skill.skills)} skills:")
    for skill in user_skill.skills:
        logger.info(f"- {skill.name} ({skill.category}, confidence: {skill.confidence})")
    
    # Ensure we have jobs in the database
    db_setup = await setup_job_database()
    if not db_setup:
        logger.error("Failed to set up job database, cannot test recommendations")
        return
    
    # Get job recommendations
    recommendations = await get_recommended_jobs(user_skill)
    
    # Log the recommendations
    logger.info(f"Found {len(recommendations)} job recommendations")
    
    if recommendations:
        for i, rec in enumerate(recommendations[:5]):  # Show top 5
            logger.info(f"\nRecommendation #{i+1}:")
            logger.info(f"Job: {rec.job.title} at {rec.job.company}")
            logger.info(f"Match Score: {rec.match_score:.2f}")
            logger.info(f"Matching Skills: {', '.join(rec.matching_skills)}")
            logger.info(f"Missing Skills: {', '.join(rec.missing_skills)}")
    else:
        logger.warning("No job recommendations found")

async def setup_job_database():
    """Make sure we have jobs in the database for testing"""
    try:
        # Import here to prevent circular imports
        from app.db.mongodb import get_database
        
        # Check if we have jobs in the database
        db = get_database()
        count = await db["jobs"].count_documents({})
        
        if count > 0:
            logger.info(f"Found {count} existing jobs in database")
            return True
        
        # If no jobs, run the scraper to get some
        logger.info("No jobs found in database, running job scraper...")
        result = await run_job_scraper(
            queries=["python developer", "web developer", "data scientist"], 
            max_pages=1
        )
        
        logger.info(f"Job scraper results: {result}")
        return result.get("total_saved", 0) > 0
        
    except Exception as e:
        logger.error(f"Error setting up job database: {str(e)}")
        return False

async def run_tests():
    """Run all job recommender tests"""
    logger.info("Starting job recommender tests...")
    
    # Connect to MongoDB
    await connect_to_mongo()
    
    try:
        # Test job recommendations
        await test_job_recommendation()
        
        logger.info("All tests completed!")
    
    except Exception as e:
        logger.error(f"Error during tests: {str(e)}")
    
    finally:
        # Close MongoDB connection
        await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(run_tests()) 
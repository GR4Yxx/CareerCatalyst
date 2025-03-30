import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Add the parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent_dir)

# Print the path
logger.info("Python path: %s", sys.path)

try:
    # Try importing the modules
    logger.info("Importing modules...")
    from app.models.skill import Skill, UserSkill, SkillCategory
    logger.info("Imported skill models successfully")
    
    from app.db.mongodb import get_database
    logger.info("Imported mongodb module successfully")
    
    # Import our job modules
    from app.models.job import Job, JobInDB, JobRecommendation
    logger.info("Imported job models successfully")
    
    from app.services.job_service import fetch_jobs, save_jobs, extract_skills_from_job
    logger.info("Imported job service successfully")
    
    logger.info("All imports successful!")
    
except Exception as e:
    logger.error("Import error: %s", str(e), exc_info=True)
    
if __name__ == "__main__":
    print("Test import script executed") 
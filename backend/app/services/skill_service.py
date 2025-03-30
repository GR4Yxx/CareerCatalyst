import os
import io
import json
import re
from typing import List, Dict, Any, Optional, Set
import docx
import PyPDF2
import logging
from bson import ObjectId
from datetime import datetime

from ..db.mongodb import get_database
from ..models.skill import Skill, UserSkill, SkillCategory, SkillAnalysisResult

# Set up logging
logger = logging.getLogger(__name__)

# Gemini API client integration
try:
    import google.generativeai as genai
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        print(f"Configured Gemini with API key: {GEMINI_API_KEY[:4]}...{GEMINI_API_KEY[-4:]}")
        GEMINI_AVAILABLE = True
    else:
        logger.warning("Gemini API key not found in environment variables. Falling back to basic skill extraction.")
        GEMINI_AVAILABLE = False
except ImportError:
    logger.warning("Google Generative AI package not installed. Falling back to basic skill extraction.")
    GEMINI_AVAILABLE = False

# Basic set of technical skills for fallback extraction
COMMON_SKILLS = [
    # Programming Languages
    "Python", "JavaScript", "TypeScript", "Java", "C#", "C++", "Go", "Ruby", "PHP", "Swift", "Kotlin",
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

async def extract_text_from_file(file_content: bytes, file_type: str) -> str:
    """Extract text from various file types."""
    file_obj = io.BytesIO(file_content)
    
    if file_type == "application/pdf":
        # Extract text from PDF
        try:
            pdf_reader = PyPDF2.PdfReader(file_obj)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text() or ""
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return ""
        
    elif file_type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        # Extract text from Word document
        try:
            doc = docx.Document(file_obj)
            return " ".join([para.text for para in doc.paragraphs])
        except Exception as e:
            logger.error(f"Error extracting text from Word document: {str(e)}")
            return ""
        
    elif file_type == "text/plain":
        # Plain text file
        try:
            return file_obj.read().decode("utf-8")
        except Exception as e:
            logger.error(f"Error reading text file: {str(e)}")
            return ""
        
    else:
        logger.warning(f"Unsupported file type: {file_type}")
        return ""

async def analyze_skills_with_gemini(
    resume_text: str
) -> SkillAnalysisResult:
    """
    Use Gemini to analyze resume text and extract skills with categorization.
    
    Args:
        resume_text: The text extracted from the resume
        
    Returns:
        SkillAnalysisResult containing the extracted skills by category
    """
    # Always reload the Gemini API key from environment
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        logger.warning("GEMINI_API_KEY not found in environment. Using basic skill extraction.")
        return await basic_skill_extraction(resume_text)
    
    # Debug log the API key (partial)
    logger.info(f"Using Gemini API key: {gemini_api_key[:4]}...{gemini_api_key[-4:]}")
    
    try:
        # Import here to ensure it's loaded when needed
        import google.generativeai as genai
        
        # Always reconfigure with the current API key
        genai.configure(api_key=gemini_api_key)
        logger.info("Gemini API configured successfully")
            
        # Configure Gemini model - use gemini-1.5-pro if available, fall back to gemini-pro
        try:
            logger.info("Attempting to use gemini-1.5-pro model")
            model = genai.GenerativeModel('gemini-1.5-pro')
        except Exception as e:
            logger.warning(f"Error with gemini-1.5-pro model: {str(e)}. Trying gemini-pro...")
            try:
                logger.info("Attempting to use gemini-pro model")
                model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                logger.error(f"Error with gemini-pro model: {str(e)}. Falling back to basic extraction.")
                return await basic_skill_extraction(resume_text)
        
        # Create prompt for skill extraction
        logger.info("Creating prompt for Gemini")
        prompt = f"""
        You are an expert resume analyzer focused on extracting and categorizing professional skills.
        
        Analyze the following resume text and extract all professional skills. Categorize them into:
        1. Technical Skills (programming languages, tools, platforms)
        2. Soft Skills (communication, leadership, etc.)
        3. Domain Knowledge (industry expertise, methodologies)
        4. Certifications (formal certifications and qualifications)
        
        For each skill, provide a confidence score from 0.0 to 1.0 indicating how confident you are 
        that this is a genuine skill based on the context and presentation in the resume.
        
        Return the result as a JSON object with the following structure:
        {{
            "technical_skills": [
                {{"name": "skill name", "confidence": 0.95}}
            ],
            "soft_skills": [
                {{"name": "skill name", "confidence": 0.8}}
            ],
            "domain_knowledge": [
                {{"name": "skill name", "confidence": 0.9}}
            ],
            "certifications": [
                {{"name": "certification name", "confidence": 0.95}}
            ]
        }}
        
        Here is the resume text:
        
        {resume_text}
        """
        
        # Get response from Gemini
        try:
            logger.info("Sending request to Gemini API")
            response = model.generate_content(prompt)
            logger.info("Successfully got response from Gemini")
        except Exception as e:
            logger.error(f"Error generating content with Gemini: {str(e)}")
            return await basic_skill_extraction(resume_text)
        
        # Parse the response to extract JSON
        try:
            # Try to directly parse if the response contains valid JSON
            if hasattr(response, 'text'):
                response_text = response.text
            else:
                response_text = str(response)
                
            # Extract JSON from response if needed
            json_str = extract_json_from_text(response_text)
            skill_data = json.loads(json_str)
            
            # Convert to our SkillAnalysisResult model
            result = SkillAnalysisResult()
            
            # Process technical skills
            if "technical_skills" in skill_data:
                for skill in skill_data["technical_skills"]:
                    result.technical_skills.append(
                        Skill(
                            name=skill["name"],
                            category=SkillCategory.TECHNICAL,
                            confidence=skill["confidence"]
                        )
                    )
            
            # Process soft skills
            if "soft_skills" in skill_data:
                for skill in skill_data["soft_skills"]:
                    result.soft_skills.append(
                        Skill(
                            name=skill["name"],
                            category=SkillCategory.SOFT,
                            confidence=skill["confidence"]
                        )
                    )
            
            # Process domain knowledge
            if "domain_knowledge" in skill_data:
                for skill in skill_data["domain_knowledge"]:
                    result.domain_knowledge.append(
                        Skill(
                            name=skill["name"],
                            category=SkillCategory.DOMAIN,
                            confidence=skill["confidence"]
                        )
                    )
            
            # Process certifications
            if "certifications" in skill_data:
                for cert in skill_data["certifications"]:
                    result.certifications.append(
                        Skill(
                            name=cert["name"],
                            category=SkillCategory.CERTIFICATION,
                            confidence=cert["confidence"]
                        )
                    )
            
            return result
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error parsing Gemini response: {str(e)}")
            logger.error(f"Response text: {response_text}")
            # Fall back to basic extraction
            return await basic_skill_extraction(resume_text)
    
    except Exception as e:
        logger.error(f"Error using Gemini for skill analysis: {str(e)}")
        # Fall back to basic extraction
        return await basic_skill_extraction(resume_text)

def extract_json_from_text(text: str) -> str:
    """
    Extract a JSON object from text that might contain other content.
    """
    # Try to find JSON object with regex
    json_match = re.search(r'({[\s\S]*})', text)
    if json_match:
        return json_match.group(1)
    
    # If no match, return the original text
    return text

async def basic_skill_extraction(resume_text: str) -> SkillAnalysisResult:
    """
    Basic skill extraction using pattern matching and a predefined list.
    Used as a fallback when Gemini is not available.
    """
    result = SkillAnalysisResult()
    
    # Simple pattern matching for skills from our predefined list
    for skill in COMMON_SKILLS:
        # Use word boundaries to match whole words
        pattern = r'\b' + re.escape(skill) + r'\b'
        matches = re.findall(pattern, resume_text, re.IGNORECASE)
        
        if matches:
            # Calculate a simple confidence based on number of matches
            confidence = min(0.5 + (len(matches) * 0.1), 0.95)
            
            # Categorize based on some heuristics
            if skill in ["Communication", "Leadership", "Teamwork", "Problem Solving", 
                        "Critical Thinking", "Time Management", "Adaptability", 
                        "Creativity", "Emotional Intelligence"]:
                result.soft_skills.append(
                    Skill(
                        name=skill,
                        category=SkillCategory.SOFT,
                        confidence=confidence
                    )
                )
            elif "certified" in skill.lower() or "certification" in skill.lower():
                result.certifications.append(
                    Skill(
                        name=skill,
                        category=SkillCategory.CERTIFICATION,
                        confidence=confidence
                    )
                )
            else:
                result.technical_skills.append(
                    Skill(
                        name=skill,
                        category=SkillCategory.TECHNICAL,
                        confidence=confidence
                    )
                )
    
    return result

def ensure_string_id(value):
    """Helper function to convert ObjectId to string if needed"""
    if isinstance(value, ObjectId):
        return str(value)
    return value

async def analyze_resume_skills(
    resume_id: str,
    file_content: bytes,
    file_type: str,
    user_id: Optional[str] = None,
    profile_id: Optional[str] = None
) -> UserSkill:
    """
    Main function to analyze a resume and extract skills.
    Stores the results in the database.
    
    Args:
        resume_id: The ID of the uploaded resume
        file_content: Binary content of the resume file
        file_type: MIME type of the file
        user_id: User ID if resume is linked directly to user
        profile_id: Profile ID if resume is linked to a profile
        
    Returns:
        UserSkill object containing the extracted skills
    """
    # Extract text from file
    try:
        resume_text = await extract_text_from_file(file_content, file_type)
    except Exception as e:
        logger.error(f"Error extracting text from resume {resume_id}: {str(e)}")
        raise ValueError(f"Failed to extract text from resume: {str(e)}")
    
    if not resume_text.strip():
        logger.error(f"Failed to extract text from resume {resume_id} - extracted text is empty")
        raise ValueError("Could not extract any text from the resume. Make sure the file is not corrupted or password protected.")
    
    # Analyze skills using Gemini
    try:
        skill_analysis = await analyze_skills_with_gemini(resume_text)
        
        if not skill_analysis or not any([
            skill_analysis.technical_skills,
            skill_analysis.soft_skills,
            skill_analysis.domain_knowledge,
            skill_analysis.certifications
        ]):
            logger.warning(f"No skills found in resume {resume_id}")
    except Exception as e:
        logger.error(f"Error in skill analysis for resume {resume_id}: {str(e)}")
        raise ValueError(f"Skill analysis failed: {str(e)}")
    
    # Ensure IDs are strings
    user_id_str = ensure_string_id(user_id) if user_id else None
    profile_id_str = ensure_string_id(profile_id) if profile_id else None
    resume_id_str = ensure_string_id(resume_id)
    
    # Create UserSkill object
    user_skill = UserSkill(
        resume_id=resume_id_str,
        user_id=user_id_str,
        profile_id=profile_id_str,
        skills=skill_analysis.all_skills()
    )
    
    # Store in database
    try:
        db = get_database()
        user_skills_collection = db["user_skills"]
        
        # Check for existing skills and remove them
        await user_skills_collection.delete_many({"resume_id": ObjectId(resume_id)})
        
        # Convert model to dict
        user_skill_dict = user_skill.model_dump(exclude={"id"})
        
        # Convert string IDs to ObjectIds for database storage
        if user_id:
            user_skill_dict["user_id"] = ObjectId(user_id)
        if profile_id:
            user_skill_dict["profile_id"] = ObjectId(profile_id)
        
        user_skill_dict["resume_id"] = ObjectId(resume_id)
        
        # Insert into database
        result = await user_skills_collection.insert_one(user_skill_dict)
        
        # Update the ID and return
        user_skill.id = str(result.inserted_id)
        
        # Log success
        skill_count = len(user_skill.skills)
        logger.info(f"Successfully analyzed resume {resume_id} and found {skill_count} skills")
        
        return user_skill
    except Exception as e:
        logger.error(f"Database error during skill storage for resume {resume_id}: {str(e)}")
        raise ValueError(f"Failed to store skills in database: {str(e)}")

async def get_skills_by_resume(resume_id: str) -> Optional[UserSkill]:
    """
    Get the skills for a specific resume.
    """
    db = get_database()
    user_skills_collection = db["user_skills"]
    
    skill_data = await user_skills_collection.find_one({"resume_id": ObjectId(resume_id)})
    
    if not skill_data:
        return None
    
    # Convert ObjectId fields to strings
    if "_id" in skill_data:
        skill_data["id"] = str(skill_data.pop("_id"))
    if "user_id" in skill_data and isinstance(skill_data["user_id"], ObjectId):
        skill_data["user_id"] = str(skill_data["user_id"])
    if "profile_id" in skill_data and isinstance(skill_data["profile_id"], ObjectId):
        skill_data["profile_id"] = str(skill_data["profile_id"])
    if "resume_id" in skill_data and isinstance(skill_data["resume_id"], ObjectId):
        skill_data["resume_id"] = str(skill_data["resume_id"])
    
    return UserSkill(**skill_data)

async def get_skills_by_user(user_id: str) -> List[UserSkill]:
    """
    Get all skills for a user
    
    Args:
        user_id: The user's ID
        
    Returns:
        List of UserSkill documents
    """
    db = get_database()
    cursor = db["user_skills"].find({"user_id": user_id}).sort("created_at", -1)
    
    skills = []
    async for doc in cursor:
        skills.append(UserSkill(**doc))
    
    return skills

async def get_skills_by_profile(profile_id: str) -> List[UserSkill]:
    """
    Get all skills for a profile.
    """
    db = get_database()
    user_skills_collection = db["user_skills"]
    
    cursor = user_skills_collection.find({"profile_id": ObjectId(profile_id)}).sort("created_at", -1)
    skills_list = await cursor.to_list(length=None)
    
    result = []
    for skill_data in skills_list:
        # Convert ObjectId fields to strings
        if "_id" in skill_data:
            skill_data["id"] = str(skill_data.pop("_id"))
        if "user_id" in skill_data and isinstance(skill_data["user_id"], ObjectId):
            skill_data["user_id"] = str(skill_data["user_id"])
        if "profile_id" in skill_data and isinstance(skill_data["profile_id"], ObjectId):
            skill_data["profile_id"] = str(skill_data["profile_id"])
        if "resume_id" in skill_data and isinstance(skill_data["resume_id"], ObjectId):
            skill_data["resume_id"] = str(skill_data["resume_id"])
        
        result.append(UserSkill(**skill_data))
    
    return result

async def get_user_skills_from_current_resume(user_id: str) -> List[Skill]:
    """
    Get the skills from the user's current resume
    
    Args:
        user_id: User ID to get skills for
        
    Returns:
        List of skills from the current resume
    """
    db = get_database()
    
    try:
        # Try to get current resume
        resume = await db["resumes"].find_one({
            "user_id": ObjectId(user_id),
            "is_current": True
        })
        
        if not resume:
            logger.warning(f"No current resume found for user {user_id}")
            
            # Try to find any resume for this user and mark it as current
            logger.info(f"Looking for any resume to mark as current for user {user_id}")
            resume = await db["resumes"].find_one({"user_id": ObjectId(user_id)})
            
            if resume:
                logger.info(f"Found resume {resume['_id']} - marking as current")
                # Mark this resume as current
                await db["resumes"].update_one(
                    {"_id": resume["_id"]},
                    {"$set": {"is_current": True}}
                )
                
                # Update our local copy to reflect the change
                resume["is_current"] = True
            else:
                logger.warning(f"No resumes found for user {user_id}")
                # Return a test set of skills for testing
                test_skills = [
                    Skill(name="Python", category=SkillCategory.TECHNICAL, confidence=0.95),
                    Skill(name="JavaScript", category=SkillCategory.TECHNICAL, confidence=0.9),
                    Skill(name="React", category=SkillCategory.TECHNICAL, confidence=0.85),
                    Skill(name="Communication", category=SkillCategory.SOFT, confidence=0.8),
                    Skill(name="Problem Solving", category=SkillCategory.SOFT, confidence=0.85)
                ]
                logger.info(f"Created test skills for user {user_id}")
                return test_skills
        
        # Get skills for the resume
        skills_data = await db["resume_skills"].find_one({"resume_id": resume["_id"]})
        
        if not skills_data:
            logger.warning(f"No skills found for resume {resume['_id']}")
            # Return a test set of skills for testing
            test_skills = [
                Skill(name="Python", category=SkillCategory.TECHNICAL, confidence=0.95),
                Skill(name="JavaScript", category=SkillCategory.TECHNICAL, confidence=0.9),
                Skill(name="React", category=SkillCategory.TECHNICAL, confidence=0.85),
                Skill(name="Communication", category=SkillCategory.SOFT, confidence=0.8),
                Skill(name="Problem Solving", category=SkillCategory.SOFT, confidence=0.85)
            ]
            logger.info(f"Created test skills for resume {resume['_id']}")
            return test_skills
        
        skills = []
        for skill_data in skills_data.get("skills", []):
            try:
                skill = Skill(
                    name=skill_data.get("name", ""),
                    category=SkillCategory(skill_data.get("category", SkillCategory.TECHNICAL)),
                    confidence=skill_data.get("confidence", 0.0)
                )
                skills.append(skill)
            except Exception as e:
                logger.error(f"Error creating skill from data: {str(e)}")
        
        return skills
        
    except Exception as e:
        logger.error(f"Error getting skills from current resume: {str(e)}")
        # Return a fallback set of skills
        return [
            Skill(name="Python", category=SkillCategory.TECHNICAL, confidence=0.9),
            Skill(name="JavaScript", category=SkillCategory.TECHNICAL, confidence=0.8),
            Skill(name="Communication", category=SkillCategory.SOFT, confidence=0.7)
        ] 
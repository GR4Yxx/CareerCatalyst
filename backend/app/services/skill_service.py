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
    if not GEMINI_AVAILABLE:
        logger.warning("Gemini API not available. Using basic skill extraction.")
        return await basic_skill_extraction(resume_text)
    
    try:
        # Ensure API key is set
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            logger.warning("GEMINI_API_KEY not found in environment. Using basic skill extraction.")
            return await basic_skill_extraction(resume_text)
            
        # Reconfigure with the API key to ensure it's using the latest
        genai.configure(api_key=gemini_api_key)
            
        # Configure Gemini model - use gemini-1.5-pro if available, fall back to gemini-pro
        try:
            model = genai.GenerativeModel('gemini-1.5-pro')
        except Exception as e:
            logger.warning(f"Error with gemini-1.5-pro model: {str(e)}. Trying gemini-pro...")
            try:
                model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                logger.error(f"Error with gemini-pro model: {str(e)}. Falling back to basic extraction.")
                return await basic_skill_extraction(resume_text)
        
        # Create prompt for skill extraction
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
    resume_text = await extract_text_from_file(file_content, file_type)
    
    if not resume_text.strip():
        logger.error(f"Failed to extract text from resume {resume_id}")
        return UserSkill(
            resume_id=resume_id,
            user_id=user_id,
            profile_id=profile_id,
            skills=[]
        )
    
    # Analyze skills using Gemini
    skill_analysis = await analyze_skills_with_gemini(resume_text)
    
    # Create UserSkill object
    user_skill = UserSkill(
        resume_id=resume_id,
        user_id=user_id,
        profile_id=profile_id,
        skills=skill_analysis.all_skills()
    )
    
    # Store in database
    db = get_database()
    user_skills_collection = db["user_skills"]
    
    # Convert model to dict
    user_skill_dict = user_skill.model_dump(exclude={"id"})
    
    # Convert string IDs to ObjectIds
    if user_id:
        user_skill_dict["user_id"] = ObjectId(user_id)
    if profile_id:
        user_skill_dict["profile_id"] = ObjectId(profile_id)
    
    user_skill_dict["resume_id"] = ObjectId(resume_id)
    
    # Insert into database
    result = await user_skills_collection.insert_one(user_skill_dict)
    
    # Update the ID and return
    user_skill.id = str(result.inserted_id)
    return user_skill

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
    Get all skills for a user.
    """
    db = get_database()
    user_skills_collection = db["user_skills"]
    
    cursor = user_skills_collection.find({"user_id": ObjectId(user_id)}).sort("created_at", -1)
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
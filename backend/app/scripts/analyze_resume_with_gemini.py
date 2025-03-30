#!/usr/bin/env python3
import asyncio
import os
import sys
from pathlib import Path

# Load environment variables from .env file first
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    print(f"Loading environment from {env_path}")
    load_dotenv(dotenv_path=env_path)

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(str(Path(__file__).parent.parent.parent))

import aiohttp
import json
from pprint import pprint

# Import directly from the app for direct testing
from app.services import skill_service
from app.db.mongodb import connect_to_mongo, close_mongo_connection

async def analyze_resume_file():
    """
    A simple script to directly analyze a resume file with Gemini.
    This bypasses the API and directly uses the skill_service for testing.
    """
    # Configuration
    RESUME_PATH = Path(__file__).parent.parent.parent / "data" / "Resume-Joshua Dsouza.docx"
    
    if not RESUME_PATH.exists():
        print(f"Error: Resume file not found at {RESUME_PATH}")
        return False
    
    print(f"Using resume file: {RESUME_PATH}")
    
    try:
        # Read the file
        print("📄 Reading resume file...")
        with open(RESUME_PATH, "rb") as f:
            file_content = f.read()
        
        # Determine file type based on extension
        file_name = RESUME_PATH.name
        file_extension = RESUME_PATH.suffix.lower()
        
        if file_extension == ".pdf":
            file_type = "application/pdf"
        elif file_extension == ".docx":
            file_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif file_extension == ".doc":
            file_type = "application/msword"
        elif file_extension == ".txt":
            file_type = "text/plain"
        else:
            print(f"❌ Unsupported file type: {file_extension}")
            return False
        
        print(f"✅ File loaded: {file_name} ({file_type})")
        
        # Extract text from the resume
        print("\n📃 Extracting text from resume...")
        resume_text = await skill_service.extract_text_from_file(file_content, file_type)
        
        if not resume_text:
            print("❌ Failed to extract text from resume")
            return False
        
        # Print a preview of the extracted text
        text_preview = resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
        print(f"✅ Extracted text ({len(resume_text)} characters):")
        print(f"\n{text_preview}\n")
        
        # Check if Gemini API key is configured
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            print("⚠️ Warning: GEMINI_API_KEY not found in environment variables.")
            print("   Will fall back to basic pattern matching.")
        else:
            print(f"✅ Gemini API key found: {gemini_api_key[:4]}...{gemini_api_key[-4:]}")
            # Force reload the Gemini configuration
            import google.generativeai as genai
            genai.configure(api_key=gemini_api_key)
            print("   Gemini API configured successfully.")
        
        # Send to Gemini for analysis
        print("\n🧪 Sending to Gemini for skill analysis...")
        print("   This may take a few moments...")
        
        skill_analysis = await skill_service.analyze_skills_with_gemini(resume_text)
        
        print("✅ Gemini analysis complete!")
        
        # Display the results
        print("\n📊 Skill Analysis Results:")
        
        # Technical Skills
        print(f"\n🔧 Technical Skills ({len(skill_analysis.technical_skills)}): ")
        for skill in skill_analysis.technical_skills:
            print(f"   - {skill.name} (confidence: {skill.confidence:.2f})")
            
        # Soft Skills
        print(f"\n🤝 Soft Skills ({len(skill_analysis.soft_skills)}): ")
        for skill in skill_analysis.soft_skills:
            print(f"   - {skill.name} (confidence: {skill.confidence:.2f})")
            
        # Domain Knowledge
        print(f"\n🌐 Domain Knowledge ({len(skill_analysis.domain_knowledge)}): ")
        for skill in skill_analysis.domain_knowledge:
            print(f"   - {skill.name} (confidence: {skill.confidence:.2f})")
            
        # Certifications
        print(f"\n🏆 Certifications ({len(skill_analysis.certifications)}): ")
        for skill in skill_analysis.certifications:
            print(f"   - {skill.name} (confidence: {skill.confidence:.2f})")
        
        # Count total skills
        total_skills = (len(skill_analysis.technical_skills) + 
                        len(skill_analysis.soft_skills) + 
                        len(skill_analysis.domain_knowledge) + 
                        len(skill_analysis.certifications))
        
        print(f"\n🎯 Total Skills Identified: {total_skills}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during resume analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Resume Skill Analysis with Gemini\n")
    
    result = asyncio.run(analyze_resume_file())
    
    if result:
        print("\n🎉 Resume analysis with Gemini completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Resume analysis with Gemini failed")
        sys.exit(1) 
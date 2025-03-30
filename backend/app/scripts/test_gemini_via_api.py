#!/usr/bin/env python3
import asyncio
import os
import sys
import json
from pathlib import Path

# Load environment variables from .env file first
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    print(f"Loading environment from {env_path}")
    load_dotenv(dotenv_path=env_path)

import aiohttp
from pprint import pprint

# API configuration
API_BASE_URL = "http://localhost/api"  # Through Nginx
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "password123"
RESUME_PATH = Path(__file__).parent.parent.parent / "data" / "Resume-Joshua Dsouza.docx"

async def test_gemini_via_api():
    """
    Test the Gemini skills analysis through the API routes (through Nginx).
    This simulates how the frontend would interact with the backend.
    """
    if not RESUME_PATH.exists():
        print(f"Error: Resume file not found at {RESUME_PATH}")
        return False
    
    print(f"Using resume file: {RESUME_PATH}")
    
    try:
        async with aiohttp.ClientSession() as session:
            # Step 1: Authenticate
            print("\n🔑 Authenticating...")
            auth_data = {
                "username": TEST_EMAIL,
                "password": TEST_PASSWORD
            }
            
            async with session.post(f"{API_BASE_URL}/auth/login", data=auth_data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    print(f"❌ Authentication failed with status {response.status}: {error_text}")
                    return False
                
                auth_response = await response.json()
                access_token = auth_response.get("access_token")
                
                if not access_token:
                    print("❌ Failed to get access token")
                    return False
                
                print("✅ Authentication successful")
                
                # Set auth header for subsequent requests
                headers = {"Authorization": f"Bearer {access_token}"}
            
            # Step 2: Upload a test resume
            print("\n📄 Uploading resume...")
            
            with open(RESUME_PATH, "rb") as f:
                form_data = aiohttp.FormData()
                form_data.add_field("file", 
                                    f,
                                    filename=RESUME_PATH.name,
                                    content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                
                async with session.post(f"{API_BASE_URL}/resumes/upload", data=form_data, headers=headers) as response:
                    if response.status not in (200, 201):
                        error_text = await response.text()
                        print(f"❌ Resume upload failed with status {response.status}: {error_text}")
                        return False
                    
                    resume_data = await response.json()
                    resume_id = resume_data.get("_id") or resume_data.get("id")
                    
                    if not resume_id:
                        print("❌ Failed to get resume ID")
                        return False
                    
                    print(f"✅ Resume uploaded successfully with ID: {resume_id}")
            
            # Step 3: Analyze the resume skills using Gemini
            print("\n🧠 Analyzing resume with Gemini through API...")
            
            async with session.post(f"{API_BASE_URL}/skills/analyze/{resume_id}", headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    print(f"❌ Skills analysis failed with status {response.status}: {error_text}")
                    return False
                
                skills_data = await response.json()
                print("✅ Skills analysis completed successfully")
                
                # Display the results
                skills = skills_data.get("skills", [])
                
                if not skills:
                    print("❌ No skills returned from analysis")
                    return False
                
                # Count skills by category
                tech_skills = [s for s in skills if s.get("category") == "technical"]
                soft_skills = [s for s in skills if s.get("category") == "soft"]
                domain_skills = [s for s in skills if s.get("category") == "domain"]
                certifications = [s for s in skills if s.get("category") == "certification"]
                
                # Display the results
                print("\n📊 Skill Analysis Results:")
                
                # Technical Skills
                print(f"\n🔧 Technical Skills ({len(tech_skills)}): ")
                for skill in tech_skills:
                    print(f"   - {skill.get('name')} (confidence: {skill.get('confidence'):.2f})")
                    
                # Soft Skills
                print(f"\n🤝 Soft Skills ({len(soft_skills)}): ")
                for skill in soft_skills:
                    print(f"   - {skill.get('name')} (confidence: {skill.get('confidence'):.2f})")
                    
                # Domain Knowledge
                print(f"\n🌐 Domain Knowledge ({len(domain_skills)}): ")
                for skill in domain_skills:
                    print(f"   - {skill.get('name')} (confidence: {skill.get('confidence'):.2f})")
                    
                # Certifications
                print(f"\n🏆 Certifications ({len(certifications)}): ")
                for skill in certifications:
                    print(f"   - {skill.get('name')} (confidence: {skill.get('confidence'):.2f})")
                
                # Count total skills
                total_skills = len(tech_skills) + len(soft_skills) + len(domain_skills) + len(certifications)
                
                print(f"\n🎯 Total Skills Identified: {total_skills}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error during API test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing Gemini Skills Analysis through API\n")
    
    result = asyncio.run(test_gemini_via_api())
    
    if result:
        print("\n🎉 API test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ API test failed")
        sys.exit(1) 
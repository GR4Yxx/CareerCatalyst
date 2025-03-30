#!/usr/bin/env python3
import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(str(Path(__file__).parent.parent.parent))

import aiohttp
import json
from pprint import pprint

# Import directly from the app for direct testing
from app.services import skill_service, resume_service
from app.db.mongodb import connect_to_mongo, close_mongo_connection

async def test_gemini_skill_analysis():
    """
    Test script that:
    1. Authenticates with the API
    2. Gets the current resume for the user
    3. Downloads the resume content
    4. Sends the resume to Gemini for skill analysis
    5. Displays the extracted skills
    """
    # Configuration
    API_URL = "http://localhost"  # Nginx URL (port 80)
    
    # User credentials
    USER_EMAIL = "xpjosh10@gmail.com"
    USER_PASSWORD = "lol123456"
    
    print("🚀 Starting Gemini Skill Analysis Test\n")
    
    # Part 1: Test API Flow (through endpoints)
    print("📡 Testing through API endpoints...\n")
    
    async with aiohttp.ClientSession() as session:
        # Step 1: Authenticate
        print("🔑 Authenticating...")
        auth_data = {
            "username": USER_EMAIL,
            "password": USER_PASSWORD
        }
        
        async with session.post(f"{API_URL}/api/auth/login", data=auth_data) as response:
            if response.status != 200:
                error_text = await response.text()
                print(f"❌ Authentication failed with status {response.status}: {error_text}")
                
                # Try directly with the backend server
                print("\n⚠️ Retrying with direct backend connection...")
                direct_api_url = "http://localhost:8000"
                async with session.post(f"{direct_api_url}/auth/login", data=auth_data) as direct_response:
                    if direct_response.status != 200:
                        direct_error = await direct_response.text()
                        print(f"❌ Direct authentication also failed with status {direct_response.status}: {direct_error}")
                        return False
                    
                    print("✅ Direct authentication successful!")
                    auth_response = await direct_response.json()
                    access_token = auth_response.get("access_token")
                    API_URL = direct_api_url  # Use direct connection for subsequent requests
            else:
                auth_response = await response.json()
                access_token = auth_response.get("access_token")
            
            if not access_token:
                print("❌ Failed to get access token")
                return False
            
            print("✅ Authentication successful")
            
            # Set auth header for subsequent requests
            headers = {"Authorization": f"Bearer {access_token}"}
        
        # Step 2: Get current resume
        print("\n📄 Getting current resume...")
        
        # Determine the correct endpoint based on which API_URL we're using
        current_resume_endpoint = "/resumes/user/current" if API_URL == "http://localhost:8000" else "/api/resumes/user/current"
        
        async with session.get(f"{API_URL}{current_resume_endpoint}", headers=headers) as response:
            if response.status != 200:
                error_text = await response.text()
                print(f"❌ Failed to get current resume with status {response.status}: {error_text}")
                return False
            
            resume_data = await response.json()
            resume_id = resume_data.get("_id")
            
            if not resume_id:
                print("❌ Failed to get resume ID")
                return False
            
            print(f"✅ Got current resume: {resume_data.get('original_filename')}")
            print(f"   Resume ID: {resume_id}")
        
        # Step 3: Trigger skill analysis
        print("\n🧠 Triggering Gemini skill analysis...")
        
        # Determine the correct endpoint based on which API_URL we're using
        analyze_endpoint = f"/skills/analyze/{resume_id}" if API_URL == "http://localhost:8000" else f"/api/skills/analyze/{resume_id}"
        
        async with session.post(f"{API_URL}{analyze_endpoint}", headers=headers) as response:
            if response.status != 200:
                error_text = await response.text()
                print(f"❌ Skill analysis failed with status {response.status}: {error_text}")
                return False
            
            skills_data = await response.json()
            skills = skills_data.get("skills", [])
            
            print(f"✅ Skill analysis completed successfully!")
            print(f"   Total skills found: {len(skills)}")
            
            # Display skills by category
            technical_skills = [s for s in skills if s.get("category") == "technical"]
            soft_skills = [s for s in skills if s.get("category") == "soft"]
            domain_skills = [s for s in skills if s.get("category") == "domain"]
            certifications = [s for s in skills if s.get("category") == "certification"]
            
            print(f"\n🔧 Technical Skills ({len(technical_skills)}): ")
            for skill in technical_skills[:5]:  # Show first 5 skills
                print(f"   - {skill.get('name')} (confidence: {skill.get('confidence'):.2f})")
            if len(technical_skills) > 5:
                print(f"   - ... and {len(technical_skills) - 5} more")
                
            print(f"\n🤝 Soft Skills ({len(soft_skills)}): ")
            for skill in soft_skills[:5]:
                print(f"   - {skill.get('name')} (confidence: {skill.get('confidence'):.2f})")
            if len(soft_skills) > 5:
                print(f"   - ... and {len(soft_skills) - 5} more")
                
            print(f"\n🌐 Domain Knowledge ({len(domain_skills)}): ")
            for skill in domain_skills[:5]:
                print(f"   - {skill.get('name')} (confidence: {skill.get('confidence'):.2f})")
            if len(domain_skills) > 5:
                print(f"   - ... and {len(domain_skills) - 5} more")
                
            print(f"\n🏆 Certifications ({len(certifications)}): ")
            for skill in certifications[:5]:
                print(f"   - {skill.get('name')} (confidence: {skill.get('confidence'):.2f})")
            if len(certifications) > 5:
                print(f"   - ... and {len(certifications) - 5} more")
    
    # Part 2: Test Direct Service Integration
    print("\n\n🔬 Testing direct service integration...\n")
    
    try:
        # Connect to MongoDB
        await connect_to_mongo()
        
        # Get the current resume for the user directly
        user_id = "your-user-id"  # Replace with actual user ID if available, or use below method
        print("📑 Getting resume directly from service...")
        
        # If user_id is not known, we can get a random resume for testing
        resumes = await resume_service.get_resumes_by_user(user_id)
        
        if not resumes:
            print("⚠️ No resumes found for this user. Trying to get any available resume...")
            # Use the DB directly to find a resume
            from app.db.mongodb import get_database
            db = get_database()
            resumes_collection = db["resumes"]
            resume_doc = await resumes_collection.find_one({})
            
            if not resume_doc:
                print("❌ No resumes found in the database")
                return False
            
            resume_id = str(resume_doc["_id"])
            print(f"✅ Using resume with ID: {resume_id}")
        else:
            resume_id = resumes[0].id
            print(f"✅ Found resume with ID: {resume_id}")
        
        # Download the resume content
        print("\n📥 Downloading resume content...")
        file_data = await resume_service.download_resume(resume_id)
        
        if not file_data:
            print("❌ Failed to download resume content")
            return False
        
        print(f"✅ Downloaded resume: {file_data['filename']}")
        print(f"   File type: {file_data['file_type']}")
        
        # Extract text from the resume
        print("\n📃 Extracting text from resume...")
        resume_text = await skill_service.extract_text_from_file(file_data['content'], file_data['file_type'])
        
        if not resume_text:
            print("❌ Failed to extract text from resume")
            return False
        
        text_preview = resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
        print(f"✅ Extracted text ({len(resume_text)} characters):")
        print(f"   {text_preview}")
        
        # Send to Gemini for analysis
        print("\n🧪 Sending to Gemini for skill analysis...")
        skill_analysis = await skill_service.analyze_skills_with_gemini(resume_text)
        
        print("✅ Gemini analysis complete!")
        
        # Display the results
        print("\n📊 Skill Analysis Results:")
        
        print(f"\n🔧 Technical Skills ({len(skill_analysis.technical_skills)}): ")
        for skill in skill_analysis.technical_skills[:10]:
            print(f"   - {skill.name} (confidence: {skill.confidence:.2f})")
        if len(skill_analysis.technical_skills) > 10:
            print(f"   - ... and {len(skill_analysis.technical_skills) - 10} more")
            
        print(f"\n🤝 Soft Skills ({len(skill_analysis.soft_skills)}): ")
        for skill in skill_analysis.soft_skills[:10]:
            print(f"   - {skill.name} (confidence: {skill.confidence:.2f})")
        if len(skill_analysis.soft_skills) > 10:
            print(f"   - ... and {len(skill_analysis.soft_skills) - 10} more")
            
        print(f"\n🌐 Domain Knowledge ({len(skill_analysis.domain_knowledge)}): ")
        for skill in skill_analysis.domain_knowledge[:10]:
            print(f"   - {skill.name} (confidence: {skill.confidence:.2f})")
        if len(skill_analysis.domain_knowledge) > 10:
            print(f"   - ... and {len(skill_analysis.domain_knowledge) - 10} more")
            
        print(f"\n🏆 Certifications ({len(skill_analysis.certifications)}): ")
        for skill in skill_analysis.certifications[:10]:
            print(f"   - {skill.name} (confidence: {skill.confidence:.2f})")
        if len(skill_analysis.certifications) > 10:
            print(f"   - ... and {len(skill_analysis.certifications) - 10} more")
        
    except Exception as e:
        print(f"❌ Error during direct service testing: {str(e)}")
        return False
    finally:
        # Close MongoDB connection
        await close_mongo_connection()
    
    return True

if __name__ == "__main__":
    result = asyncio.run(test_gemini_skill_analysis())
    if result:
        print("\n🎉 Gemini skill analysis test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Gemini skill analysis test failed")
        sys.exit(1) 
#!/usr/bin/env python3
import asyncio
import os
import sys
from pathlib import Path
import json

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(str(Path(__file__).parent.parent.parent))

import aiohttp

async def test_resume_upload():
    """
    Debug version of the test script with more verbose logging
    """
    # Configuration
    API_URL = "http://localhost"  # Nginx URL (port 80)
    DIRECT_API_URL = "http://localhost:8000"  # Direct backend URL
    RESUME_PATH = Path(__file__).parent.parent.parent / "data" / "Resume-Joshua Dsouza.docx"
    
    if not RESUME_PATH.exists():
        print(f"Error: Resume file not found at {RESUME_PATH}")
        return False
    
    print(f"Using resume file: {RESUME_PATH}")
    
    # User credentials with the specified email
    USER_EMAIL = "xpjosh10@gmail.com"
    USER_PASSWORD = "lol123456"
    
    # Try both direct backend and nginx
    urls_to_try = [
        {"name": "NGINX", "url": API_URL, "auth_path": "/api/auth/login", "upload_path": "/api/resumes/upload"},
        {"name": "DIRECT", "url": DIRECT_API_URL, "auth_path": "/auth/login", "upload_path": "/resumes/upload"}
    ]
    
    for endpoint_config in urls_to_try:
        print(f"\n====== Testing with {endpoint_config['name']} endpoint ======")
        
        async with aiohttp.ClientSession() as session:
            # Step 1: Authenticate
            print(f"Authenticating against {endpoint_config['url'] + endpoint_config['auth_path']}...")
            auth_data = {
                "username": USER_EMAIL,
                "password": USER_PASSWORD
            }
            
            try:
                async with session.post(
                    endpoint_config['url'] + endpoint_config['auth_path'], 
                    data=auth_data
                ) as response:
                    status = response.status
                    text = await response.text()
                    print(f"Auth Status Code: {status}")
                    print(f"Auth Response: {text}")
                    
                    if status != 200:
                        print(f"Authentication failed with {endpoint_config['name']} endpoint")
                        continue
                    
                    try:
                        auth_response = json.loads(text)
                        access_token = auth_response.get("access_token")
                        
                        if not access_token:
                            print("Missing access_token in response")
                            continue
                            
                        print(f"Authentication successful with {endpoint_config['name']} endpoint")
                        
                        # Step 2: Upload resume
                        print(f"Uploading resume to {endpoint_config['url'] + endpoint_config['upload_path']}...")
                        
                        # Prepare multipart form data
                        with open(RESUME_PATH, "rb") as f:
                            form_data = aiohttp.FormData()
                            form_data.add_field('file', 
                                               f,
                                               filename=RESUME_PATH.name,
                                               content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                            
                            headers = {"Authorization": f"Bearer {access_token}"}
                            print(f"Headers: {headers}")
                            
                            async with session.post(
                                endpoint_config['url'] + endpoint_config['upload_path'], 
                                data=form_data,
                                headers=headers
                            ) as upload_response:
                                upload_status = upload_response.status
                                upload_text = await upload_response.text()
                                print(f"Upload Status Code: {upload_status}")
                                print(f"Upload Response: {upload_text}")
                                
                                if upload_status != 201:
                                    print(f"Upload failed with {endpoint_config['name']} endpoint")
                                    continue
                                
                                try:
                                    upload_json = json.loads(upload_text)
                                    
                                    if "_id" in upload_json:
                                        print(f"✅ Upload successful with {endpoint_config['name']} endpoint!")
                                        print(f"Resume ID: {upload_json.get('_id')}")
                                        return True
                                    else:
                                        print("Response doesn't contain _id field")
                                except json.JSONDecodeError:
                                    print("Failed to parse upload response as JSON")
                    
                    except json.JSONDecodeError:
                        print("Failed to parse auth response as JSON")
            
            except Exception as e:
                print(f"Error communicating with {endpoint_config['name']} endpoint: {str(e)}")
    
    print("\n❌ All endpoints failed")
    return False

if __name__ == "__main__":
    result = asyncio.run(test_resume_upload())
    if result:
        print("\n🎉 Resume upload test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Resume upload test failed")
        sys.exit(1) 
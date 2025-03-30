#!/usr/bin/env python3
import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(str(Path(__file__).parent.parent.parent))

import aiohttp
import json

async def test_resume_upload():
    """
    Test script that uploads a resume file to the backend API and checks if it works properly.
    This script:
    1. Attempts to authenticate with a test user
    2. Uploads a resume file from the data directory
    3. Verifies the upload response contains the expected data
    4. Optionally downloads the uploaded resume to verify it matches
    """
    # Configuration
    API_URL = "http://localhost"  # Nginx URL (port 80)
    RESUME_PATH = Path(__file__).parent.parent.parent / "data" / "Resume-Joshua Dsouza.docx"
    
    if not RESUME_PATH.exists():
        print(f"Error: Resume file not found at {RESUME_PATH}")
        return False
    
    print(f"Using resume file: {RESUME_PATH}")
    
    # User credentials with the specified email
    USER_EMAIL = "xpjosh10@gmail.com"
    USER_PASSWORD = "lol123456"  # Updated password
    
    async with aiohttp.ClientSession() as session:
        # Step 1: Authenticate
        print("Authenticating...")
        auth_data = {
            "username": USER_EMAIL,
            "password": USER_PASSWORD
        }
        
        async with session.post(f"{API_URL}/api/auth/login", data=auth_data) as response:
            if response.status != 200:
                error_text = await response.text()
                print(f"Authentication failed with status {response.status}: {error_text}")
                
                # Try directly with the backend server
                print("\nRetrying with direct backend connection...")
                direct_api_url = "http://localhost:8000"
                async with session.post(f"{direct_api_url}/auth/login", data=auth_data) as direct_response:
                    if direct_response.status != 200:
                        direct_error = await direct_response.text()
                        print(f"Direct authentication also failed with status {direct_response.status}: {direct_error}")
                        return False
                    
                    print("Direct authentication successful!")
                    auth_response = await direct_response.json()
                    access_token = auth_response.get("access_token")
                    API_URL = direct_api_url  # Use direct connection for subsequent requests
            else:
                auth_response = await response.json()
                access_token = auth_response.get("access_token")
            
            if not access_token:
                print("Failed to get access token")
                return False
            
            print("Authentication successful")
            
            # Set auth header for subsequent requests
            headers = {"Authorization": f"Bearer {access_token}"}
        
        # Step 2: Upload resume
        print("Uploading resume...")
        print(f"Using API URL: {API_URL}")
        
        # Determine the correct endpoint based on which API_URL we're using
        upload_endpoint = "/resumes/upload" if API_URL == "http://localhost:8000" else "/api/resumes/upload"
        
        # Prepare multipart form data
        with open(RESUME_PATH, "rb") as f:
            form_data = aiohttp.FormData()
            form_data.add_field('file', 
                                f,
                                filename=RESUME_PATH.name,
                                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            
            print(f"Sending upload request to: {API_URL}{upload_endpoint}")
            async with session.post(f"{API_URL}{upload_endpoint}", 
                                   data=form_data,
                                   headers=headers) as response:
                
                if response.status != 201:
                    error_text = await response.text()
                    print(f"Upload failed with status {response.status}: {error_text}")
                    return False
                
                upload_response = await response.json()
                print("Upload successful!")
                print(f"Resume ID: {upload_response.get('_id')}")
                print(f"Original filename: {upload_response.get('original_filename')}")
                
                # Step 3: Verify the upload response
                if (upload_response.get('original_filename') == RESUME_PATH.name and
                    upload_response.get('file_type') == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
                    print("✅ Upload response contains expected data")
                else:
                    print("❌ Upload response does not match expected data")
                    print(f"Expected filename: {RESUME_PATH.name}")
                    print(f"Got: {upload_response}")
                    return False
                
                # Step 4: Download the uploaded resume to verify
                resume_id = upload_response.get('_id')
                print(f"\nDownloading resume with ID: {resume_id}")
                
                # Determine the correct download endpoint based on which API_URL we're using
                download_endpoint = f"/resumes/{resume_id}/download" if API_URL == "http://localhost:8000" else f"/api/resumes/{resume_id}/download"
                
                print(f"Sending download request to: {API_URL}{download_endpoint}")
                async with session.get(f"{API_URL}{download_endpoint}", 
                                      headers=headers) as download_response:
                    
                    if download_response.status != 200:
                        error_text = await download_response.text()
                        print(f"Download failed with status {download_response.status}: {error_text}")
                        return False
                    
                    content_disposition = download_response.headers.get('Content-Disposition', '')
                    if RESUME_PATH.name in content_disposition:
                        print("✅ Downloaded resume filename matches the uploaded file")
                    else:
                        print(f"❌ Content-Disposition header does not contain original filename: {content_disposition}")
                    
                    # Could save downloaded content and compare checksums for complete verification
                    print("✅ Resume download successful")
                
                return True

if __name__ == "__main__":
    result = asyncio.run(test_resume_upload())
    if result:
        print("\n🎉 Resume upload test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Resume upload test failed")
        sys.exit(1) 
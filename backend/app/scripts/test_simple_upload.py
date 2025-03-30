#!/usr/bin/env python3
import requests
import os
from pathlib import Path

# Configuration
API_URL = "http://localhost"
RESUME_PATH = Path(__file__).parent.parent.parent / "data" / "Resume-Joshua Dsouza.docx"
USER_EMAIL = "xpjosh10@gmail.com"
USER_PASSWORD = "lol123456"

def test_simple_upload():
    """
    A simplified test to upload a resume file directly to the nginx endpoint
    using the requests library instead of aiohttp.
    """
    print(f"Using resume file: {RESUME_PATH}")
    
    if not RESUME_PATH.exists():
        print(f"Error: Resume file not found at {RESUME_PATH}")
        return False
    
    # Step 1: Authenticate
    print("Authenticating...")
    auth_data = {
        "username": USER_EMAIL,
        "password": USER_PASSWORD
    }
    
    auth_response = requests.post(f"{API_URL}/api/auth/login", data=auth_data)
    if auth_response.status_code != 200:
        print(f"Authentication failed: {auth_response.text}")
        return False
    
    access_token = auth_response.json().get("access_token")
    print("Authentication successful")
    
    # Step 2: Upload resume
    print("Uploading resume...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    with open(RESUME_PATH, "rb") as f:
        files = {"file": (RESUME_PATH.name, f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        upload_response = requests.post(f"{API_URL}/api/resumes/upload", headers=headers, files=files)
    
    if upload_response.status_code != 201:
        print(f"Upload failed: {upload_response.text}")
        return False
    
    result = upload_response.json()
    print("Upload successful!")
    print(f"Resume ID: {result.get('_id')}")
    print(f"Original filename: {result.get('original_filename')}")
    
    return True

if __name__ == "__main__":
    try:
        if test_simple_upload():
            print("\n🎉 Resume upload test completed successfully!")
            exit(0)
        else:
            print("\n❌ Resume upload test failed")
            exit(1)
    except Exception as e:
        print(f"\n❌ Error during test: {str(e)}")
        exit(1) 
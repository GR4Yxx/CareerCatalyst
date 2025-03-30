#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import asyncio
import json
from bson import ObjectId
from pymongo import MongoClient
import datetime
import gridfs
from motor.motor_asyncio import AsyncIOMotorClient
import requests

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(str(Path(__file__).parent.parent.parent))

# Configuration
MONGO_URI = "mongodb://app_user:app_password@localhost:27017/career_catalyst"
MONGO_DB = "career_catalyst"
USER_EMAIL = "xpjosh10@gmail.com"
RESUME_PATH = Path(__file__).parent.parent.parent / "data" / "Resume-Joshua Dsouza.docx"
API_URL = "http://localhost:8000"  # Direct backend URL
NGINX_URL = "http://localhost:80"  # Nginx proxy URL

# Function to convert ObjectId to string for JSON serialization
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

async def test_get_user_resumes():
    """
    Tests uploading a resume and then getting all resumes for a user.
    This helps diagnose the issue with /api/resumes/user endpoint.
    """
    print("=== Testing Get User Resumes ===")
    
    # Step 1: Direct MongoDB upload (bypassing API) to ensure we have a resume
    print("\n--- Direct MongoDB Upload ---")
    
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        
        # Find the user ID
        print(f"Looking up user with email: {USER_EMAIL}")
        user = db.users.find_one({"email": USER_EMAIL})
        
        if not user:
            print(f"Error: User with email {USER_EMAIL} not found")
            return False
        
        user_id = user["_id"]
        print(f"Found user with ID: {user_id}")
        
        # Check if user already has resumes
        existing_resumes = list(db.resumes.find({"user_id": user_id}))
        print(f"User has {len(existing_resumes)} existing resume(s)")
        
        if existing_resumes:
            print("\nExisting resume details:")
            for idx, resume in enumerate(existing_resumes):
                print(f"Resume #{idx+1}:")
                print(f"  ID: {resume['_id']}")
                print(f"  Filename: {resume['original_filename']}")
                print(f"  Is Current: {resume['is_current']}")
                print(f"  Created: {resume['created_at']}")
                
                # Check if this is a valid Resume document with properly serialized IDs
                try:
                    id_str = str(resume['_id'])
                    user_id_str = str(resume['user_id'])
                    print(f"  ID as string: {id_str}")
                    print(f"  User ID as string: {user_id_str}")
                except Exception as e:
                    print(f"  ERROR serializing IDs: {str(e)}")
        
        # If no resumes exist, upload one directly to MongoDB
        if not existing_resumes:
            print("\nNo existing resumes found. Uploading a new resume...")
            
            if not RESUME_PATH.exists():
                print(f"Error: Resume file not found at {RESUME_PATH}")
                return False
            
            # Set all existing resumes to not current
            db.resumes.update_many(
                {"user_id": user_id},
                {"$set": {"is_current": False}}
            )
            
            # Create GridFS
            fs = gridfs.GridFS(db)
            
            # Upload file to GridFS
            with open(RESUME_PATH, "rb") as f:
                file_content = f.read()
                
                metadata = {
                    "file_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    "upload_date": datetime.datetime.utcnow(),
                    "user_id": str(user_id)
                }
                
                file_id = fs.put(
                    file_content, 
                    filename=RESUME_PATH.name, 
                    metadata=metadata
                )
            
            print(f"File uploaded to GridFS with ID: {file_id}")
            
            # Create resume document
            resume_data = {
                "original_filename": RESUME_PATH.name,
                "file_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "file_id": str(file_id),
                "user_id": user_id,
                "created_at": datetime.datetime.utcnow(),
                "is_current": True,
                "parsed_content": {}
            }
            
            result = db.resumes.insert_one(resume_data)
            resume_id = result.inserted_id
            
            print(f"Resume document created with ID: {resume_id}")
        
        # Step 2: Test /api/resumes/user endpoint (will be failing)
        print("\n--- API Get User Resumes Test ---")
        
        # Now test directly against the resumes collection
        resumes = list(db.resumes.find({"user_id": user_id}))
        print(f"MongoDB query found {len(resumes)} resume(s)")
        
        for idx, resume in enumerate(resumes):
            # Convert ObjectId to string for display
            resume_id_str = str(resume["_id"])
            print(f"Resume #{idx+1}: ID = {resume_id_str}, Filename = {resume['original_filename']}")
        
        # Verify each resume can be serialized to JSON properly
        print("\nTesting JSON serialization of resume objects:")
        try:
            json_str = json.dumps(resumes, cls=JSONEncoder)
            print("✅ All resumes can be serialized to JSON")
        except Exception as e:
            print(f"❌ Error serializing resumes to JSON: {str(e)}")
        
        # Get the resume_service.py code that handles the get_resumes_by_user function
        print("\n--- Simulating resume_service.get_resumes_by_user function ---")
        
        # Manually simulate the same code that's failing in the API
        motor_client = AsyncIOMotorClient(MONGO_URI)
        motor_db = motor_client[MONGO_DB]
        
        async def get_resumes_by_user_simulation(user_id):
            cursor = motor_db.resumes.find({"user_id": user_id}).sort("created_at", -1)
            resumes = await cursor.to_list(length=None)
            print(f"Found {len(resumes)} resume(s) in MongoDB")
            
            # Check if we can construct Resume objects
            result = []
            for idx, resume in enumerate(resumes):
                print(f"Processing resume #{idx+1}")
                
                # Print out the raw resume data structure
                print(f"Raw resume data: {json.dumps(resume, cls=JSONEncoder)}")
                
                # Check the types of the fields
                print(f"_id type: {type(resume.get('_id'))}")
                print(f"user_id type: {type(resume.get('user_id'))}")
                
                # Try to manually construct a properly formatted resume dict
                try:
                    formatted_resume = {
                        "_id": str(resume["_id"]),
                        "user_id": str(resume["user_id"]) if "user_id" in resume else None,
                        "profile_id": str(resume["profile_id"]) if "profile_id" in resume else None,
                        "original_filename": resume["original_filename"],
                        "file_type": resume["file_type"],
                        "file_id": resume["file_id"],
                        "created_at": resume["created_at"].isoformat() if isinstance(resume["created_at"], datetime.datetime) else resume["created_at"],
                        "is_current": resume["is_current"],
                        "parsed_content": resume.get("parsed_content", {})
                    }
                    result.append(formatted_resume)
                    print(f"✅ Successfully formatted resume #{idx+1}")
                except Exception as e:
                    print(f"❌ Error formatting resume #{idx+1}: {str(e)}")
            
            return result
        
        formatted_resumes = await get_resumes_by_user_simulation(user_id)
        print(f"\nSuccessfully formatted {len(formatted_resumes)} resume(s) for API response")
        
        # Step 3: Test the API endpoint through direct backend
        print("\n--- Testing Direct Backend API ---")
        
        # First authenticate to get a token
        auth_data = {
            "username": USER_EMAIL,
            "password": "lol123456"
        }
        
        auth_response = requests.post(f"{API_URL}/auth/login", data=auth_data)
        
        if auth_response.status_code != 200:
            print(f"Authentication failed with status {auth_response.status_code}: {auth_response.text}")
            return False
        
        access_token = auth_response.json().get("access_token")
        print("Authentication successful")
        
        # Call the get user resumes endpoint
        headers = {"Authorization": f"Bearer {access_token}"}
        resumes_response = requests.get(f"{API_URL}/resumes/user", headers=headers)
        
        print(f"Direct API Response Status: {resumes_response.status_code}")
        
        if resumes_response.status_code == 200:
            resumes_data = resumes_response.json()
            print(f"API returned {len(resumes_data)} resume(s)")
            print("✅ Direct API request successful")
        else:
            print(f"❌ Direct API request failed: {resumes_response.text}")
        
        # Step 4: Test the API endpoint through nginx
        print("\n--- Testing Through Nginx ---")
        
        # Authenticate through nginx
        nginx_auth_response = requests.post(f"{NGINX_URL}/api/auth/login", data=auth_data)
        
        if nginx_auth_response.status_code != 200:
            print(f"Nginx authentication failed with status {nginx_auth_response.status_code}: {nginx_auth_response.text}")
            return False
        
        nginx_access_token = nginx_auth_response.json().get("access_token")
        print("Nginx authentication successful")
        
        # Call the get user resumes endpoint through nginx
        nginx_headers = {"Authorization": f"Bearer {nginx_access_token}"}
        nginx_resumes_response = requests.get(f"{NGINX_URL}/api/resumes/user", headers=nginx_headers)
        
        print(f"Nginx API Response Status: {nginx_resumes_response.status_code}")
        
        if nginx_resumes_response.status_code == 200:
            nginx_resumes_data = nginx_resumes_response.json()
            print(f"Nginx API returned {len(nginx_resumes_data)} resume(s)")
            print("✅ Nginx API request successful")
        else:
            print(f"❌ Nginx API request failed: {nginx_resumes_response.text}")
            
        # Compare the two responses
        print("\n--- Comparing Direct Backend vs Nginx Results ---")
        if resumes_response.status_code == 200 and nginx_resumes_response.status_code == 200:
            print("Both direct backend and nginx requests were successful")
            
            direct_data = resumes_response.json()
            nginx_data = nginx_resumes_response.json()
            
            if len(direct_data) == len(nginx_data):
                print(f"Both returned the same number of resumes: {len(direct_data)}")
            else:
                print(f"Different number of resumes: Direct={len(direct_data)}, Nginx={len(nginx_data)}")
                
        elif resumes_response.status_code == 200:
            print("Only direct backend request was successful")
        elif nginx_resumes_response.status_code == 200:
            print("Only nginx request was successful")
        else:
            print("Both requests failed - backend issue with resume retrieval")
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        # Close the MongoDB connection
        if 'client' in locals():
            client.close()
            print("MongoDB connection closed")
        if 'motor_client' in locals():
            motor_client.close()
            print("Motor MongoDB connection closed")

if __name__ == "__main__":
    try:
        asyncio.run(test_get_user_resumes())
    except Exception as e:
        print(f"Test error: {str(e)}")
        sys.exit(1) 
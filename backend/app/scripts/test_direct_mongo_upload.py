#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import datetime
import gridfs
from pymongo import MongoClient
from bson import ObjectId

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(str(Path(__file__).parent.parent.parent))

# Configuration
MONGO_URI = "mongodb://app_user:app_password@localhost:27017/career_catalyst"
MONGO_DB = "career_catalyst"
USER_EMAIL = "xpjosh10@gmail.com"
RESUME_PATH = Path(__file__).parent.parent.parent / "data" / "Resume-Joshua Dsouza.docx"

def test_direct_upload():
    """
    A script to test uploading a resume directly to MongoDB,
    bypassing the API to avoid any validation errors.
    """
    if not RESUME_PATH.exists():
        print(f"Error: Resume file not found at {RESUME_PATH}")
        return False
    
    print(f"Using resume file: {RESUME_PATH}")
    
    try:
        # Connect to MongoDB
        print(f"Connecting to MongoDB at {MONGO_URI}...")
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        
        # Check connection
        db.command("ping")
        print("Connected to MongoDB successfully")
        
        # Find the user ID
        print(f"Looking up user with email: {USER_EMAIL}")
        user = db.users.find_one({"email": USER_EMAIL})
        
        if not user:
            print(f"Error: User with email {USER_EMAIL} not found")
            return False
        
        user_id = user["_id"]
        print(f"Found user with ID: {user_id}")
        
        # Set all existing resumes for this user to not current
        print("Setting existing resumes to not current...")
        db.resumes.update_many(
            {"user_id": user_id},
            {"$set": {"is_current": False}}
        )
        
        # Create GridFS
        fs = gridfs.GridFS(db)
        
        # Upload file to GridFS
        print("Uploading file to GridFS...")
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
        print("Creating resume document...")
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
        
        # Verify the upload by retrieving the file
        print("Verifying upload by retrieving file...")
        file_obj = fs.get(file_id)
        print(f"Retrieved file with name: {file_obj.filename}")
        print(f"File metadata: {file_obj.metadata}")
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        # Close the MongoDB connection
        if 'client' in locals():
            client.close()
            print("MongoDB connection closed")

if __name__ == "__main__":
    if test_direct_upload():
        print("\n🎉 Direct resume upload test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Direct resume upload test failed")
        sys.exit(1) 
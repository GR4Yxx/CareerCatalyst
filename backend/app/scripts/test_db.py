#!/usr/bin/env python
"""
Simple script to test MongoDB connection and create a test user.
"""

import asyncio
import logging
from datetime import datetime
from pydantic import EmailStr
from passlib.context import CryptContext

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Use direct MongoDB connection for simplicity
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    """Test MongoDB connection and create a test user."""
    logger.info("Testing MongoDB connection...")
    
    # MongoDB connection string - using the Docker service name
    mongo_uri = "mongodb://app_user:app_password@mongodb:27017/career_catalyst"
    
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongo_uri)
        db = client.career_catalyst
        
        # Simple ping to verify connection
        await db.command("ping")
        logger.info("MongoDB connection successful!")
        
        # Create a test user
        test_user = {
            "email": "test@example.com",
            "name": "Test User",
            "hashed_password": pwd_context.hash("password123"),
            "created_at": datetime.utcnow()
        }
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": test_user["email"]})
        if existing_user:
            logger.info(f"User {test_user['email']} already exists")
        else:
            result = await db.users.insert_one(test_user)
            logger.info(f"Created test user with ID: {result.inserted_id}")
        
        # List all users
        logger.info("Listing all users:")
        async for user in db.users.find():
            logger.info(f"User: {user['name']} ({user['email']})")
        
    except Exception as e:
        logger.error(f"MongoDB connection error: {str(e)}")
        raise
    finally:
        # Close MongoDB connection
        if 'client' in locals():
            client.close()
            logger.info("MongoDB connection closed")

if __name__ == "__main__":
    asyncio.run(main()) 
from typing import Optional, Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from bson import ObjectId
import io

from ..db.mongodb import get_database

async def upload_file(file_content: bytes, filename: str, metadata: Optional[Dict[str, Any]] = None) -> str:
    """
    Upload a file to GridFS and return the file_id
    """
    db = get_database()
    fs = AsyncIOMotorGridFSBucket(db)
    
    # Create a file-like object from bytes
    file_data = io.BytesIO(file_content)
    
    # Upload the file
    grid_in_options = {}
    if metadata:
        grid_in_options["metadata"] = metadata
    
    file_id = await fs.upload_from_stream(
        filename,
        file_data,
        metadata=metadata
    )
    
    return str(file_id)

async def download_file(file_id: str) -> Optional[bytes]:
    """
    Download a file from GridFS
    """
    db = get_database()
    fs = AsyncIOMotorGridFSBucket(db)
    
    # Create a buffer to store the file content
    buffer = io.BytesIO()
    
    try:
        # Download the file
        await fs.download_to_stream(ObjectId(file_id), buffer)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None

async def delete_file(file_id: str) -> bool:
    """
    Delete a file from GridFS
    """
    db = get_database()
    fs = AsyncIOMotorGridFSBucket(db)
    
    try:
        await fs.delete(ObjectId(file_id))
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

async def get_file_metadata(file_id: str) -> Optional[Dict[str, Any]]:
    """
    Get file metadata from GridFS
    """
    db = get_database()
    fs_files = db["fs.files"]
    
    try:
        file_info = await fs_files.find_one({"_id": ObjectId(file_id)})
        return file_info
    except Exception as e:
        print(f"Error getting file metadata: {e}")
        return None

async def list_files(filter_query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    List files in GridFS matching the filter
    """
    db = get_database()
    fs_files = db["fs.files"]
    
    filter_query = filter_query or {}
    
    cursor = fs_files.find(filter_query)
    files = await cursor.to_list(length=None)
    
    return files 
# Resume Upload Test Scripts

This directory contains various scripts for testing the resume upload functionality in the CareerCatalyst application.

## Issue Summary

When attempting to upload resumes through the API, we encountered a Pydantic validation error related to MongoDB's ObjectId:

```
{"detail":"1 validation error for Resume\n_id\n  Input should be a valid string [type=string_type, input_value=ObjectId('67e90c7b1b93bae9b7949888'), input_type=ObjectId]\n    For further information visit https://errors.pydantic.dev/2.3/v/string_type"}
```

This error occurs because the backend is trying to serialize a MongoDB ObjectId directly into a Pydantic model, causing validation issues.

## Available Scripts

### 1. `test_resume_upload.py`

This is the original test script that attempts to upload a resume through the API. It uses `aiohttp` to:

- Authenticate a user
- Upload a resume file from the data directory
- Verify the upload response contains the expected data
- Download the uploaded resume to verify it matches

```bash
python -m app.scripts.test_resume_upload
```

### 2. `test_resume_upload_debug.py`

A debug version of the script that provides more verbose output, trying both the nginx endpoint and direct backend connection:

```bash
python -m app.scripts.test_resume_upload_debug
```

### 3. `test_simple_upload.py`

A simplified version using the `requests` library instead of `aiohttp`:

```bash
python -m app.scripts.test_simple_upload
```

### 4. `test_direct_mongo_upload.py` (Working Solution)

This script bypasses the API entirely and uploads the resume directly to MongoDB using `pymongo`. It:

- Connects directly to the MongoDB database
- Looks up the user by email
- Uploads the file to GridFS
- Creates a resume document in the database

```bash
python -m app.scripts.test_direct_mongo_upload
```

## How to Use

To test resume uploading for a specific user, modify the corresponding script's configuration variables:

```python
USER_EMAIL = "xpjosh10@gmail.com"
USER_PASSWORD = "lol123456"  # Only needed for API-based scripts
RESUME_PATH = Path(__file__).parent.parent.parent / "data" / "Resume-Joshua Dsouza.docx"
```

## Backend Issue and Recommendation

The API validation error is likely caused by how the Resume model handles MongoDB ObjectId serialization. The backend should be updated to properly handle the conversion between ObjectId and string types in the Resume model.

A potential fix would be to update the PyObjectId class in models/user.py to ensure proper serialization/deserialization or to modify the Resume model's field serializers.

## Requirements

These scripts require:

- Python 3.8+
- aiohttp (for test_resume_upload.py and test_resume_upload_debug.py)
- requests (for test_simple_upload.py)
- pymongo (for test_direct_mongo_upload.py)

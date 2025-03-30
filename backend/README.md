# CareerCatalyst Backend

## Overview

This is the backend API for the CareerCatalyst platform - an AI-powered career navigation system. It provides RESTful endpoints for resume processing, skill extraction, job recommendations, ATS optimization, and career path visualization.

## Technology Stack

- **Framework**: FastAPI
- **Containerization**: Docker
- **Reverse Proxy**: Nginx
- **Database**: MongoDB
- **ML/AI Components**: spaCy for NLP, Gemini API for LLM capabilities

## Project Structure

## Setup and Configuration

1. Clone the repository
2. Create a `.env` file based on the `.env.example` template
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Gemini API Key Setup

The Skills Intelligence feature uses Google's Gemini API to analyze resumes and extract skills. To set this up:

1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/)
2. Add your API key to the `.env` file:
   ```
   GEMINI_API_KEY=your-gemini-api-key
   ```
3. If you don't provide a Gemini API key, the system will fall back to basic pattern matching

For more details on the Skill Intelligence feature, see [Skills Intelligence Documentation](../docs/skill_intelligence.md).

## Running the Application

To run the application locally:

```bash
uvicorn app.main:app --reload
```

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Dict, List, Optional
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="CareerCatalyst API",
    description="API for AI-powered career navigation system",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Skill(BaseModel):
    name: str
    category: str
    confidence: float
    experience_years: Optional[float] = None

class SkillProfile(BaseModel):
    skills: List[Skill]
    total_skills: int

class JobRecommendation(BaseModel):
    job_id: str
    title: str
    company: str
    match_percentage: float
    location: str
    salary_range: Optional[str] = None
    description: str

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to CareerCatalyst API", "status": "operational"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/skills/profile", response_model=SkillProfile)
async def get_skills_profile():
    # Dummy data for demonstration
    skills = [
        Skill(name="Python", category="Programming Language", confidence=0.95, experience_years=3.5),
        Skill(name="FastAPI", category="Framework", confidence=0.88, experience_years=1.2),
        Skill(name="Data Analysis", category="Domain Knowledge", confidence=0.85, experience_years=2.0),
        Skill(name="Project Management", category="Soft Skill", confidence=0.78, experience_years=4.0),
    ]
    return SkillProfile(skills=skills, total_skills=len(skills))

@app.get("/api/jobs/recommendations", response_model=List[JobRecommendation])
async def get_job_recommendations():
    # Dummy data for demonstration
    recommendations = [
        JobRecommendation(
            job_id="job123",
            title="Senior Python Developer",
            company="TechCorp Inc.",
            match_percentage=87.5,
            location="Remote",
            salary_range="$110,000 - $130,000",
            description="Senior developer position focused on building scalable APIs and services."
        ),
        JobRecommendation(
            job_id="job456",
            title="Data Scientist",
            company="Analytics Co.",
            match_percentage=82.3,
            location="New York, NY",
            salary_range="$95,000 - $120,000",
            description="Data science role with focus on machine learning models and data analysis."
        )
    ]
    return recommendations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 
from fastapi import APIRouter
from .endpoints import auth, profiles, resumes, skills, jobs, ats

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["Profiles"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])
api_router.include_router(skills.router, prefix="/skills", tags=["Skills"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(ats.router, prefix="/ats", tags=["ATS"])
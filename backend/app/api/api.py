from fastapi import APIRouter
from .endpoints import auth, profiles, resumes

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["Profiles"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["Resumes"]) 
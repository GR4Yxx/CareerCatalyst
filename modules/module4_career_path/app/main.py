# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from modules.module4_career_path.recommender import recommend_career_and_skills

app = FastAPI()

class RecommendationRequest(BaseModel):
    user_id: str
    current_job_tag: str
    resume_text: str

class RecommendationResponse(BaseModel):
    recommended_tracks: List[str]
    skills_to_learn: List[str]

@app.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(request: RecommendationRequest):
    tracks, skills = recommend_career_and_skills(request.current_job_tag, request.resume_text)
    return RecommendationResponse(
        recommended_tracks=tracks,
        skills_to_learn=skills
    )

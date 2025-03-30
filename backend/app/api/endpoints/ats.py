from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Body, File, UploadFile, status
from fastapi.responses import StreamingResponse, FileResponse
from typing import Dict, List, Optional, Any
import logging
import io
import tempfile
import os
import subprocess
import json
from datetime import datetime
from bson import ObjectId
from types import SimpleNamespace
import google.generativeai as genai
import time

from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job
from app.services import resume_service, user_service, job_service
from app.utils import gridfs
from ..endpoints.auth import get_current_user
from pydantic import BaseModel

# Define models for request and response
class ResumeOptimizationRequest(BaseModel):
    resumeId: str
    jobDescription: str
    requiredSkills: Optional[List[str]] = []

class ResumeOptimizationResponse(BaseModel):
    latexCode: str

# Configure logging
logger = logging.getLogger(__name__)

# Define Gemini API key
GEMINI_API_KEY = "AIzaSyAEO9xdicSGhXeChy5x7sFxcDYTrFhzLUc"
GEMINI_AVAILABLE = True

router = APIRouter()

@router.post("/analyze")
async def analyze_resume(
    data: dict = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze a resume against a job description
    """
    resume_id = data.get("resumeId")
    job_description = data.get("jobDescription")
    
    if not resume_id or not job_description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both resumeId and jobDescription are required"
        )
    
    # Get the resume
    resume = await resume_service.get_resume_by_id(resume_id)
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Here you would implement the actual ATS analysis logic
    # For now, we'll return mock data
    
    return {
        "score": 72,
        "suggestions": [
            {"type": "warning", "message": "Add more specific technical skills relevant to the job description"},
            {"type": "warning", "message": "Use more industry standard terminology in your experience section"},
            {"type": "success", "message": "Your resume format is ATS-friendly"}
        ],
        "keywordAnalysis": [
            {"name": "Vue.js", "found": True},
            {"name": "TypeScript", "found": True},
            {"name": "CI/CD Experience", "found": False},
            {"name": "Agile Development", "found": True}
        ]
    }

@router.post("/optimize-resume")
async def optimize_resume(
    request: ResumeOptimizationRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Optimize a resume based on job description and required skills.
    Uses the actual resume data from the database and Gemini API for optimization.
    Saves the LaTeX code as a .tex file for download.
    """
    resume_id = request.resumeId
    job_description = request.jobDescription
    required_skills = request.requiredSkills
    
    logger.info(f"Optimize resume request received for resume_id: {resume_id}")
    logger.info(f"Gemini available: {GEMINI_AVAILABLE}")
    
    # Get the actual resume from the database
    try:
        resume = await resume_service.get_resume_by_id(resume_id)
        if not resume:
            logger.error(f"Resume not found with ID: {resume_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        logger.info(f"Resume found, using real resume data for optimization")
    except Exception as e:
        logger.error(f"Error retrieving resume: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume not found: {str(e)}"
        )
    
    # Get resume content if available
    resume_content = {}
    if hasattr(resume, 'parsed_content') and resume.parsed_content:
        resume_content = resume.parsed_content
        logger.info(f"Resume content available, keys: {resume_content.keys() if resume_content else 'None'}")
    else:
        logger.warning(f"No parsed content available for resume: {resume_id}")
        # Create minimal resume data with user email
        resume_content = {
            "email": current_user.email,
            "name": current_user.name if hasattr(current_user, 'name') else current_user.email.split('@')[0],
            "skills": [{"name": skill} for skill in required_skills] if required_skills else []
        }
        logger.info(f"Created minimal resume content with email and name")

    # Generate the LaTeX content using Gemini or fallback
    latex_code = await optimize_resume_with_gemini(current_user.email, required_skills, job_description, resume_content) if resume_content and GEMINI_AVAILABLE else generate_mock_latex_resume(resume_content.get("name", current_user.name if hasattr(current_user, 'name') else current_user.email.split('@')[0]), current_user.email, required_skills, job_description, [skill.get("name", "") for skill in resume_content.get("skills", [])] if resume_content and "skills" in resume_content else [])
    
    # Create a unique filename for the .tex file
    current_time = int(time.time())
    file_name = f"optimized_resume_{current_time}.tex"
    
    # Change from /app/data/temp to /tmp which should be writable
    temp_dir = "/tmp"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Save the LaTeX code to a file
    file_path = os.path.join(temp_dir, file_name)
    with open(file_path, "w") as f:
        f.write(latex_code)
    
    logger.info(f"LaTeX resume saved to {file_path}")
    
    # Generate download URL
    download_url = f"/api/ats/download-tex/{file_name}"
    
    # Return the LaTeX code and file info
    return {
        "latexCode": latex_code,  # Return the full code
        "filename": file_name,
        "downloadUrl": download_url
    }

@router.get("/download-tex/{filename}")
async def download_tex_file(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    """
    Download the generated LaTeX file
    """
    file_path = os.path.join("/tmp", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/x-tex"
    )

def generate_mock_latex_resume(name, email, required_skills, job_description, user_skills=None):
    """
    Generate a mock LaTeX resume as a fallback when Gemini is not available.
    Creates a concise, job-focused resume with only relevant skills and experience.
    
    Args:
        name: User's name
        email: User's email
        required_skills: List of skills required for the job
        job_description: Description of the job
        user_skills: User's existing skills
    
    Returns:
        String containing LaTeX code for the resume
    """
    logger.warning("Generating mock LaTeX resume as fallback")
    
    # Define skills section - prioritize required skills
    if required_skills:
        skills_list = required_skills
        if user_skills:
            # Find matching skills first
            matching_skills = [skill for skill in user_skills if skill.lower() in [req.lower() for req in required_skills]]
            # Then add other required skills
            remaining_required = [skill for skill in required_skills if skill.lower() not in [match.lower() for match in matching_skills]]
            # Limit to 8 skills maximum with priority to matching skills
            skills_list = matching_skills + remaining_required
            skills_list = skills_list[:8]
    else:
        skills_list = user_skills if user_skills else ["Problem Solving", "Communication", "Technical Writing", "Teamwork"]
    
    skills_section = ", ".join(skills_list)
    
    # Extract key terms from job description for the summary
    key_terms = []
    if job_description:
        # Simple extraction of capitalized terms as potential keywords
        words = job_description.split()
        key_terms = [word for word in words if word[0].isupper() and len(word) > 3]
        key_terms = list(set(key_terms))[:5]  # Take up to 5 unique terms
    
    # Create a simple but professional-looking LaTeX resume focused on relevance
    return r"""\documentclass[10pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[margin=0.6in]{geometry}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{fontawesome}
\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=blue}
\pagestyle{empty}

% Custom section command
\newcommand{\resumesection}[1]{%
  \section*{#1}
  \vspace{-0.3cm}
  \hrule
  \vspace{0.2cm}
}

% Custom item command
\newcommand{\resumeitem}[1]{\item[\small\textbullet] #1}

\begin{document}

% Header
\begin{center}
    {\Large\textbf{""" + name + r"""}}\\
    \vspace{0.1cm}
    \href{mailto:""" + email + r"""}{""" + email + r"""}
\end{center}

% Summary
\resumesection{Professional Summary}
Results-driven professional with expertise in """ + skills_section + r""". Passionate about delivering high-quality solutions """ + (f"in the field of {key_terms[0]}" if key_terms else "that meet business requirements") + r""".

% Skills
\resumesection{Core Technical Skills}
""" + skills_section + r"""

% Experience
\resumesection{Relevant Experience}
\textbf{Senior Software Engineer} \\
\textit{Technology Solutions Inc.} \hfill 2020--Present
\begin{itemize}[leftmargin=*,itemsep=0.1em,parsep=0pt]
    \resumeitem{Developed and implemented """ + (skills_list[0] if skills_list else "technology") + r"""-based solutions, improving system performance by 40\%}
    \resumeitem{Collaborated with cross-functional teams to deliver high-impact projects on time and within budget}
\end{itemize}

\vspace{0.1cm}
\textbf{Software Developer} \\
\textit{Innovative Systems} \hfill 2017--2020
\begin{itemize}[leftmargin=*,itemsep=0.1em,parsep=0pt]
    \resumeitem{Implemented features using """ + (skills_list[1] if len(skills_list) > 1 else "advanced technologies") + r""", reducing system errors by 60\%}
    \resumeitem{Mentored junior developers and established best practices for code quality and testing}
\end{itemize}

% Education
\resumesection{Education}
\textbf{Bachelor of Science in Computer Science}\\
\textit{University of Technology} \hfill 2013--2017

\end{document}"""

def clean_latex_code(latex_code: str) -> str:
    """Clean the LaTeX code by removing any Markdown formatting."""
    if latex_code.startswith("```latex"):
        latex_code = latex_code[8:]
    elif latex_code.startswith("```"):
        latex_code = latex_code[3:]
    
    if latex_code.endswith("```"):
        latex_code = latex_code[:-3]
    
    return latex_code.strip()

async def optimize_resume_with_gemini(email, required_skills, job_description, resume_content):
    """Use Google's Gemini to optimize a resume for ATS by fine-tuning the existing resume data."""
    logger.info(f"Optimizing resume with Gemini for email: {email}, job requires skills: {required_skills}")
    
    # Configure Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info(f"Configured Gemini with API key: {GEMINI_API_KEY[:4]}...{GEMINI_API_KEY[-4:]}")
    
    # Extract the user's name
    name = resume_content.get("name", "Applicant")
    
    # Format the resume data for the prompt
    resume_data = "Resume Details:\n"
    
    # Add skills information
    if resume_content and "skills" in resume_content:
        skills = [skill.get("name", "") for skill in resume_content.get("skills", [])]
        resume_data += f"Skills: {', '.join(skills)}\n\n"
    
    # Add education information
    if resume_content and "education" in resume_content:
        education = resume_content.get("education", [])
        resume_data += "Education:\n"
        for edu in education:
            school = edu.get("school", "")
            degree = edu.get("degree", "")
            field = edu.get("field", "")
            start_date = edu.get("startDate", "")
            end_date = edu.get("endDate", "")
            resume_data += f"- {degree} in {field} from {school}, {start_date} to {end_date}\n"
        resume_data += "\n"
    
    # Add work history information
    if resume_content and "workHistory" in resume_content:
        experience = resume_content.get("workHistory", [])
        resume_data += "Work Experience:\n"
        for work in experience:
            company = work.get("company", "")
            title = work.get("title", "")
            start_date = work.get("startDate", "")
            end_date = work.get("endDate", "Current")
            description = work.get("description", "")
            resume_data += f"- {title} at {company}, {start_date} to {end_date}\n"
            resume_data += f"  Description: {description}\n"
        resume_data += "\n"
    
    # Add projects if available
    if resume_content and "projects" in resume_content:
        projects = resume_content.get("projects", [])
        resume_data += "Projects:\n"
        for project in projects:
            title = project.get("title", "")
            description = project.get("description", "")
            resume_data += f"- {title}: {description}\n"
        resume_data += "\n"
    
    # Format prompt for Gemini, focusing on fine-tuning the existing resume
    prompt = (
        "I need to create a highly professional, ATS-optimized resume for a specific job application.\n"
        f"\nMy information:\nName: {name}\nEmail: {email}\n"
        f"\n{resume_data}\n"
        f"Job Description I'm applying for:\n{job_description}\n"
        f"\nThe job requires these skills: {', '.join(required_skills) if required_skills else 'Not specified'}\n"
        "\nPlease create a polished, professional ONE-PAGE resume that will excel in ATS systems while presenting my qualifications in the best possible light:\n"
        "\n1. Create a clean, modern LaTeX resume with professional typography and spacing"
        "\n2. Include ONLY skills and experiences directly relevant to this specific job description"
        "\n3. If you don't have complete information for a section, either omit that section entirely or create a minimal version with only the information you have - DO NOT include placeholder text like 'Company Name' or 'Dates of Employment'"
        "\n4. Strategically incorporate keywords from the job description in appropriate contexts"
        "\n5. For work experience, create compelling, achievement-oriented bullet points that quantify impact where possible"
        "\n6. Use a modern, elegant LaTeX template with subtle styling (nothing flashy that would confuse ATS)"
        "\n7. Ensure proper vertical spacing and margins (0.5-0.7 inches) to fit everything on ONE PAGE"
        "\n8. Use semantic LaTeX markup for better document structure"
        "\n\nFormat requirements:"
        "\n- Use a clean, professional LaTeX template design"
        "\n- Optimize white space intelligently - compact but not crowded"
        "\n- Ensure perfect formatting with no errors or placeholder text"
        "\n- Use appropriate font sizing and weights for hierarchy"
        "\n- If exact dates aren't provided, either omit them or use general timeframes based on the data available"
        "\n\nThe complete LaTeX code should start with \\documentclass and include all necessary packages, formatting, and content."
        "\nReturn only the complete, error-free LaTeX code without any explanations or markdown formatting."
    )
    
    logger.info("Sending request to Gemini API")
    
    try:
        # Get response from Gemini
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        
        # Extract the LaTeX code from the response
        latex_code = response.text.strip()
        logger.info(f"Received response from Gemini, length: {len(latex_code)}")
        
        # Clean up Markdown formatting
        latex_code = clean_latex_code(latex_code)
        
        # If the response doesn't look like LaTeX, create a fallback
        if not latex_code.startswith("\\documentclass") and not "\\begin{document}" in latex_code:
            logger.warning("Response doesn't appear to be valid LaTeX, generating fallback")
            return generate_mock_latex_resume(name, email, required_skills, job_description, [skill.get("name", "") for skill in resume_content.get("skills", [])] if resume_content and "skills" in resume_content else [])
        
        return latex_code
    except Exception as e:
        logger.error(f"Error using Gemini API: {str(e)}")
        # Generate a fallback if Gemini fails
        return generate_mock_latex_resume(name, email, required_skills, job_description, [skill.get("name", "") for skill in resume_content.get("skills", [])] if resume_content and "skills" in resume_content else [])
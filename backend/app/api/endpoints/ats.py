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

@router.post("/optimize-resume", response_model=ResumeOptimizationResponse)
async def optimize_resume(
    request: ResumeOptimizationRequest,
    # Comment out the current_user dependency for testing
    # current_user: User = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Optimize a resume based on job description and required skills.
    """
    resume_id = request.resumeId
    job_description = request.jobDescription
    required_skills = request.requiredSkills
    
    # For testing purposes, use a mock user
    user = SimpleNamespace(email="test@example.com", name="Test User")
    
    logger.info(f"Optimize resume request received for resume_id: {resume_id}")
    logger.info(f"Gemini available: {GEMINI_AVAILABLE}")
    
    # Get the resume
    try:
        # Mock resume for testing
        resume = SimpleNamespace(parsed_content=None)
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
            "email": user.email,
            "name": user.name if hasattr(user, 'name') else "User",
            "skills": [{"name": skill} for skill in required_skills] if required_skills else []
        }
        logger.info(f"Created minimal resume content with email and name")

    # Use Gemini to optimize the resume if available
    if GEMINI_AVAILABLE:
        try:
            logger.info(f"Attempting to use Gemini for resume optimization")
            latex_code = await optimize_resume_with_gemini(
                user.email, 
                required_skills, 
                job_description, 
                resume_content
            )
            logger.info(f"Successfully generated resume with Gemini, length: {len(latex_code)}")
            return {"latexCode": latex_code}
        except Exception as e:
            logger.error(f"Error optimizing resume with Gemini: {str(e)}")
            # Fall back to template if Gemini fails
            logger.info("Falling back to template resume")
    else:
        logger.warning(f"Not using Gemini. GEMINI_AVAILABLE={GEMINI_AVAILABLE}")
        logger.info("Falling back to template resume")

    # Fall back to template resume
    logger.info(f"Generating mock resume for {user.email} with {len(required_skills) if required_skills else 0} required skills")
    user_skills = []
    if resume_content and "skills" in resume_content:
        user_skills = [skill.get("name", "") for skill in resume_content.get("skills", [])]
    name = resume_content.get("name", user.name if hasattr(user, 'name') else "Applicant")
    latex_code = generate_mock_latex_resume(name, user.email, required_skills, job_description, user_skills)

    return {"latexCode": latex_code}

@router.post("/latex-to-pdf")
async def latex_to_pdf(
    data: dict = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Convert LaTeX code to PDF
    """
    latex_code = data.get("latex")
    
    if not latex_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="LaTeX code is required"
        )
    
    try:
        # Create a temporary directory to hold the LaTeX files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a temporary file for the LaTeX source
            tex_file_path = os.path.join(temp_dir, "resume.tex")
            pdf_file_path = os.path.join(temp_dir, "resume.pdf")
            
            # Write the LaTeX code to the temporary file
            with open(tex_file_path, "w") as tex_file:
                tex_file.write(latex_code)
            
            # Run pdflatex to convert LaTeX to PDF
            try:
                process = subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", "-output-directory", temp_dir, tex_file_path],
                    capture_output=True,
                    check=True,
                    timeout=30  # Timeout after 30 seconds
                )
                
                if not os.path.exists(pdf_file_path):
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to generate PDF"
                    )
                
                # Read the PDF file
                with open(pdf_file_path, "rb") as pdf_file:
                    pdf_content = pdf_file.read()
                
                # Return the PDF as a streaming response
                return StreamingResponse(
                    io.BytesIO(pdf_content),
                    media_type="application/pdf",
                    headers={"Content-Disposition": "attachment; filename=optimized_resume.pdf"}
                )
                
            except subprocess.CalledProcessError as e:
                # Log the error output for debugging
                logger.error(f"pdflatex error: {e.stderr.decode()}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error converting LaTeX to PDF"
                )
            except subprocess.TimeoutExpired:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="PDF generation timed out"
                )
    except Exception as e:
        logger.error(f"Unexpected error in latex_to_pdf: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate PDF: {str(e)}"
        )

def generate_mock_latex_resume(name, email, required_skills, job_description, user_skills=None):
    """
    Generate a mock LaTeX resume as a fallback when Gemini is not available.
    
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
    
    # Define skills section
    if required_skills:
        skills_list = required_skills
        if user_skills:
            # Combine user skills with required skills, removing duplicates
            all_skills = list(set(required_skills + user_skills))
            skills_list = all_skills[:10]  # Limit to 10 skills
    else:
        skills_list = user_skills if user_skills else ["Python", "JavaScript", "React", "Node.js", "SQL"]
    
    skills_section = ", ".join(skills_list)
    
    # Create a simple but professional-looking LaTeX resume
    return r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[margin=1in]{geometry}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{xcolor}
\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=blue}
\pagestyle{empty}

\begin{document}

\begin{center}
    {\LARGE \textbf{""" + name + r"""}}\\
    \vspace{0.1in}
    """ + email + r"""
\end{center}

\noindent\rule{\textwidth}{1pt}

\section*{Summary}
Results-driven professional with experience in software development and data analysis. Strong problem-solving skills and ability to adapt to new technologies quickly. Seeking to leverage my technical expertise and communication skills to contribute to innovative projects.

\section*{Education}
\textbf{Bachelor of Science in Computer Science}\\
University of Technology\\
2015 - 2019

\section*{Professional Experience}
\textbf{Software Developer} \hfill 2019 - Present\\
Tech Solutions Inc.
\begin{itemize}[leftmargin=*]
    \item Developed and maintained web applications using modern technologies
    \item Collaborated with cross-functional teams to deliver high-quality products
    \item Implemented automated testing strategies to improve code quality
    \item Optimized application performance, resulting in 30\% faster load times
\end{itemize}

\textbf{Software Engineering Intern} \hfill Summer 2018\\
Innovative Software Company
\begin{itemize}[leftmargin=*]
    \item Assisted in developing new features for the company's flagship product
    \item Participated in code reviews and implemented feedback from senior developers
    \item Created documentation for API endpoints and common procedures
\end{itemize}

\section*{Technical Skills}
""" + skills_section + r"""

\section*{Projects}
\textbf{Personal Portfolio Website}
\begin{itemize}[leftmargin=*]
    \item Designed and implemented a responsive portfolio website
    \item Utilized modern web development practices for optimal performance
\end{itemize}

\textbf{Data Analysis Tool}
\begin{itemize}[leftmargin=*]
    \item Created a tool to analyze and visualize large datasets
    \item Implemented algorithms to identify patterns and generate insights
\end{itemize}

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
    """Use Google's Gemini to optimize a resume for ATS."""
    logger.info(f"Optimizing resume with Gemini for email: {email}, job requires skills: {required_skills}")
    
    # Configure Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info(f"Configured Gemini with API key: {GEMINI_API_KEY[:4]}...{GEMINI_API_KEY[-4:]}")
    
    # Extract relevant information from resume_content
    skills = []
    if resume_content and "skills" in resume_content:
        skills = [skill.get("name", "") for skill in resume_content.get("skills", [])]
    
    education = []
    if resume_content and "education" in resume_content:
        education = resume_content.get("education", [])
    
    experience = []
    if resume_content and "workHistory" in resume_content:
        experience = resume_content.get("workHistory", [])
    
    name = resume_content.get("name", "Applicant")
    
    # Format prompt for Gemini
    prompt = f"""
    I need to create a LaTeX-formatted resume that will pass through Applicant Tracking Systems (ATS) well.

    Here's the information:
    
    Name: {name}
    Contact: {email}
    
    Job Description: {job_description}
    
    Required Skills: {", ".join(required_skills) if required_skills else "None provided"}
    
    My Current Skills: {", ".join(skills) if skills else "None provided"}
    
    Education: {json.dumps(education) if education else "None provided"}
    
    Work Experience: {json.dumps(experience) if experience else "None provided"}
    
    Please generate a complete LaTeX resume document that:
    1. Is optimized for ATS using the skills from the job description
    2. Has a professional layout with appropriate sections
    3. Includes all the LaTeX formatting commands and document structure
    4. Uses a clean, professional template
    5. Has proper spacing and formatting
    
    Return the LaTeX code without any Markdown formatting or explanation.
    """
    
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
            return generate_mock_latex_resume(name, email, required_skills, job_description, skills)
        
        return latex_code
    except Exception as e:
        logger.error(f"Error using Gemini API: {str(e)}")
        # Generate a fallback if Gemini fails
        return generate_mock_latex_resume(name, email, required_skills, job_description, skills)
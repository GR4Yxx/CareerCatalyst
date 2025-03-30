from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Body, File, UploadFile, status
from fastapi.responses import StreamingResponse, FileResponse
from typing import Dict, List, Optional, Any
import logging
import io
import tempfile
import os
import subprocess
from datetime import datetime
from bson import ObjectId

from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job
from app.services import resume_service, user_service, job_service
from app.utils import gridfs
from ..endpoints.auth import get_current_user

# Configure logging
logger = logging.getLogger(__name__)

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
    data: dict = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Generate an optimized resume in LaTeX format
    """
    resume_id = data.get("resumeId")
    job_description = data.get("jobDescription")
    required_skills = data.get("requiredSkills", [])
    
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
        
    # Get the user
    user = await user_service.get_user_by_id(resume.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Here you would implement the actual resume optimization logic
    # For now, we'll return mock data
    latex_code = generate_mock_latex_resume(user.email, required_skills, job_description)
    
    return {
        "latexCode": latex_code
    }

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

# Helper function to generate mock LaTeX resume
def generate_mock_latex_resume(email: str, required_skills: List[str], job_description: str) -> str:
    # Using the same template as in the frontend
    required_skills_section = ""
    if required_skills:
        required_skills_section = f"\\resumeSubItem{{Additional Skills}}{{{', '.join(required_skills)}}}"
    
    return r"""
\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[pdftex]{hyperref}
\usepackage{fancyhdr}
\usepackage{multirow}

\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

%-------------------------
% Custom commands
\newcommand{\resumeItem}[2]{
  \item\small{
    \textbf{#1}{: #2 \vspace{-2pt}}
  }
}

\newcommand{\resumeItemNH}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-1pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-5pt}
}

\newcommand{\resumeSubItem}[2]{\resumeItem{#1}{#2}\vspace{-4pt}}

\renewcommand{\labelitemii}{$\circ$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=*]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeSubHeadingListStartBullets}{\begin{itemize}[leftmargin=*]}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

%-------------------------------------------
%%%%%%  CV STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%


\begin{document}

%----------HEADING-----------------
\begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
  \textbf{\href{http://sourabhbajaj.com/}{\Large John Doe}} & Email : \href{mailto:john.doe@example.com}{john.doe@example.com}\\
  \href{https://linkedin.com/in/johndoe/}{linkedin.com/in/johndoe} & Mobile : +1-123-456-7890 \\
\end{tabular*}

%-----------EDUCATION-----------------
\section{Education}
  \resumeSubHeadingListStart
    \resumeSubheading
      {University of Technology}{New York, NY}
      {Master of Science in Computer Science}{Aug. 2018 -- Dec. 2020}
    \resumeSubheading
      {University of Example}{San Francisco, CA}
      {Bachelor of Engineering in Computer Science}{Aug. 2014 -- May 2018}
  \resumeSubHeadingListEnd

%-----------EXPERIENCE-----------------
\section{Professional Experience}
  \resumeSubHeadingListStart

    \resumeSubheading
      {Senior Software Engineer}{Jan 2021 -- Present}
      {Tech Innovations Inc.}{San Francisco, CA}
      \resumeItemListStart
        \resumeItem{Full Stack Development}
          {Architected and implemented RESTful APIs using Node.js and Express, resulting in a 40\% increase in API throughput.}
        \resumeItem{Performance Optimization}
          {Optimized React.js frontend applications, reducing load time by 60\% and improving user experience significantly.}
        \resumeItem{Team Leadership}
          {Led a team of 5 developers, implementing Agile methodologies that improved project delivery time by 25\%.}
      \resumeItemListEnd

    \resumeSubheading
      {Software Developer}{Jun 2018 -- Dec 2020}
      {Digital Solutions Corp.}{New York, NY}
      \resumeItemListStart
        \resumeItem{Backend Development}
          {Developed microservices using Python and Flask, handling over 1M daily requests.}
        \resumeItem{Database Management}
          {Designed and maintained MongoDB databases, implementing efficient indexing strategies that reduced query times by 35\%.}
        \resumeItem{CI/CD Pipeline}
          {Set up continuous integration and deployment pipelines using Jenkins and Docker, reducing deployment time from days to hours.}
      \resumeItemListEnd
      
  \resumeSubHeadingListEnd

%-----------PROJECTS-----------------
\section{Projects}
  \resumeSubHeadingListStart
    \resumeSubItem{E-commerce Platform}
      {Built a full-stack e-commerce platform using MERN stack (MongoDB, Express.js, React.js, Node.js) with features like product search, cart management, and secure payment processing. Implemented JWT authentication for secure user login.}
    \resumeSubItem{Machine Learning Recommendation System}
      {Developed a content-based recommendation system using Python and scikit-learn that analyzes user behavior to suggest products, resulting in a 15\% increase in user engagement during testing.}
    \resumeSubItem{Mobile Fitness Application}
      {Created a cross-platform mobile application using React Native that tracks workouts, nutrition, and provides personalized fitness plans. Integrated with wearable device APIs for real-time health monitoring.}
  \resumeSubHeadingListEnd

%-----------TECHNICAL SKILLS-----------------
\section{Technical Skills}
  \resumeSubHeadingListStartBullets
    \resumeSubItem{Languages}{JavaScript, TypeScript, Python, Java, SQL, HTML, CSS}
    \resumeSubItem{Frameworks \& Libraries}{React.js, Node.js, Express.js, Django, Flask, TensorFlow, Redux}
    \resumeSubItem{Databases}{MongoDB, PostgreSQL, MySQL, Redis}
    \resumeSubItem{Tools \& Platforms}{Git, Docker, Kubernetes, AWS, Azure, Jenkins, Jira}
    \resumeSubItem{Methodologies}{Agile Development, Test-Driven Development, CI/CD, Microservices Architecture}
  \resumeSubHeadingListEnd

%-----------EXTRACURRICULAR ACTIVITIES-----------------
\section{Extracurricular Activities}
  \resumeSubHeadingListStartBullets
    \resumeSubItem{Technical Speaker}{Regular speaker at local tech meetups and conferences on topics including web development and cloud architecture.}
    \resumeSubItem{Open Source Contributor}{Active contributor to several open-source projects, including React and Express.js.}
    \resumeSubItem{Technical Writer}{Author of technical articles on Medium and Dev.to with over 50,000 cumulative views.}
    \resumeSubItem{Hackathon Participant}{Participated in and won awards at multiple hackathons, developing innovative solutions within 24-48 hours.}
  \resumeSubHeadingListEnd

%-----------HONORS \& AWARDS-----------------
\section{Honors \& Awards}
  \resumeSubHeadingListStartBullets
    \resumeSubItem{Spotlight Award}{Fourth Signal, For introducing new changes and making an impact in UI/UX design and functionality.}
    \resumeSubItem{Judge}{IT Department, St Francis Institute of Technology, for evaluating projects based on innovation and technical proficiency.}
    \resumeSubItem{2nd Place}{Tech fest Colloquium, for the Virtual College Tour Project.}
    \resumeSubItem{3rd Place}{College Blind coding competition.}
  \resumeSubHeadingListEnd

%-----------PUBLICATIONS-----------------
\section{Publications}
  \resumeSubHeadingListStart
    \resumeItemNH{J. Dsouza, S. Ger, L. Wilson, N. Lobo, and N. Rai, ``A Framework for Development of a Virtual Campus Tour," 2023 International Conference on Communication System, Computing and IT Applications (CSCITA), Mumbai, India, 2023, pp. 225-230, doi: 10.1109/CSCITA55725.2023.10104840.}
  \resumeSubHeadingListEnd

%-------------------------------------------
\end{document}"""
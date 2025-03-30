from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not found. Please check your .env file.")

genai.configure(api_key=GOOGLE_API_KEY)

# Set the model name to use (use one from your available models list)
MODEL_NAME = "models/gemini-1.5-pro"

app = FastAPI(title="Interview Chatbot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Use specific frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Origin", "X-Requested-With", "Content-Type", "Accept", "Authorization"],
    expose_headers=["Content-Length"],
    max_age=1728000,  # 20 days
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    resume: Optional[str] = None
    job_description: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str] = None
    
# In-memory storage for chat sessions
interview_sessions = {}

def get_gemini_model():
    """Get the Gemini model instance."""
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        return model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize Gemini model: {str(e)}")

@app.get("/")
async def root():
    """Serve the interview chatbot frontend"""
    return FileResponse("static/index.html")

@app.post("/api/start-interview", response_model=ChatResponse)
async def start_interview(resume: str = Form(...), job_description: str = Form(...)):
    """Start a new interview session with resume and job description"""
    try:
        model = get_gemini_model()
        
        # Create a new session ID
        session_id = str(len(interview_sessions) + 1)
        
        # Create the system prompt
        system_prompt = f"""
        You are an AI-powered interview assistant. Your task is to conduct a professional job interview.

        RESUME:
        {resume}

        JOB DESCRIPTION:
        {job_description}

        GUIDELINES:
        1. Ask one question at a time related to the candidate's experience and the job requirements.
        2. Analyze the candidate's answers and ask follow-up questions that explore their skills, experience, and fit.
        3. Start with general questions and progressively move to more specific technical questions.
        4. Adapt your questions based on the candidate's previous answers.
        5. Be professional and encouraging.
        6. Don't overwhelm the candidate with extremely complex questions right away.
        7. Focus on evaluating the match between the candidate's skills and the job requirements.
        8. After 5-8 questions, start wrapping up the interview.

        Begin the interview with a brief introduction and your first question.
        """
        
        # Initialize chat history
        interview_sessions[session_id] = {
            "resume": resume,
            "job_description": job_description,
            "chat_history": []
        }
        
        # Get the initial message from Gemini
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        response = model.generate_content(
            system_prompt,
            generation_config=generation_config
        )
        
        # Store the response in our session
        interview_sessions[session_id]["chat_history"] = [
            {"role": "user", "content": system_prompt},
            {"role": "model", "content": response.text}
        ]
        
        return {"response": response.text, "session_id": session_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting interview: {str(e)}")

@app.post("/api/chat/{session_id}", response_model=ChatResponse)
async def chat(session_id: str, request: ChatRequest):
    """Continue a chat conversation in an existing session"""
    if session_id not in interview_sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")
    
    try:
        model = get_gemini_model()
        
        # Get the current session
        session = interview_sessions[session_id]
        
        # Get resume and job description context
        resume = session["resume"]
        job_description = session["job_description"]
        
        # Update with the new message
        user_message = request.messages[-1]
        session["chat_history"].append({"role": "user", "content": user_message.content})
        
        # Create context for this request
        context = f"""
        Based on this RESUME: {resume}
        
        And this JOB DESCRIPTION: {job_description}
        
        Previous conversation:
        """
        
        # Add previous conversation
        for msg in session["chat_history"][:-1]:
            role = "Interviewer" if msg["role"] == "model" else "Candidate"
            context += f"\n{role}: {msg['content']}"
        
        # Add the current question
        context += f"\nCandidate: {user_message.content}\n\nAs the interviewer, respond with your next question or comment:"
        
        # Generation config
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        # Send to Gemini
        response = model.generate_content(
            context,
            generation_config=generation_config
        )
        
        # Store the response
        session["chat_history"].append({"role": "model", "content": response.text})
        
        return {"response": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
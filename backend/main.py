from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from dotenv import load_dotenv
from resume_parser import extract_text



# Load API Key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

# ✅ Add CORS Middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from frontend (http://localhost:3000)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_resume_improvement(resume_text, job_description):
    """Generates an optimized resume using Google Gemini API."""
    
    prompt = f"""
    You are an expert resume optimizer for Applicant Tracking Systems (ATS).

    Given the following resume:
    {resume_text}

    And the following job description:
    {job_description}

    - Extract **key skills and keywords** from the job description.
    - Compare with the resume and identify **missing skills or keywords**.
    - Suggest improvements to make the resume **more aligned with the job description**.
    - Rewrite the resume in a way that improves **ATS compatibility** while maintaining clarity.

    Format the response as:
    1. **Extracted Key Skills**
    2. **Matched Skills in Resume**
    3. **Missing Skills & Suggested Additions**
    4. **Optimized Resume Output**
    """

    model = genai.GenerativeModel("gemini-1.5-flash")  # Use Gemini-2.0 if available
    response = model.generate_content(prompt)

    return response.text

@app.post("/upload")
async def process_resume(resume: UploadFile, jobDesc: str = Form(...)):
    """Handles resume upload and sends data to Gemini API for optimization."""
    
    if resume.filename.endswith(".pdf") or resume.filename.endswith(".docx"):
        resume_text = extract_text(resume)
    else:
        return {"error": "Invalid file format. Only PDF and DOCX allowed."}

    optimized_resume = generate_resume_improvement(resume_text, jobDesc)
    return {"highlighted_resume": optimized_resume}

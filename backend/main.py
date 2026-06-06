import os
import fitz
import json
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Resume JD Analyzer API", redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"), timeout=30.0)

SYSTEM_PROMPT = """You are an expert recruiter. Compare the resume against the job description.
Respond ONLY with a valid JSON object with these exact keys:
{"match_score": integer 0-100, "summary": "string", "strengths": ["list"], "missing_skills": ["list"], "suggestions": ["list"], "keyword_matches": ["list"]}
No markdown, no backticks, just raw JSON."""

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "ok", "message": "Resume JD Analyzer API is running"}

@app.post("/analyze")
async def analyze(resume: UploadFile = File(...), jd: str = Form(...)):
    if not jd.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")
    pdf_bytes = await resume.read()
    if len(pdf_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded PDF is empty.")
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        resume_text = ""
        for page in doc:
            resume_text += page.get_text()
        doc.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read PDF: {str(e)}")
    if not resume_text.strip():
        raise HTTPException(status_code=422, detail="No readable text found in PDF.")
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"RESUME:\n{resume_text[:6000]}\n\nJOB DESCRIPTION:\n{jd[:3000]}"}
            ],
            temperature=0.3,
            max_tokens=1000,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Groq API error: {str(e)}")
    try:
        result = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI returned malformed JSON.")
    return result

import json
import os

import fitz
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Resume JD Analyzer API", redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """You are an expert technical recruiter and career coach.
Your job is to compare a candidate's resume against a job description and produce a structured analysis.
You must respond with ONLY a raw JSON object, no markdown, no backticks, no explanation.
The JSON must have exactly these keys:
The JSON must have exactly these keys:
{
  "match_score": <integer 0-100, overall % match>,
  "summary": "<2-3 sentence plain English summary of the candidate's fit>",
  "strengths": ["<strength 1>", "<strength 2>", ...],
  "missing_skills": ["<skill or requirement missing from resume>", ...],
  "suggestions": ["<actionable improvement suggestion>", ...],
  "keyword_matches": ["<keyword found in both resume and JD>", ...]
}
Rules:
- match_score must be an integer between 0 and 100
- strengths: list 3-5 items
- missing_skills: list all genuinely missing requirements, empty list [] if none
- suggestions: list 3-5 concrete specific improvement tips
- keyword_matches: list actual keywords/technologies that appear in both
- Be honest and objective, do not inflate the score"""


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    try:
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())
        text = "\n".join(part for part in text_parts if part)
        if not text.strip():
            raise ValueError("No readable text found in the PDF. Make sure it is not a scanned image-only PDF.")
        return text.strip()
    finally:
        doc.close()


def build_user_prompt(resume_text: str, jd_text: str) -> str:
    return f"""=== RESUME ===
{resume_text[:6000]}

=== JOB DESCRIPTION ===
{jd_text[:3000]}

Analyze the resume against the job description and return the JSON object as specified."""


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "message": "Resume JD Analyzer API is running"}


@app.post("/analyze")
async def analyze(resume: UploadFile = File(...), jd: str = Form(...)):
    client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

    if resume.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    if not jd.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    pdf_bytes = await resume.read()
    if len(pdf_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded PDF is empty.")

    try:
        resume_text = extract_text_from_pdf(pdf_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to read PDF: {str(exc)}") from exc

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(resume_text, jd)},
            ],
            temperature=0.3,
            max_tokens=1000,
        )
        content = response.choices[0].message.content
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {str(exc)}") from exc

    try:
        result = json.loads(content)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail="AI returned malformed JSON. Please try again.") from exc

    required_keys = {"match_score", "summary", "strengths", "missing_skills", "suggestions", "keyword_matches"}
    if not required_keys.issubset(result.keys()):
        raise HTTPException(status_code=500, detail="AI response missing required fields.")

    return result

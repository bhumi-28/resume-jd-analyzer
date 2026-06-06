# Resume JD Analyzer

Resume JD Analyzer compares a candidate's PDF resume against a job description and returns a structured match score, strengths, missing skills, and improvement suggestions.

## Live Demo

- Frontend: https://your-app.vercel.app
- Backend API: https://your-api.onrender.com

## Tech Stack

- React + Vite
- FastAPI + PyMuPDF
- OpenAI GPT-4o-mini
- Render
- Vercel

## Local Development

### Backend

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

### Backend

- OPENAI_API_KEY

### Frontend

- VITE_API_URL


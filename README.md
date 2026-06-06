# Resume JD Analyzer

A full-stack AI-powered web app that analyzes how well a resume matches
a job description — giving a match score, skill gaps, strengths, and
actionable suggestions.

## 🔗 Live Demo
- **App:** https://resume-jd-analyzer-chi.vercel.app
- **API:** https://resume-jd-analyzer-mvuw.onrender.com/health

## ✨ Features
- Upload any PDF resume and paste a job description
- AI returns a match score (0-100%) with color-coded ring
- Highlights strengths, missing skills, keyword matches
- Gives 5 concrete suggestions to improve your resume
- Fully responsive UI

## 🏗️ Architecture
User → React Frontend (Vercel) → Vercel Proxy → FastAPI Backend (Render) → Groq LLaMA 3.1 API

## 🛠️ Tech Stack
| Area | Technologies |
|------|--------------|
| Frontend | React 18, Vite, Axios, CSS |
| Backend | FastAPI, PyMuPDF, Python 3.11 |
| AI Model | Groq LLaMA 3.1 (llama-3.1-8b-instant) |
| Deployment | Vercel (frontend), Render (backend) |
| Monitoring | UptimeRobot |

## 📁 Repository Structure
resume-jd-analyzer/
  backend/
    main.py
    requirements.txt
    Procfile
  frontend/
    src/
      components/
      App.jsx
      main.jsx
    package.json
    vite.config.js
    vercel.json

## 🚀 Local Setup
### Backend
cd backend
python3.11 -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Create .env with GROQ_API_KEY=your_key
uvicorn main:app --reload --port 8000

### Frontend
cd frontend
npm install
# Create .env with VITE_API_URL=http://localhost:8000
npm run dev

## 📡 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| POST | /analyze | Analyze resume vs JD |

## 📄 License
MIT


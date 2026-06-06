import { useState } from 'react'
import axios from 'axios'
import FileUpload from './components/FileUpload'
import JDInput from './components/JDInput'
import ResultCard from './components/ResultCard'
import Spinner from './components/Spinner'

const API_URL = typeof window !== 'undefined' && window.location.hostname !== 'localhost'
  ? '/api'
  : (import.meta.env.VITE_API_URL || 'http://localhost:8000')

export default function App() {
  const [resumeFile, setResumeFile] = useState(null)
  const [jdText, setJdText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAnalyze = async () => {
    if (!resumeFile) {
      setError('Please upload a PDF resume.')
      return
    }

    if (!jdText.trim()) {
      setError('Please paste a job description.')
      return
    }

    setError('')
    setResult(null)
    setLoading(true)

    try {
      const formData = new FormData()
      formData.append('resume', resumeFile)
      formData.append('jd', jdText)

      const response = await axios.post(`${API_URL}/analyze`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 60000,
      })

      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setResumeFile(null)
    setJdText('')
    setResult(null)
    setError('')
    setLoading(false)
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Resume JD Analyzer</h1>
        <p className="subtitle">Find out how well your resume matches a job description — powered by AI</p>
      </header>

      <main className="main">
        {!result ? (
          <div className="form-container">
            <FileUpload file={resumeFile} onFileChange={setResumeFile} />
            <JDInput value={jdText} onChange={setJdText} />

            {error ? <div className="error-banner">{error}</div> : null}

            <button
              type="button"
              className="analyze-btn"
              onClick={handleAnalyze}
              disabled={loading}
            >
              {loading ? 'Analyzing…' : 'Analyze Resume'}
            </button>

            {loading ? <Spinner /> : null}
          </div>
        ) : (
          <div className="form-container">
            <ResultCard result={result} />
            <button type="button" className="reset-btn" onClick={handleReset}>
              ← Analyze Another Resume
            </button>
          </div>
        )}
      </main>

      <footer className="footer">Built with FastAPI · React · OpenAI GPT-4o-mini</footer>
    </div>
  )
}

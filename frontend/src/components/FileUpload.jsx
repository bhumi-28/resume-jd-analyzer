import { useRef } from 'react'

export default function FileUpload({ file, onFileChange }) {
  const inputRef = useRef(null)

  const handleDrop = (e) => {
    e.preventDefault()
    const droppedFile = e.dataTransfer.files?.[0]

    if (droppedFile?.type === 'application/pdf') {
      onFileChange(droppedFile)
    }
  }

  const handleClick = () => {
    inputRef.current?.click()
  }

  const handleInputChange = (e) => {
    const chosenFile = e.target.files?.[0]

    if (chosenFile) {
      onFileChange(chosenFile)
    }

    e.target.value = ''
  }

  return (
    <div className="section">
      <label className="section-label">📄 Upload Resume (PDF)</label>
      <div
        className={`drop-zone ${file ? 'drop-zone--active' : ''}`}
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        onClick={handleClick}
        role="button"
        tabIndex={0}
      >
        {file ? (
          <span className="file-name">✅ {file.name}</span>
        ) : (
          <span className="drop-hint">
            Drag & drop your PDF here, or <u>click to browse</u>
          </span>
        )}
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          hidden
          onChange={handleInputChange}
        />
      </div>
      {file && (
        <button
          type="button"
          className="clear-btn"
          onClick={(e) => {
            e.stopPropagation()
            onFileChange(null)
          }}
        >
          Remove file
        </button>
      )}
    </div>
  )
}

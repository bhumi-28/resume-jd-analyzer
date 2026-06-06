export default function JDInput({ value, onChange }) {
  return (
    <div className="section">
      <label className="section-label">
        📋 Job Description
        <span className="char-count">{value.length} chars</span>
      </label>
      <textarea
        className="jd-textarea"
        placeholder="Paste the full job description here..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={10}
      />
    </div>
  )
}

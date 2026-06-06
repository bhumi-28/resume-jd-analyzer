function ResultSection({ emoji, title, items = [], itemClass, emptyMessage }) {
  return (
    <section className="result-section">
      <h3 className="result-section-title">{emoji} {title}</h3>
      {items.length ? (
        <div className="tags-row">
          {items.map((item, index) => (
            <span key={`${title}-${index}`} className={`tag ${itemClass}`}>
              {item}
            </span>
          ))}
        </div>
      ) : (
        <p className="empty-msg">{emptyMessage}</p>
      )}
    </section>
  )
}

export default function ResultCard({ result }) {
  const scoreColor =
    result.match_score >= 75
      ? '#22c55e'
      : result.match_score >= 50
        ? '#f59e0b'
        : '#ef4444'

  return (
    <article className="result-card">
      <section className="score-section">
        <div className="score-ring" style={{ '--score-color': scoreColor }}>
          <span className="score-number" style={{ color: scoreColor }}>
            {result.match_score}%
          </span>
          <span className="score-label">Match</span>
        </div>
        <p className="summary-text">{result.summary}</p>
      </section>

      <ResultSection
        emoji="✅"
        title="Strengths"
        items={result.strengths}
        itemClass="tag--green"
        emptyMessage="No major strengths listed."
      />

      <ResultSection
        emoji="⚠️"
        title="Missing Skills / Gaps"
        items={result.missing_skills}
        itemClass="tag--red"
        emptyMessage="No major gaps found!"
      />

      <ResultSection
        emoji="🔑"
        title="Keyword Matches"
        items={result.keyword_matches}
        itemClass="tag--blue"
        emptyMessage="No keyword matches found."
      />

      <section className="result-section">
        <h3 className="result-section-title">💡 Suggestions to Improve</h3>
        <ol className="suggestions-list">
          {result.suggestions.map((item, index) => (
            <li key={`suggestion-${index}`}>{item}</li>
          ))}
        </ol>
      </section>
    </article>
  )
}

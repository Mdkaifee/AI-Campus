export default function SourceLinks({ sources }) {
  if (!sources?.length) return null

  return (
    <div className="source-links">
      <p className="source-links__label">Sources</p>
      <ul>
        {sources.map((source) => (
          <li key={`${source.title}-${source.url}`}>
            {source.url ? (
              <a href={source.url} target="_blank" rel="noreferrer">
                {source.title}
              </a>
            ) : (
              <span>{source.title}</span>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}

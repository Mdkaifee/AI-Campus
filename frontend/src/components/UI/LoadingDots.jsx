export default function LoadingDots({ label = 'Thinking' }) {
  return (
    <div className="loading-dots" aria-live="polite" aria-label={label}>
      <span />
      <span />
      <span />
    </div>
  )
}

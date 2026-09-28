export default function ErrorBanner({ message, onDismiss }) {
  if (!message) return null

  return (
    <div className="error-banner" role="alert">
      <p>{message}</p>
      {onDismiss ? (
        <button type="button" className="error-banner__close" onClick={onDismiss}>
          Dismiss
        </button>
      ) : null}
    </div>
  )
}

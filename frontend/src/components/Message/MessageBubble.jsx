import { useState } from 'react'
import { Sparkles, User, Copy, Check } from 'lucide-react'
import LocationCard from './LocationCard.jsx'
import SourceLinks from './SourceLinks.jsx'

function renderContent(content) {
  const lines = content.split('\n')
  return lines.map((line, index) => {
    const bullet = line.match(/^\s*[•*-]\s+(.*)/)
    if (bullet) {
      return (
        <li key={index} className="message__bullet">
          {bullet[1]}
        </li>
      )
    }
    if (!line.trim()) {
      return <br key={index} />
    }
    return <p key={index}>{line}</p>
  })
}

export default function MessageBubble({ message, isStreaming = false }) {
  const isUser = message.role === 'user'
  const hasBullets = message.content?.includes('\n') && /[•*-]\s+/.test(message.content)
  const [copied, setCopied] = useState(false)

  function copyText() {
    if (message.content) {
      navigator.clipboard?.writeText(message.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <article className={`message ${isUser ? 'message--user' : 'message--assistant'}`}>
      <div className="message__avatar" aria-hidden="true">
        {isUser ? (
          <User size={18} strokeWidth={2.2} />
        ) : (
          <Sparkles size={18} strokeWidth={2.2} />
        )}
      </div>
      <div className="message__body">
        <div className="message__sender-row">
          <span className="message__sender-name">{isUser ? 'You' : 'DAVIET Campus AI'}</span>
          {!isUser && !isStreaming ? (
            <button
              type="button"
              className="message__copy-btn"
              onClick={copyText}
              title="Copy response"
              aria-label="Copy response"
            >
              {copied ? (
                <>
                  <Check size={12} strokeWidth={2.5} />
                  <span>Copied</span>
                </>
              ) : (
                <>
                  <Copy size={12} strokeWidth={2.2} />
                  <span>Copy</span>
                </>
              )}
            </button>
          ) : null}
        </div>

        {/* Content with optional blinking cursor while streaming */}
        {hasBullets
          ? <div className="message__text">
              {renderContent(message.content)}
              {isStreaming && <span className="message__cursor" aria-hidden="true" />}
            </div>
          : <p>
              {message.content}
              {isStreaming && <span className="message__cursor" aria-hidden="true" />}
            </p>
        }

        {!isUser && message.location ? <LocationCard location={message.location} /> : null}

        {/* Only show sources once streaming is complete */}
        {!isUser && !isStreaming ? <SourceLinks sources={message.sources} /> : null}
      </div>
    </article>
  )
}

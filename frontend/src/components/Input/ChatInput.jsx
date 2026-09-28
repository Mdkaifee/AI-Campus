import { useEffect, useRef, useState } from 'react'
import { Paperclip, Mic, Send, Sparkles } from 'lucide-react'

export default function ChatInput({ onSend, disabled }) {
  const [value, setValue] = useState('')
  const textareaRef = useRef(null)

  useEffect(() => {
    const el = textareaRef.current
    if (el) {
      el.style.height = 'auto'
      el.style.height = `${Math.min(el.scrollHeight, 140)}px`
    }
  }, [value])

  function submit(event) {
    event?.preventDefault?.()
    if (!value.trim() || disabled) return
    onSend(value)
    setValue('')
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }
  }

  function onKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      submit(event)
    }
  }

  return (
    <footer className="composer-container">
      <form className="composer-pill-card" onSubmit={submit}>
        {/* Attachment Icon Button */}
        <button
          type="button"
          className="composer-icon-action"
          aria-label="Attach file or document"
          title="Attach document (coming soon)"
        >
          <Paperclip size={19} strokeWidth={2} />
        </button>

        {/* Input Textarea */}
        <textarea
          ref={textareaRef}
          id="chat-input"
          rows={1}
          value={value}
          disabled={disabled}
          placeholder="Ask anything about DAVIET campus, library, fees, hostels, or locations..."
          onChange={(event) => setValue(event.target.value)}
          onKeyDown={onKeyDown}
        />

        {/* Voice Input Button */}
        <button
          type="button"
          className="composer-icon-action"
          aria-label="Voice input"
          title="Voice input"
        >
          <Mic size={19} strokeWidth={2} />
        </button>

        {/* Gradient Send Button */}
        <button
          type="submit"
          className="composer-submit-circle"
          disabled={disabled || !value.trim()}
          aria-label="Send message"
          title="Send"
        >
          <Send size={16} strokeWidth={2.4} />
        </button>
      </form>

      {/* Footer Branding Bar */}
      <div className="composer-subfooter">
        <div className="subfooter-left">
          <Sparkles size={14} className="subfooter-sparkle" />
          <span className="subfooter-brand">DAVIET AI</span>
          <span className="subfooter-bullet">•</span>
          <span className="subfooter-tagline">Always here to help</span>
        </div>
        <div className="subfooter-right">
          <span>Learn • Explore • Grow 🌱</span>
        </div>
      </div>
    </footer>
  )
}

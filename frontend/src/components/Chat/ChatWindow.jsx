import { useEffect, useRef } from 'react'
import MessageBubble from '../Message/MessageBubble.jsx'
import LoadingDots from '../UI/LoadingDots.jsx'
import EmptyState from './EmptyState.jsx'

export default function ChatWindow({ messages, loading, onSelectPrompt }) {
  const endRef = useRef(null)

  // True when the assistant bubble is already streaming (last msg is assistant)
  const lastMsg = messages[messages.length - 1]
  const isStreaming = loading && lastMsg?.role === 'assistant'

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages, loading])

  if (!messages.length && !loading) {
    return <EmptyState onSelectPrompt={onSelectPrompt} />
  }

  return (
    <div className="chat-window">
      {messages.map((message, index) => {
        // Mark last assistant message as streaming while response is in flight
        const isLastAssistant =
          index === messages.length - 1 && message.role === 'assistant'
        return (
          <MessageBubble
            key={`${message.role}-${index}`}
            message={message}
            isStreaming={isLastAssistant && isStreaming}
          />
        )
      })}
      {/* Show LoadingDots only while waiting for the FIRST token */}
      {loading && !isStreaming ? (
        <div className="message message--assistant">
          <div className="message__avatar" aria-hidden="true">
            AI
          </div>
          <div className="message__body">
            <LoadingDots />
          </div>
        </div>
      ) : null}
      <div ref={endRef} />
    </div>
  )
}

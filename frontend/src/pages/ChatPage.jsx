import { useState, useEffect } from 'react'
import ChatHeader from '../components/Chat/ChatHeader.jsx'
import ChatWindow from '../components/Chat/ChatWindow.jsx'
import ChatInput from '../components/Input/ChatInput.jsx'
import SessionSidebar from '../components/Sidebar/SessionSidebar.jsx'
import ErrorBanner from '../components/UI/ErrorBanner.jsx'
import { useChat } from '../hooks/useChat.js'

export default function ChatPage({ onBackToHome, initialPrompt, theme, onToggleTheme }) {
  const chat = useChat()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  // If launched with a prompt from landing page, send it automatically
  useEffect(() => {
    if (initialPrompt && chat.messages.length === 0 && !chat.loading) {
      chat.send(initialPrompt)
    }
  }, [initialPrompt])

  function handleNewChat() {
    chat.startNewChat()
    setSidebarOpen(false)
  }

  return (
    <div className="app-shell">
      <SessionSidebar
        sessions={chat.sessions}
        currentSessionId={chat.sessionId}
        loading={chat.sessionsLoading}
        onSelect={chat.loadSession}
        onNewChat={handleNewChat}
        onRemove={chat.removeSession}
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />
      {sidebarOpen ? <button type="button" className="backdrop" aria-label="Close history" onClick={() => setSidebarOpen(false)} /> : null}
      <section className="app-main">
        <ChatHeader
          theme={theme}
          onToggleTheme={onToggleTheme}
          onToggleSidebar={() => setSidebarOpen(true)}
          onNewChat={handleNewChat}
          onBackToHome={onBackToHome}
        />
        <ErrorBanner message={chat.error} onDismiss={chat.clearError} />
        <ChatWindow messages={chat.messages} loading={chat.loading} onSelectPrompt={chat.send} />
        <ChatInput onSend={chat.send} disabled={chat.loading} />
      </section>
    </div>
  )
}

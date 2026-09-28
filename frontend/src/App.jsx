import { useState, useEffect } from 'react'
import LandingPage from './pages/LandingPage.jsx'
import ChatPage from './pages/ChatPage.jsx'
import AuthModal from './components/Auth/AuthModal.jsx'
import { AuthProvider } from './context/AuthContext.jsx'

function MainContent() {
  const [activeView, setActiveView] = useState('landing') // 'landing' | 'chat'
  const [initialPrompt, setInitialPrompt] = useState('')
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('daviet_theme') || 'light'
  })

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('daviet_theme', theme)
  }, [theme])

  function toggleTheme() {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'))
  }

  function handleOpenChat(prompt = '') {
    setInitialPrompt(prompt)
    setActiveView('chat')
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  function handleBackToHome() {
    setActiveView('landing')
    setInitialPrompt('')
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <>
      <AuthModal />
      {activeView === 'chat' ? (
        <ChatPage
          onBackToHome={handleBackToHome}
          initialPrompt={initialPrompt}
          theme={theme}
          onToggleTheme={toggleTheme}
        />
      ) : (
        <LandingPage
          onOpenChat={handleOpenChat}
          theme={theme}
          onToggleTheme={toggleTheme}
        />
      )}
    </>
  )
}

function App() {
  return (
    <AuthProvider>
      <MainContent />
    </AuthProvider>
  )
}

export default App

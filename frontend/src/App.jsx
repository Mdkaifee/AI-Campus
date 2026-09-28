import { useState, useEffect, useCallback } from 'react'
import LandingPage from './pages/LandingPage.jsx'
import ChatPage from './pages/ChatPage.jsx'
import AuthModal from './components/Auth/AuthModal.jsx'
import { AuthProvider, useAuth } from './context/AuthContext.jsx'

function MainRouter() {
  const { user, openAuthModal } = useAuth()
  const [activeRoute, setActiveRoute] = useState(() => {
    const path = window.location.pathname.toLowerCase().replace(/\/$/, '')
    if (path === '/guest' || path === '/chat') return 'chat'
    return 'landing'
  })
  const [isGuestExplicit, setIsGuestExplicit] = useState(() => {
    const path = window.location.pathname.toLowerCase().replace(/\/$/, '')
    return path === '/guest'
  })
  const [initialPrompt, setInitialPrompt] = useState('')
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('daviet_theme') || 'light'
  })

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('daviet_theme', theme)
  }, [theme])

  // Handle direct navigation or back/forward buttons
  useEffect(() => {
    function handleLocationChange() {
      const path = window.location.pathname.toLowerCase().replace(/\/$/, '')
      if (path === '/guest') {
        setActiveRoute('chat')
        setIsGuestExplicit(true)
      } else if (path === '/chat') {
        setActiveRoute('chat')
        setIsGuestExplicit(false)
      } else if (path === '/login') {
        setActiveRoute('landing')
        openAuthModal('login')
      } else if (path === '/signup') {
        setActiveRoute('landing')
        openAuthModal('signup')
      } else {
        setActiveRoute('landing')
        setIsGuestExplicit(false)
      }
    }

    // Initial check on mount
    const path = window.location.pathname.toLowerCase().replace(/\/$/, '')
    if (path === '/login') {
      openAuthModal('login')
    } else if (path === '/signup') {
      openAuthModal('signup')
    }

    window.addEventListener('popstate', handleLocationChange)
    return () => window.removeEventListener('popstate', handleLocationChange)
  }, [openAuthModal])

  function toggleTheme() {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'))
  }

  const navigateTo = useCallback((path, state = {}) => {
    window.history.pushState(null, '', path)
    const cleanPath = path.toLowerCase().replace(/\/$/, '')
    if (cleanPath === '/guest') {
      setIsGuestExplicit(true)
      setActiveRoute('chat')
    } else if (cleanPath === '/chat') {
      setIsGuestExplicit(false)
      setActiveRoute('chat')
    } else {
      setIsGuestExplicit(false)
      setActiveRoute('landing')
    }
    if (state.prompt) {
      setInitialPrompt(state.prompt)
    }
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, [])

  function handleOpenChat(prompt = '', forceGuest = false) {
    const targetPath = (forceGuest || !user) ? '/guest' : '/chat'
    navigateTo(targetPath, { prompt })
  }

  function handleBackToHome() {
    navigateTo('/')
    setInitialPrompt('')
  }

  return (
    <>
      <AuthModal />
      {activeRoute === 'chat' ? (
        <ChatPage
          onBackToHome={handleBackToHome}
          initialPrompt={initialPrompt}
          theme={theme}
          onToggleTheme={toggleTheme}
          isGuestRoute={isGuestExplicit || !user}
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
      <MainRouter />
    </AuthProvider>
  )
}

export default App

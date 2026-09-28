import { useState, useEffect, useCallback } from 'react'
import LandingPage from './pages/LandingPage.jsx'
import ChatPage from './pages/ChatPage.jsx'
import AuthModal from './components/Auth/AuthModal.jsx'
import { AuthProvider, useAuth } from './context/AuthContext.jsx'

function getScheduledTheme() {
  const hours = new Date().getHours()
  // Dark mode turns ON after 6:00 PM (18:00) and turns OFF after 5:00 AM (05:00)
  if (hours >= 18 || hours < 5) {
    return 'dark'
  }
  return 'light'
}

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

  const [manualOverride, setManualOverride] = useState(() => {
    return sessionStorage.getItem('daviet_theme_manual') === 'true'
  })

  const [theme, setTheme] = useState(() => {
    const isManual = sessionStorage.getItem('daviet_theme_manual') === 'true'
    if (isManual) {
      return localStorage.getItem('daviet_theme') || getScheduledTheme()
    }
    return getScheduledTheme()
  })

  // Synchronize document attribute whenever theme changes
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('daviet_theme', theme)
  }, [theme])

  // Periodic and visibility-based auto theme check (6 PM - 5 AM)
  useEffect(() => {
    function checkSchedule() {
      if (!manualOverride) {
        const scheduled = getScheduledTheme()
        setTheme((current) => (current !== scheduled ? scheduled : current))
      }
    }

    checkSchedule()
    const timer = setInterval(checkSchedule, 10000) // check every 10s
    const handleVisibility = () => {
      if (document.visibilityState === 'visible') {
        checkSchedule()
      }
    }
    document.addEventListener('visibilitychange', handleVisibility)

    return () => {
      clearInterval(timer)
      document.removeEventListener('visibilitychange', handleVisibility)
    }
  }, [manualOverride])

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
    setManualOverride(true)
    sessionStorage.setItem('daviet_theme_manual', 'true')
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

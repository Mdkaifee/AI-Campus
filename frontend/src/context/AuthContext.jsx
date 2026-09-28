import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import {
  authGetMe,
  authLogin,
  authSignUp,
  getAuthToken,
  setAuthToken,
  removeAuthToken,
} from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(() => getAuthToken())
  const [loading, setLoading] = useState(true)
  const [authModalOpen, setAuthModalOpen] = useState(false)
  const [authModalMode, setAuthModalMode] = useState('login') // 'login' | 'signup'

  // Initialize and verify session on load
  useEffect(() => {
    let active = true
    const currentToken = getAuthToken()

    if (!currentToken) {
      setLoading(false)
      return
    }

    authGetMe()
      .then((profile) => {
        if (!active) return
        setUser(profile)
      })
      .catch(() => {
        if (!active) return
        // Token invalid or expired
        removeAuthToken()
        setToken('')
        setUser(null)
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => {
      active = false
    }
  }, [])

  const openAuthModal = useCallback((mode = 'login') => {
    setAuthModalMode(mode)
    setAuthModalOpen(true)
  }, [])

  const closeAuthModal = useCallback(() => {
    setAuthModalOpen(false)
  }, [])

  const login = useCallback(async ({ email, password }) => {
    const res = await authLogin({ email, password })
    if (res.token) {
      setAuthToken(res.token)
      setToken(res.token)
      setUser(res.user)
      setAuthModalOpen(false)
      return res
    }
    throw new Error('Authentication failed.')
  }, [])

  const signup = useCallback(async ({ name, email, password }) => {
    const res = await authSignUp({ name, email, password })
    if (res.token) {
      setAuthToken(res.token)
      setToken(res.token)
      setUser(res.user)
      setAuthModalOpen(false)
      return res
    }
    throw new Error('Registration failed.')
  }, [])

  const logout = useCallback(() => {
    removeAuthToken()
    setToken('')
    setUser(null)
  }, [])

  const value = {
    user,
    token,
    loading,
    isAuthenticated: Boolean(user && token),
    authModalOpen,
    authModalMode,
    openAuthModal,
    closeAuthModal,
    setAuthModalMode,
    login,
    signup,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

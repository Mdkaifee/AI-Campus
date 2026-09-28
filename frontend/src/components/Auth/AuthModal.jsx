import { useState, useEffect } from 'react'
import {
  X,
  Mail,
  Lock,
  User,
  Eye,
  EyeOff,
  Sparkles,
  ShieldCheck,
  GraduationCap,
  ArrowRight,
  AlertCircle,
  Loader2,
} from 'lucide-react'
import { useAuth } from '../../context/AuthContext'

export default function AuthModal() {
  const {
    authModalOpen,
    authModalMode,
    closeAuthModal,
    setAuthModalMode,
    login,
    signup,
  } = useAuth()

  const [mode, setMode] = useState(authModalMode)
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    setMode(authModalMode)
    setError('')
  }, [authModalMode, authModalOpen])

  if (!authModalOpen) return null

  function resetForm() {
    setName('')
    setEmail('')
    setPassword('')
    setConfirmPassword('')
    setError('')
  }

  function handleSwitchMode(newMode) {
    setMode(newMode)
    setAuthModalMode(newMode)
    resetForm()
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    const cleanEmail = email.trim().toLowerCase()
    const cleanPassword = password.trim()

    if (!cleanEmail) {
      setError('Please enter your email address.')
      return
    }

    if (!cleanPassword) {
      setError('Please enter your password.')
      return
    }

    if (mode === 'signup') {
      const cleanName = name.trim()
      if (!cleanName || cleanName.length < 2) {
        setError('Please enter your full name (minimum 2 characters).')
        return
      }
      if (cleanPassword.length < 6) {
        setError('Password must be at least 6 characters long.')
        return
      }
      if (cleanPassword !== confirmPassword.trim()) {
        setError('Passwords do not match. Please verify.')
        return
      }

      setSubmitting(true)
      try {
        await signup({ name: cleanName, email: cleanEmail, password: cleanPassword })
        resetForm()
      } catch (err) {
        setError(err.message || 'Registration failed. Please try again.')
      } finally {
        setSubmitting(false)
      }
    } else {
      setSubmitting(true)
      try {
        await login({ email: cleanEmail, password: cleanPassword })
        resetForm()
      } catch (err) {
        setError(err.message || 'Login failed. Please check your email and password.')
      } finally {
        setSubmitting(false)
      }
    }
  }

  return (
    <div className="auth-modal-overlay" onClick={closeAuthModal}>
      <div
        className="auth-modal-card"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        {/* Close Button */}
        <button
          type="button"
          className="auth-modal-close"
          onClick={closeAuthModal}
          aria-label="Close dialog"
        >
          <X size={20} />
        </button>

        {/* Modal Header */}
        <div className="auth-modal-header">
          <div className="auth-brand-badge">
            <GraduationCap size={24} className="auth-brand-icon" />
          </div>
          <h2 className="auth-modal-title">
            {mode === 'signup' ? 'Create Student Account' : 'Sign In to Campus AI'}
          </h2>
          <p className="auth-modal-subtitle">
            DAV Institute of Engineering &amp; Technology • AI Portal
          </p>
        </div>

        {/* Mode Switcher Tabs */}
        <div className="auth-tab-bar">
          <button
            type="button"
            className={`auth-tab-btn ${mode === 'login' ? 'is-active' : ''}`}
            onClick={() => handleSwitchMode('login')}
          >
            Sign In
          </button>
          <button
            type="button"
            className={`auth-tab-btn ${mode === 'signup' ? 'is-active' : ''}`}
            onClick={() => handleSwitchMode('signup')}
          >
            Create Account
          </button>
        </div>

        {/* Privacy Highlight Banner */}
        <div className="auth-privacy-callout">
          <ShieldCheck size={16} className="auth-privacy-icon" />
          <span>Private &amp; Secure: Only you can view your personal chat sessions and queries.</span>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="auth-error-banner">
            <AlertCircle size={16} className="auth-error-icon" />
            <span>{error}</span>
          </div>
        )}

        {/* Form */}
        <form className="auth-form" onSubmit={handleSubmit}>
          {mode === 'signup' && (
            <div className="auth-field-group">
              <label className="auth-field-label" htmlFor="auth-name">
                Full Name
              </label>
              <div className="auth-input-wrap">
                <User size={18} className="auth-input-icon" />
                <input
                  id="auth-name"
                  type="text"
                  className="auth-input"
                  placeholder="e.g. Enter your name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  disabled={submitting}
                  autoComplete="name"
                  required
                />
              </div>
            </div>
          )}

          <div className="auth-field-group">
            <label className="auth-field-label" htmlFor="auth-email">
              Email Address
            </label>
            <div className="auth-input-wrap">
              <Mail size={18} className="auth-input-icon" />
              <input
                id="auth-email"
                type="email"
                className="auth-input"
                placeholder="e.g. student@davietjal.org"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={submitting}
                autoComplete="email"
                required
              />
            </div>
          </div>

          <div className="auth-field-group">
            <label className="auth-field-label" htmlFor="auth-password">
              Password {mode === 'signup' && <span className="auth-label-hint">(min. 6 characters)</span>}
            </label>
            <div className="auth-input-wrap">
              <Lock size={18} className="auth-input-icon" />
              <input
                id="auth-password"
                type={showPassword ? 'text' : 'password'}
                className="auth-input"
                placeholder={mode === 'signup' ? 'Create a secure password' : 'Enter your password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={submitting}
                autoComplete={mode === 'signup' ? 'new-password' : 'current-password'}
                required
              />
              <button
                type="button"
                className="auth-password-toggle"
                onClick={() => setShowPassword((prev) => !prev)}
                aria-label={showPassword ? 'Hide password' : 'Show password'}
              >
                {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
              </button>
            </div>
          </div>

          {mode === 'signup' && (
            <div className="auth-field-group">
              <label className="auth-field-label" htmlFor="auth-confirm-password">
                Confirm Password
              </label>
              <div className="auth-input-wrap">
                <Lock size={18} className="auth-input-icon" />
                <input
                  id="auth-confirm-password"
                  type={showPassword ? 'text' : 'password'}
                  className="auth-input"
                  placeholder="Re-enter your password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  disabled={submitting}
                  autoComplete="new-password"
                  required
                />
              </div>
            </div>
          )}

          <button
            type="submit"
            className="auth-submit-btn"
            disabled={submitting}
          >
            {submitting ? (
              <>
                <Loader2 size={18} className="auth-spinner" />
                <span>{mode === 'signup' ? 'Creating Account…' : 'Signing In…'}</span>
              </>
            ) : (
              <>
                <Sparkles size={17} />
                <span>{mode === 'signup' ? 'Create Student Account' : 'Sign In'}</span>
                <ArrowRight size={17} />
              </>
            )}
          </button>
        </form>

        {/* Footer switch */}
        <div className="auth-modal-footer">
          {mode === 'login' ? (
            <p>
              Don&apos;t have an account yet?{' '}
              <button
                type="button"
                className="auth-link-btn"
                onClick={() => handleSwitchMode('signup')}
              >
                Create an account
              </button>
            </p>
          ) : (
            <p>
              Already have an account?{' '}
              <button
                type="button"
                className="auth-link-btn"
                onClick={() => handleSwitchMode('login')}
              >
                Sign in here
              </button>
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

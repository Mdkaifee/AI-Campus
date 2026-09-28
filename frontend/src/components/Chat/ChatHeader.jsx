import { Menu, Sun, Moon, ArrowLeft, LogIn, LogOut, UserCircle2 } from 'lucide-react'
import { useAuth } from '../../context/AuthContext'

export default function ChatHeader({
  theme,
  onToggleTheme,
  onToggleSidebar,
  onNewChat,
  onBackToHome,
  isGuestRoute,
}) {
  const isDark = theme === 'dark'
  const { user, openAuthModal, logout } = useAuth()

  return (
    <header className="chat-header">
      <div className="chat-header__left">
        {onBackToHome && (
          <button
            type="button"
            className="header-home-btn"
            onClick={onBackToHome}
            aria-label="Back to Campus Portal"
            title="Back to Campus Portal Home"
          >
            <ArrowLeft size={18} strokeWidth={2.2} />
            <span className="header-home-text">Portal Home</span>
          </button>
        )}

        <button
          type="button"
          className="header-drawer-btn"
          onClick={onToggleSidebar}
          aria-label="Toggle chat history"
          title="Toggle History Sidebar"
        >
          <Menu size={20} strokeWidth={2} />
        </button>

        <div className="header-college-info">
          <span className="header-college-tag">DAV Institute of Engineering &amp; Technology, Jalandhar</span>
        </div>
      </div>

      <div className="chat-header__right">
        {user ? (
          <div className="header-user-badge" title={`Signed in as ${user.email}`}>
            <div className="header-user-avatar">
              {user.name ? user.name.charAt(0).toUpperCase() : 'U'}
            </div>
            <span className="header-user-name">{user.name}</span>
            <button
              type="button"
              className="header-user-logout"
              onClick={logout}
              title="Sign Out"
              aria-label="Sign Out"
            >
              <LogOut size={15} />
            </button>
          </div>
        ) : (
          <div className="header-guest-wrap">
            <div className="header-guest-chip" title="You are chatting in isolated Guest Mode. Your chat will not be saved across browsers or tabs.">
              <UserCircle2 size={15} />
              <span>Guest Mode</span>
            </div>
            <button
              type="button"
              className="header-signin-btn"
              onClick={() => openAuthModal('login')}
              title="Sign in to save private chat history"
            >
              <LogIn size={15} />
              <span className="header-signin-text">Sign In</span>
            </button>
          </div>
        )}

        <button
          type="button"
          className="header-theme-btn"
          onClick={onToggleTheme}
          aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
          title={isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
        >
          {isDark ? <Sun size={18} strokeWidth={2.2} /> : <Moon size={18} strokeWidth={2.2} />}
        </button>

        <div className="header-badge-chip">
          <div className="header-badge-emblem">
            <span className="header-emblem-text">DAV</span>
          </div>
          <div className="header-badge-text">
            <span className="header-badge-name">DAV Institute of Engineering &amp; Technology</span>
            <span className="header-badge-loc">Jalandhar, Punjab</span>
          </div>
        </div>
      </div>
    </header>
  )
}

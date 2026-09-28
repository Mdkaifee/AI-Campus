import { useState } from 'react'
import {
  GraduationCap,
  Plus,
  MessageSquare,
  Clock,
  MapPin,
  IndianRupee,
  Building2,
  Home,
  FileText,
  Trash2,
  Settings,
  HelpCircle,
  Sparkles,
  ChevronRight,
} from 'lucide-react'

// Default sample quick-access icons mapping if title matches keywords
function getIconForTitle(title = '') {
  const t = title.toLowerCase()
  if (t.includes('library') || t.includes('time') || t.includes('timing')) return Clock
  if (t.includes('location') || t.includes('tpo') || t.includes('map') || t.includes('office')) return MapPin
  if (t.includes('fee') || t.includes('money') || t.includes('cost') || t.includes('payment')) return IndianRupee
  if (t.includes('department') || t.includes('branch') || t.includes('engineering')) return Building2
  if (t.includes('hostel') || t.includes('room') || t.includes('stay') || t.includes('mess')) return Home
  if (t.includes('admission') || t.includes('form') || t.includes('apply')) return FileText
  return MessageSquare
}

export default function SessionSidebar({
  sessions,
  currentSessionId,
  loading,
  onSelect,
  onNewChat,
  onRemove,
  open,
  onClose,
}) {
  return (
    <aside className={`sidebar ${open ? 'sidebar--open' : ''}`}>
      {/* Brand Header with Graduation Cap */}
      <div className="sidebar__brand-header">
        <div className="sidebar__brand-icon-box">
          <GraduationCap className="sidebar__brand-cap-icon" size={26} strokeWidth={2.2} />
        </div>
        <div className="sidebar__brand-details">
          <h2 className="sidebar__brand-title">DAVIET</h2>
          <span className="sidebar__brand-subtitle">Campus AI</span>
        </div>
      </div>

      {/* New Chat Primary Button */}
      <button type="button" className="sidebar__new-chat-action" onClick={onNewChat}>
        <Plus size={18} strokeWidth={2.5} />
        <span>New Chat</span>
      </button>

      {/* Section Header: Recent Conversations */}
      <div className="sidebar__section-header">
        <div className="sidebar__section-left">
          <Clock size={15} strokeWidth={2.2} className="sidebar__section-clock" />
          <span className="sidebar__section-title">Recent Conversations</span>
        </div>
        <ChevronRight size={15} className="sidebar__section-chevron" />
      </div>

      {/* Session History List */}
      <nav className="sidebar__list" aria-label="Chat history">
        {loading && !sessions.length ? (
          <p className="sidebar__hint">Loading chats…</p>
        ) : null}
        {!loading && !sessions.length ? (
          <div className="sidebar__empty">
            <MessageSquare size={28} strokeWidth={1.5} className="sidebar__empty-icon" />
            <p>No conversations yet. Start a new chat!</p>
          </div>
        ) : null}
        {sessions.map((session) => {
          const ItemIcon = getIconForTitle(session.title)
          const isActive = session.session_id === currentSessionId
          return (
            <div
              key={session.session_id}
              className={`sidebar__item-wrap ${isActive ? 'is-active' : ''}`}
            >
              <button
                type="button"
                className="sidebar__item"
                onClick={() => {
                  onSelect(session.session_id)
                  onClose?.()
                }}
                title={session.title || 'Chat'}
              >
                <div className="sidebar__item-icon-wrapper">
                  <ItemIcon size={16} strokeWidth={2} />
                </div>
                <div className="sidebar__item-text-container">
                  <span className="sidebar__item-text">{session.title || 'Conversation'}</span>
                  <span className="sidebar__item-meta">Active chat</span>
                </div>
                <ChevronRight size={14} className="sidebar__item-arrow" />
              </button>
              {onRemove ? (
                <button
                  type="button"
                  className="sidebar__delete-btn"
                  title="Delete this chat"
                  onClick={(e) => onRemove(session.session_id, e)}
                  aria-label="Delete chat"
                >
                  <Trash2 size={13} strokeWidth={2} />
                </button>
              ) : null}
            </div>
          )
        })}
      </nav>

      {/* Bottom Utility Links */}
      <div className="sidebar__bottom-tools">
        <button type="button" className="sidebar__tool-btn">
          <Settings size={17} strokeWidth={1.9} />
          <span>Settings</span>
        </button>
        <button type="button" className="sidebar__tool-btn">
          <HelpCircle size={17} strokeWidth={1.9} />
          <span>Help &amp; Information</span>
        </button>
      </div>

      {/* Footer Profile / Status Badge */}
      <div className="sidebar__footer">
        <div className="sidebar__status-profile">
          <div className="sidebar__status-dot-pulse" />
          <div className="sidebar__status-meta">
            <span className="sidebar__status-name">DAVIET AI</span>
            <span className="sidebar__status-online">Online</span>
          </div>
        </div>
        <div className="sidebar__footer-spark-glow">
          <Sparkles size={16} strokeWidth={2} />
        </div>
      </div>
    </aside>
  )
}

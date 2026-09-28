const CURRENT_KEY = 'daviet.currentSessionId'
const GUEST_SESSIONS_KEY = 'daviet.guestSessions'
const GUEST_MESSAGES_PREFIX = 'daviet.guestMsgs.'

// Clean up any old localStorage session key to prevent cross-tab or stale guest session leakage
try {
  localStorage.removeItem(CURRENT_KEY)
} catch {
  // ignore
}

export function getStoredSessionId() {
  try {
    return sessionStorage.getItem(CURRENT_KEY)
  } catch {
    return null
  }
}

export function storeSessionId(sessionId) {
  try {
    if (sessionId) {
      sessionStorage.setItem(CURRENT_KEY, sessionId)
    } else {
      sessionStorage.removeItem(CURRENT_KEY)
    }
  } catch {
    // ignore storage failures
  }
}

export function getStoredGuestSessions() {
  try {
    const raw = sessionStorage.getItem(GUEST_SESSIONS_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

export function saveStoredGuestSessions(sessions) {
  try {
    sessionStorage.setItem(GUEST_SESSIONS_KEY, JSON.stringify(sessions || []))
  } catch {
    // ignore
  }
}

export function getStoredGuestMessages(sessionId) {
  try {
    if (!sessionId) return []
    const raw = sessionStorage.getItem(GUEST_MESSAGES_PREFIX + sessionId)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

export function storeGuestMessages(sessionId, messages) {
  try {
    if (!sessionId) return
    sessionStorage.setItem(GUEST_MESSAGES_PREFIX + sessionId, JSON.stringify(messages || []))
  } catch {
    // ignore
  }
}

export function deleteStoredGuestSession(sessionId) {
  try {
    sessionStorage.removeItem(GUEST_MESSAGES_PREFIX + sessionId)
    const current = getStoredGuestSessions()
    const updated = current.filter((s) => s.session_id !== sessionId)
    saveStoredGuestSessions(updated)
  } catch {
    // ignore
  }
}

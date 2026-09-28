const CURRENT_KEY = 'daviet.currentSessionId'

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

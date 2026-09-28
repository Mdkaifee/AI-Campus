const CURRENT_KEY = 'daviet.currentSessionId'

export function getStoredSessionId() {
  try {
    return localStorage.getItem(CURRENT_KEY)
  } catch {
    return null
  }
}

export function storeSessionId(sessionId) {
  try {
    if (sessionId) localStorage.setItem(CURRENT_KEY, sessionId)
    else localStorage.removeItem(CURRENT_KEY)
  } catch {
    // ignore storage failures
  }
}

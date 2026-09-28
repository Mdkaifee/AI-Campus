const API_BASE = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')

const TOKEN_KEY = 'daviet_auth_token'

export function getAuthToken() {
  return localStorage.getItem(TOKEN_KEY) || ''
}

export function setAuthToken(token) {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token)
  } else {
    localStorage.removeItem(TOKEN_KEY)
  }
}

export function removeAuthToken() {
  localStorage.removeItem(TOKEN_KEY)
}

async function request(path, options = {}) {
  let response
  const token = getAuthToken()
  const defaultHeaders = {
    'Content-Type': 'application/json',
  }
  if (token) {
    defaultHeaders['Authorization'] = `Bearer ${token}`
  }

  try {
    response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...(options.headers || {}),
      },
    })
  } catch (err) {
    if (err.name === 'AbortError') {
      throw err
    }
    throw new Error('Something went wrong while communicating with the server. Please try again.')
  }

  if (!response.ok) {
    let detail = 'Something went wrong while processing your request.'
    try {
      const payload = await response.json()
      if (typeof payload?.detail === 'string') {
        detail = payload.detail
      } else if (Array.isArray(payload?.detail) && payload.detail[0]?.msg) {
        detail = payload.detail[0].msg.replace(/^Value error,\s*/i, '')
      }
    } catch {
      // keep generic message
    }
    throw new Error(detail)
  }

  return response.json()
}

// ---------------- Authentication APIs ----------------

export function authSignUp({ name, email, password }) {
  return request('/api/auth/signup', {
    method: 'POST',
    body: JSON.stringify({ name, email, password }),
  })
}

export function authLogin({ email, password }) {
  return request('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
}

export function authGetMe() {
  return request('/api/auth/me')
}

// ---------------- Chat APIs ----------------

export function sendMessage({ message, sessionId }, options = {}) {
  const body = { message }
  if (sessionId) body.session_id = sessionId
  return request('/api/chat', {
    method: 'POST',
    body: JSON.stringify(body),
    ...options,
  })
}

export async function sendMessageStream({ message, sessionId, onMetadata, onToken, onDone }, options = {}) {
  const body = { message }
  if (sessionId) body.session_id = sessionId

  const token = getAuthToken()
  const headers = { 'Content-Type': 'application/json' }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE}/api/chat/stream`, {
    method: 'POST',
    headers: {
      ...headers,
      ...(options.headers || {}),
    },
    body: JSON.stringify(body),
    ...options,
  })

  if (!response.ok) {
    let detail = 'Something went wrong while processing your question. Please try again.'
    try {
      const payload = await response.json()
      if (typeof payload?.detail === 'string') detail = payload.detail
    } catch {
      // keep default
    }
    throw new Error(detail)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    // Normalize \r\n → \n so SSE splitting is consistent regardless of server line endings
    buffer += decoder.decode(value, { stream: true }).replace(/\r\n/g, '\n').replace(/\r/g, '\n')

    // SSE events are separated by a blank line (\n\n)
    const parts = buffer.split('\n\n')
    // Last part may be incomplete — keep it in the buffer
    buffer = parts.pop() ?? ''

    for (const part of parts) {
      for (const line of part.split('\n')) {
        const trimmed = line.trim()
        if (!trimmed.startsWith('data: ')) continue
        try {
          const event = JSON.parse(trimmed.slice(6))
          if (event.type === 'metadata') {
            onMetadata?.(event)
          } else if (event.type === 'token') {
            onToken?.(event.content)
          } else if (event.type === 'done') {
            onDone?.()
          }
        } catch {
          // ignore malformed chunk
        }
      }
    }
  }
}

export function listSessions(options = {}) {
  return request('/api/chat/sessions', options)
}

export function getSession(sessionId, options = {}) {
  return request(`/api/chat/sessions/${encodeURIComponent(sessionId)}`, options)
}

export function deleteSession(sessionId, options = {}) {
  return request(`/api/chat/sessions/${encodeURIComponent(sessionId)}`, {
    method: 'DELETE',
    ...options,
  })
}

export function checkHealth(options = {}) {
  return request('/api/health', options)
}

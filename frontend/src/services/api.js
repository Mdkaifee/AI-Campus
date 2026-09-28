const API_BASE = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')

async function request(path, options = {}) {
  let response
  try {
    response = await fetch(`${API_BASE}${path}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      ...options,
    })
  } catch (err) {
    if (err.name === 'AbortError') {
      throw err
    }
    throw new Error('Something went wrong while processing your question. Please try again.')
  }

  if (!response.ok) {
    let detail = 'Something went wrong while processing your question. Please try again.'
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

  const response = await fetch(`${API_BASE}/api/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
    ...options,
  })

  if (!response.ok) {
    throw new Error('Something went wrong while processing your question. Please try again.')
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
      // Each part may have multiple lines; find the "data: " line
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


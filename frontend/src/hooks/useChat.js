import { useCallback, useEffect, useRef, useState } from 'react'
import { deleteSession, getSession, listSessions, sendMessageStream } from '../services/api'
import { getStoredSessionId, storeSessionId } from '../utils/session'
import { useAuth } from '../context/AuthContext'

export function useChat() {
  const { user, token } = useAuth()
  const [sessionId, setSessionId] = useState(() => getStoredSessionId())
  const [messages, setMessages] = useState([])
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [sessionsLoading, setSessionsLoading] = useState(false)

  // Track active fetch controller to abort stale requests when switching context
  const activeControllerRef = useRef(null)
  // Track target session ID that the UI currently expects
  const activeTargetIdRef = useRef(sessionId)

  const cancelActiveRequest = useCallback(() => {
    if (activeControllerRef.current) {
      activeControllerRef.current.abort()
      activeControllerRef.current = null
    }
  }, [])

  const refreshSessions = useCallback(async () => {
    setSessionsLoading(true)
    try {
      const rows = await listSessions()
      setSessions(rows)
    } catch {
      // History is optional if the database is degraded
    } finally {
      setSessionsLoading(false)
    }
  }, [])

  const loadSession = useCallback(
    async (id) => {
      if (!id) return

      cancelActiveRequest()
      const controller = new AbortController()
      activeControllerRef.current = controller
      activeTargetIdRef.current = id

      setError('')
      setLoading(true)

      try {
        const history = await getSession(id, { signal: controller.signal })

        // Guard against stale response if user navigated away before completion
        if (activeTargetIdRef.current !== id) return

        const nextMessages = []
        for (const turn of history.turns || []) {
          nextMessages.push({ role: 'user', content: turn.user_message })
          nextMessages.push({
            role: 'assistant',
            content: turn.assistant_message,
            sources: turn.sources || [],
            location: turn.location || null,
          })
        }
        setSessionId(id)
        storeSessionId(id)
        setMessages(nextMessages)
      } catch (err) {
        if (err.name === 'AbortError') return
        if (activeTargetIdRef.current === id) {
          setError(err.message || 'Something went wrong while loading this conversation.')
        }
      } finally {
        if (activeTargetIdRef.current === id) {
          setLoading(false)
        }
      }
    },
    [cancelActiveRequest],
  )

  const startNewChat = useCallback(() => {
    cancelActiveRequest()
    activeTargetIdRef.current = null
    setSessionId(null)
    storeSessionId(null)
    setMessages([])
    setError('')
    setLoading(false)
  }, [cancelActiveRequest])

  // When user changes (login / logout / switch account), clear and reload sessions for that user
  useEffect(() => {
    let active = true
    startNewChat()
    setSessionsLoading(true)

    listSessions()
      .then((rows) => {
        if (!active) return
        setSessions(rows)
        if (rows.length > 0) {
          loadSession(rows[0].session_id)
        }
      })
      .catch(() => {
        if (!active) return
        setSessions([])
      })
      .finally(() => {
        if (active) setSessionsLoading(false)
      })

    return () => {
      active = false
    }
  }, [token, user?.email])

  const removeSession = useCallback(
    async (id, event) => {
      event?.stopPropagation?.()
      try {
        await deleteSession(id)
        if (sessionId === id || activeTargetIdRef.current === id) {
          startNewChat()
        }
        setSessions((prev) => prev.filter((s) => s.session_id !== id))
      } catch {
        setError('Failed to delete chat session.')
      }
    },
    [sessionId, startNewChat],
  )

  const send = useCallback(
    async (text) => {
      const trimmed = text.trim()
      if (!trimmed || loading) return

      cancelActiveRequest()
      const controller = new AbortController()
      activeControllerRef.current = controller

      const currentSessionId = sessionId
      // Mark the current target so any in-flight loadSession knows to yield
      activeTargetIdRef.current = currentSessionId

      setError('')
      setMessages((current) => [...current, { role: 'user', content: trimmed }])
      setLoading(true)

      try {
        let streamStarted = false

        await sendMessageStream(
          {
            message: trimmed,
            sessionId: currentSessionId,
            onMetadata: (meta) => {
              const currentTarget = activeTargetIdRef.current
              if (
                currentTarget !== null &&
                currentTarget !== currentSessionId &&
                currentTarget !== meta.session_id
              ) {
                return
              }

              activeTargetIdRef.current = meta.session_id
              setSessionId(meta.session_id)
              storeSessionId(meta.session_id)

              if (!streamStarted) {
                streamStarted = true
                setMessages((current) => [
                  ...current,
                  {
                    role: 'assistant',
                    content: '',
                    sources: meta.sources || [],
                    location: meta.location || null,
                  },
                ])
              }
            },
            onToken: (tokenChunk) => {
              setMessages((current) => {
                if (current.length === 0) return current
                const lastIdx = current.length - 1
                const lastMsg = current[lastIdx]
                if (lastMsg.role !== 'assistant') return current
                const updated = [...current]
                updated[lastIdx] = {
                  ...lastMsg,
                  content: lastMsg.content + tokenChunk,
                }
                return updated
              })
            },
          },
          { signal: controller.signal },
        )

        refreshSessions()
      } catch (err) {
        if (err.name === 'AbortError') return
        setError(err.message || 'Something went wrong while processing your question. Please try again.')
      } finally {
        setLoading(false)
      }
    },
    [cancelActiveRequest, loading, refreshSessions, sessionId],
  )

  return {
    sessionId,
    messages,
    sessions,
    loading,
    error,
    sessionsLoading,
    send,
    startNewChat,
    loadSession,
    removeSession,
    refreshSessions,
    clearError: () => setError(''),
  }
}

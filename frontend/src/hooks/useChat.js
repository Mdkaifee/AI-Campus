import { useCallback, useEffect, useRef, useState } from 'react'
import { deleteSession, getSession, listSessions, sendMessageStream } from '../services/api'
import {
  getStoredSessionId,
  storeSessionId,
  getStoredGuestSessions,
  saveStoredGuestSessions,
  getStoredGuestMessages,
  storeGuestMessages,
  deleteStoredGuestSession,
} from '../utils/session'
import { useAuth } from '../context/AuthContext'

export function useChat() {
  const { user, token } = useAuth()
  const [sessionId, setSessionId] = useState(() => getStoredSessionId())
  const [messages, setMessages] = useState([])
  const [sessions, setSessions] = useState(() => {
    return user ? [] : getStoredGuestSessions()
  })
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
    if (!user) {
      setSessions(getStoredGuestSessions())
      return
    }
    setSessionsLoading(true)
    try {
      const rows = await listSessions()
      setSessions(rows)
    } catch {
      // History is optional if the database is degraded
    } finally {
      setSessionsLoading(false)
    }
  }, [user])

  const loadSession = useCallback(
    async (id) => {
      if (!id) return

      cancelActiveRequest()
      const controller = new AbortController()
      activeControllerRef.current = controller
      activeTargetIdRef.current = id

      setError('')
      setLoading(true)

      // In guest mode, check tab session storage first for instant load
      if (!user) {
        const cached = getStoredGuestMessages(id)
        if (cached && cached.length > 0) {
          setSessionId(id)
          storeSessionId(id)
          setMessages(cached)
          setLoading(false)
          return
        }
      }

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
        if (!user) {
          storeGuestMessages(id, nextMessages)
        }
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
    [cancelActiveRequest, user],
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

    if (!user) {
      // Load tab-scoped guest sessions
      const guestList = getStoredGuestSessions()
      setSessions(guestList)
      setSessionsLoading(false)
      const currentGuestId = getStoredSessionId()
      if (currentGuestId && guestList.some((s) => s.session_id === currentGuestId)) {
        loadSession(currentGuestId)
      }
      return
    }

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
        if (!user) {
          deleteStoredGuestSession(id)
          if (sessionId === id || activeTargetIdRef.current === id) {
            startNewChat()
          }
          setSessions((prev) => prev.filter((s) => s.session_id !== id))
          return
        }

        await deleteSession(id)
        if (sessionId === id || activeTargetIdRef.current === id) {
          startNewChat()
        }
        setSessions((prev) => prev.filter((s) => s.session_id !== id))
      } catch {
        setError('Failed to delete chat session.')
      }
    },
    [sessionId, startNewChat, user],
  )

  const send = useCallback(
    async (text) => {
      const trimmed = text.trim()
      if (!trimmed || loading) return

      cancelActiveRequest()
      const controller = new AbortController()
      activeControllerRef.current = controller

      const currentSessionId = sessionId
      activeTargetIdRef.current = currentSessionId

      setError('')
      const userMessageObj = { role: 'user', content: trimmed }
      setMessages((current) => [...current, userMessageObj])
      setLoading(true)

      try {
        let streamStarted = false
        let finalSessionId = currentSessionId
        let accumulatedAssistant = ''
        let accumulatedSources = []
        let accumulatedLocation = null

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

              finalSessionId = meta.session_id
              activeTargetIdRef.current = meta.session_id
              setSessionId(meta.session_id)
              storeSessionId(meta.session_id)

              accumulatedSources = meta.sources || []
              accumulatedLocation = meta.location || null

              if (!streamStarted) {
                streamStarted = true
                setMessages((current) => [
                  ...current,
                  {
                    role: 'assistant',
                    content: '',
                    sources: accumulatedSources,
                    location: accumulatedLocation,
                  },
                ])
              }

              // Update guest session sidebar list immediately so "hi" shows right away!
              if (!user) {
                setSessions((prev) => {
                  const existingIndex = prev.findIndex((s) => s.session_id === meta.session_id)
                  let updated
                  if (existingIndex >= 0) {
                    updated = [...prev]
                    updated[existingIndex] = {
                      ...updated[existingIndex],
                      updated_at: new Date().toISOString(),
                    }
                  } else {
                    const titleText = trimmed.length > 32 ? trimmed.slice(0, 32) + '…' : trimmed
                    const newEntry = {
                      session_id: meta.session_id,
                      title: titleText,
                      updated_at: new Date().toISOString(),
                      message_count: 1,
                    }
                    updated = [newEntry, ...prev]
                  }
                  saveStoredGuestSessions(updated)
                  return updated
                })
              }
            },
            onToken: (tokenChunk) => {
              accumulatedAssistant += tokenChunk
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

        // Save complete message turn to tab session storage for guest
        if (!user && finalSessionId) {
          setMessages((current) => {
            storeGuestMessages(finalSessionId, current)
            return current
          })
        }

        if (user) {
          refreshSessions()
        }
      } catch (err) {
        if (err.name === 'AbortError') return
        setError(err.message || 'Something went wrong while processing your question. Please try again.')
      } finally {
        setLoading(false)
      }
    },
    [cancelActiveRequest, loading, refreshSessions, sessionId, user],
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

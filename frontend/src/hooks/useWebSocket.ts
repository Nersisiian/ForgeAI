import { useEffect, useRef, useState } from 'react'
import { createProjectSocket } from '../services/websocket'

export function useProjectWebSocket(projectId: string | null) {
  const [messages, setMessages] = useState<any[]>([])
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    if (!projectId) return
    const token = localStorage.getItem('access_token')
    if (!token) return
    const ws = createProjectSocket(projectId, token)
    wsRef.current = ws
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setMessages(prev => [...prev, data])
    }
    return () => ws.close()
  }, [projectId])

  return messages
}
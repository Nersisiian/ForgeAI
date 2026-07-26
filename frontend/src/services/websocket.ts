import { WS_BASE } from '../utils/constants'

export function createProjectSocket(projectId: string, token: string) {
  const ws = new WebSocket(`${WS_BASE}/api/v1/ws/${projectId}?token=${token}`)
  return ws
}
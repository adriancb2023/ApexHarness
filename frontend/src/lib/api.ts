export interface Project {
  id: string
  name: string
  cwd: string
}

export interface Session {
  id: string
  project_id: string
  title: string
  cwd: string
  tokens?: number
  opencode_session_id?: string | null
}

export interface Message {
  role: string
  content: string
  tokens: number
  ts: number
  feature: string
}

export interface Card {
  id: string
  project_id: string
  title: string
  feature: string
  files: string[]
  depends_on: string[]
  status: 'backlog' | 'progreso' | 'pruebas' | 'listo'
  blocked: boolean
}

export interface Debate {
  id: string
  project_id: string
  turns: { from: string; to: string; content: string }[]
  pending: { from: string; content: string } | null
  turn_count: number
  status: string
}

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const r = await fetch(path, init)
  if (!r.ok) throw new Error(`${init?.method ?? 'GET'} ${path} → ${r.status}`)
  return r.json() as Promise<T>
}

const json = (body: unknown) => ({
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
})

export const api = {
  health: () => req<{ ok: boolean }>('/health'),
  createProject: (name: string, cwd: string) =>
    req<Project>('/api/projects', json({ name, cwd })),
  createSession: (project_id: string, title: string, opencode_session_id?: string | null) =>
    req<Session>('/api/sessions', json({ project_id, title, opencode_session_id })),
  listSessions: (project_id: string) => req<Session[]>(`/api/sessions?project_id=${project_id}`),
  postMessage: (sid: string, content: string, feature = '') =>
    req<{ reply: string; tokens: number; status: string }>(
      `/api/sessions/${sid}/messages`,
      json({ content, feature }),
    ),
  getMessages: (sid: string) => req<Message[]>(`/api/sessions/${sid}/messages`),
  interrupt: (sid: string) =>
    req<{ interrupted: boolean }>(`/api/sessions/${sid}/interrupt`, { method: 'POST' }),
  tokensSummary: (project_id: string) =>
    req<{ project_id: string; total_tokens: number; by_session: Record<string, number>; by_feature: Record<string, number> }>(
      `/api/tokens/summary?project_id=${project_id}`,
    ),
  createCard: (card: Pick<Card, 'project_id' | 'title'> & Partial<Card>) =>
    req<Card>('/api/cards', json(card)),
  listCards: (project_id: string) => req<Card[]>(`/api/cards?project_id=${project_id}`),
  patchCard: (id: string, status: Card['status']) =>
    req<Card>(`/api/cards/${id}`, { ...json({ status }), method: 'PATCH' }),
  createDebate: (project_id: string, backend_session_id: string, frontend_session_id: string) =>
    req<Debate>('/api/debates', json({ project_id, backend_session_id, frontend_session_id })),
  getDebate: (id: string) => req<Debate>(`/api/debates/${id}`),
  propose: (id: string, from: string, content: string) =>
    req<Debate>(`/api/debates/${id}/propose`, json({ from, content })),
  approve: (id: string, approve: boolean) =>
    req<Debate>(`/api/debates/${id}/approve`, json({ approve })),
  locks: () => req<{ path: string; locked_by: string }[]>('/api/locks'),
  acquireLock: (path: string, locked_by: string) =>
    req<{ path: string; locked_by: string }>('/api/locks', json({ path, locked_by })),
  opencodeSessions: () => req<{ id: string; title: string }[]>('/api/opencode/sessions'),
  readFile: (project_id: string, path: string) =>
    req<{ path: string; content: string }>(
      `/api/files?project_id=${project_id}&path=${encodeURIComponent(path)}`,
    ),
  consolidateEngram: (card_id: string, problema: string, solucion = '') =>
    req<{ ok: boolean }>(
      '/api/engrams',
      json({ card_id, problema, solucion }),
    ),
  searchEngrams: (q: string) =>
    req<{ card_id: string; score: number }[]>(`/api/engrams/search?q=${encodeURIComponent(q)}`),
}

export function chatSocket(sessionId: string): WebSocket {
  const proto = location.protocol === 'https:' ? 'wss://' : 'ws://'
  return new WebSocket(`${proto}${location.host}/ws/sessions/${sessionId}`)
}

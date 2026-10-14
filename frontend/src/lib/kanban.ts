import type { Card } from './api'

export interface FlowNode {
  id: string
  position: { x: number; y: number }
  data: { label: string; blocked: boolean; status: Card['status'] }
}

export interface FlowEdge {
  id: string
  source: string
  target: string
  animated: boolean
}

const COLS: Card['status'][] = ['backlog', 'progreso', 'pruebas', 'listo']

export function toFlow(cards: Card[]): { nodes: FlowNode[]; edges: FlowEdge[] } {
  const byCol: Record<string, number> = {}
  const nodes = cards.map((c) => {
    const col = COLS.indexOf(c.status)
    const row = byCol[c.status] ?? 0
    byCol[c.status] = row + 1
    return {
      id: c.id,
      position: { x: col * 240, y: row * 90 },
      data: { label: `${c.title}${c.blocked ? ' ⛔' : ''}`, blocked: c.blocked, status: c.status },
    }
  })
  const ids = new Set(cards.map((c) => c.id))
  const edges = cards.flatMap((c) =>
    c.depends_on
      .filter((d) => ids.has(d))
      .map((d) => ({ id: `${d}->${c.id}`, source: d, target: c.id, animated: c.blocked })),
  )
  return { nodes, edges }
}

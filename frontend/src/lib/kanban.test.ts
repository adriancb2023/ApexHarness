import { describe, expect, it } from 'vitest'
import type { Card } from './api'
import { toFlow } from './kanban'

const card = (over: Partial<Card> & { id: string }): Card => ({
  project_id: 'p',
  title: over.id,
  feature: '',
  files: [],
  depends_on: [],
  status: 'backlog',
  blocked: false,
  ...over,
})

describe('kanban', () => {
  it('deriva edges y filtra dependencias externas', () => {
    const { nodes, edges } = toFlow([
      card({ id: 'a', status: 'listo' }),
      card({ id: 'b', depends_on: ['a', 'zzz'], blocked: true }),
    ])
    expect(nodes).toHaveLength(2)
    expect(edges).toEqual([{ id: 'a->b', source: 'a', target: 'b', animated: true }])
    expect(nodes[1].data.label).toContain('⛔')
  })

  it('coloca por columna de estado', () => {
    const { nodes } = toFlow([card({ id: 'a', status: 'pruebas' })])
    expect(nodes[0].position.x).toBe(2 * 240)
  })
})

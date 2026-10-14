import { describe, expect, it } from 'vitest'
import { needsIntervention, splitTurns } from './debate'

describe('debate', () => {
  it('reparte turnos por remitente', () => {
    const { backend, frontend } = splitTurns([
      { from: 'backend', to: 'frontend', content: 'a' },
      { from: 'frontend', to: 'backend', content: 'b' },
      { from: 'backend', to: 'frontend', content: 'c' },
    ])
    expect(backend.map((t) => t.content)).toEqual(['a', 'c'])
    expect(frontend.map((t) => t.content)).toEqual(['b'])
  })

  it('detecta intervención', () => {
    expect(needsIntervention('needs_intervention')).toBe(true)
    expect(needsIntervention('open')).toBe(false)
  })
})

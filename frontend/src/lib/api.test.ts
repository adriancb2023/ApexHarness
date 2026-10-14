import { describe, expect, it, vi } from 'vitest'
import { api } from './api'

function mockFetch(payload: unknown) {
  globalThis.fetch = vi.fn().mockResolvedValue({ ok: true, json: () => payload })
  return globalThis.fetch as unknown as ReturnType<typeof vi.fn>
}

describe('api', () => {
  it('lista sesiones del proyecto', async () => {
    const f = mockFetch([{ id: 'a' }])
    const out = await api.listSessions('p1')
    expect(f).toHaveBeenCalledWith('/api/sessions?project_id=p1', undefined)
    expect(out).toEqual([{ id: 'a' }])
  })

  it('crea tarjeta con dependencias', async () => {
    const f = mockFetch({ id: 'c1' })
    await api.createCard({ project_id: 'p1', title: 'UI', depends_on: ['x'] })
    expect(f.mock.calls[0][0]).toBe('/api/cards')
    expect(JSON.parse(f.mock.calls[0][1].body)).toMatchObject({ depends_on: ['x'] })
  })

  it('lanza error con status', async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({ ok: false, status: 409 })
    await expect(api.approve('d', true)).rejects.toThrow('409')
  })
})

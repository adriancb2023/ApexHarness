import { useState } from 'react'
import { api, type Debate as DebateT, type Session } from '../lib/api'
import { needsIntervention, splitTurns } from '../lib/debate'

export default function Debate({
  projectId,
  sessions,
}: {
  projectId: string
  sessions: Session[]
}) {
  const [backendId, setBackendId] = useState('')
  const [frontendId, setFrontendId] = useState('')
  const [debate, setDebate] = useState<DebateT | null>(null)
  const [draft, setDraft] = useState('')
  const [draftFrom, setDraftFrom] = useState('backend')

  async function create() {
    if (!projectId || !backendId || !frontendId) return
    setDebate(await api.createDebate(projectId, backendId, frontendId))
  }

  async function refresh() {
    if (!debate) return
    setDebate(await api.getDebate(debate.id))
  }

  async function propose() {
    if (!debate || !draft) return
    setDebate(await api.propose(debate.id, draftFrom, draft))
    setDraft('')
  }

  async function approve(ok: boolean) {
    if (!debate) return
    setDebate(await api.approve(debate.id, ok))
  }

  const { backend, frontend } = splitTurns(debate?.turns ?? [])

  return (
    <section>
      <h2 className="font-bold">Debate</h2>
      <div className="flex gap-2 mt-1 text-sm">
        <select className="border" value={backendId} onChange={(e) => setBackendId(e.target.value)}>
          <option value="">— backend —</option>
          {sessions.map((s) => (
            <option key={s.id} value={s.id}>
              {s.title} ({s.id})
            </option>
          ))}
        </select>
        <select
          className="border"
          value={frontendId}
          onChange={(e) => setFrontendId(e.target.value)}
        >
          <option value="">— frontend —</option>
          {sessions.map((s) => (
            <option key={s.id} value={s.id}>
              {s.title} ({s.id})
            </option>
          ))}
        </select>
        <button className="border px-2" onClick={create}>
          crear
        </button>
        {debate && (
          <button className="border px-2" onClick={refresh}>
            actualizar
          </button>
        )}
      </div>
      {debate && (
        <div id="debate-view" className="mt-2">
          <div className="flex items-center gap-2 text-sm">
            <span data-state={debate.status} className="border px-1">
              {debate.status} ({debate.turn_count}/5)
            </span>
            {needsIntervention(debate.status) && <span>⚠ intervención requerida</span>}
          </div>
          <div className="grid grid-cols-3 gap-2 mt-2 text-sm">
            <div data-agent="backend" className="border p-2">
              <h3 className="font-bold">Backend</h3>
              <ul>
                {backend.map((t, i) => (
                  <li key={i}>{t.content}</li>
                ))}
              </ul>
            </div>
            <div data-debate="turns" className="border p-2">
              <h3 className="font-bold">Debate</h3>
              <ul>
                {debate.turns.map((t, i) => (
                  <li key={i}>
                    <b>{t.from}:</b> {t.content}
                  </li>
                ))}
              </ul>
              {debate.pending && (
                <div className="border-t mt-2 pt-2">
                  <p>
                    pendiente de <b>{debate.pending.from}</b>: {debate.pending.content}
                  </p>
                  <div className="flex gap-2 mt-1">
                    <button id="approve-btn" className="border px-2" onClick={() => approve(true)}>
                      aprobar envío
                    </button>
                    <button className="border px-2" onClick={() => approve(false)}>
                      rechazar
                    </button>
                  </div>
                </div>
              )}
            </div>
            <div data-agent="frontend" className="border p-2">
              <h3 className="font-bold">Frontend</h3>
              <ul>
                {frontend.map((t, i) => (
                  <li key={i}>{t.content}</li>
                ))}
              </ul>
            </div>
          </div>
          <div className="flex gap-2 mt-2 text-sm">
            <select className="border" value={draftFrom} onChange={(e) => setDraftFrom(e.target.value)}>
              <option value="backend">backend</option>
              <option value="frontend">frontend</option>
            </select>
            <input
              className="border px-2 flex-1"
              value={draft}
              onChange={(e) => setDraft(e.target.value)}
              placeholder="propuesta"
            />
            <button className="border px-2" onClick={propose}>
              proponer
            </button>
          </div>
        </div>
      )}
    </section>
  )
}

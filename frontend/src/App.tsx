import { useEffect, useState } from 'react'
import { api, type Card, type Project, type Session } from './lib/api'
import Chat from './views/Chat'
import Debate from './views/Debate'
import FileViewer from './views/FileViewer'
import Kanban from './views/Kanban'
import Tokens from './views/Tokens'

export default function App() {
  const [projects, setProjects] = useState<Project[]>([])
  const [projectId, setProjectId] = useState('')
  const [sessions, setSessions] = useState<Session[]>([])
  const [sessionId, setSessionId] = useState('')
  const [card, setCard] = useState<Card | null>(null)
  const [name, setName] = useState('')
  const [cwd, setCwd] = useState('')

  useEffect(() => {
    if (!projectId) {
      setSessions([])
      return
    }
    api.listSessions(projectId).then(setSessions).catch(() => setSessions([]))
  }, [projectId])

  async function addProject() {
    if (!name || !cwd) return
    const p = await api.createProject(name, cwd)
    setProjects([...projects, p])
    setProjectId(p.id)
    setName('')
  }

  return (
    <main className="p-4 max-w-4xl mx-auto flex flex-col gap-6">
      <h1 className="text-xl font-bold">ApexHarness</h1>
      <section>
        <div className="flex gap-2">
          <input
            aria-label="nombre"
            className="border px-2"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="proyecto"
          />
          <input
            aria-label="cwd"
            className="border px-2"
            value={cwd}
            onChange={(e) => setCwd(e.target.value)}
            placeholder="C:/ruta"
          />
          <button className="border px-2" onClick={addProject}>
            añadir
          </button>
        </div>
        <select
          id="project-selector"
          className="border mt-2 w-full"
          value={projectId}
          onChange={(e) => setProjectId(e.target.value)}
        >
          <option value="">— proyecto —</option>
          {projects.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
        <select
          id="session-selector"
          className="border mt-2 w-full"
          value={sessionId}
          onChange={(e) => setSessionId(e.target.value)}
        >
          <option value="">— sesión —</option>
          {sessions.map((s) => (
            <option key={s.id} value={s.id}>
              {s.title} ({s.id})
            </option>
          ))}
        </select>
        <ul id="session-list" className="mt-2 text-sm">
          {sessions.map((s) => (
            <li key={s.id}>
              {s.title} ({s.id})
            </li>
          ))}
        </ul>
      </section>
      <Chat sessionId={sessionId} />
      <Debate projectId={projectId} sessions={sessions} />
      <Kanban projectId={projectId} onSelect={setCard} />
      <FileViewer projectId={projectId} card={card} />
      <Tokens projectId={projectId} />
    </main>
  )
}

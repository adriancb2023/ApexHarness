import { useEffect, useState } from 'react'
import { api, type Project, type Session } from './lib/api'

export default function App() {
  const [projects, setProjects] = useState<Project[]>([])
  const [projectId, setProjectId] = useState('')
  const [sessions, setSessions] = useState<Session[]>([])
  const [name, setName] = useState('')
  const [cwd, setCwd] = useState('')

  useEffect(() => {
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
    <main className="p-4 max-w-2xl mx-auto">
      <h1 className="text-xl font-bold">ApexHarness</h1>
      <div className="flex gap-2 mt-4">
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
        className="border mt-4 w-full"
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
      <ul id="session-list" className="mt-2">
        {sessions.map((s) => (
          <li key={s.id}>
            {s.title} ({s.id})
          </li>
        ))}
      </ul>
    </main>
  )
}

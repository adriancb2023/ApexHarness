import Editor from '@monaco-editor/react'
import { useEffect, useState } from 'react'
import { api, type Card } from '../lib/api'

export default function FileViewer({
  projectId,
  card,
}: {
  projectId: string
  card: Card | null
}) {
  const [file, setFile] = useState('')
  const [content, setContent] = useState('// elige archivo')

  useEffect(() => {
    setFile(card?.files[0] ?? '')
  }, [card])

  useEffect(() => {
    if (!projectId || !file) return
    api
      .readFile(projectId, file)
      .then((r) => setContent(r.content))
      .catch(() => setContent('// no legible'))
  }, [projectId, file])

  if (!card) return null
  return (
    <section>
      <div className="flex items-center gap-2">
        <h2 className="font-bold">Visor</h2>
        <select className="border text-sm" value={file} onChange={(e) => setFile(e.target.value)}>
          {(card.files ?? []).map((f) => (
            <option key={f} value={f}>
              {f}
            </option>
          ))}
        </select>
      </div>
      <div className="border mt-1">
        <Editor height="300px" language="plaintext" value={content} options={{ readOnly: true }} />
      </div>
    </section>
  )
}

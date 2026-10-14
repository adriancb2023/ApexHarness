import { useEffect, useState } from 'react'
import { api } from '../lib/api'

export default function Tokens({ projectId }: { projectId: string }) {
  const [total, setTotal] = useState(0)
  const [byFeature, setByFeature] = useState<Record<string, number>>({})

  async function refresh() {
    if (!projectId) return
    const s = await api.tokensSummary(projectId).catch(() => null)
    if (!s) return
    setTotal(s.total_tokens)
    setByFeature(s.by_feature)
  }

  useEffect(() => {
    refresh().catch(() => null)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projectId])

  return (
    <section>
      <div className="flex items-center gap-2">
        <h2 className="font-bold">Tokens</h2>
        <button className="border px-2 text-sm" onClick={refresh}>
          actualizar
        </button>
      </div>
      <div id="tokens-panel" data-total={total} className="mt-1">
        {total} tokens
      </div>
      <ul className="text-sm">
        {Object.entries(byFeature).map(([f, n]) => (
          <li key={f}>
            {f}: {n}
          </li>
        ))}
      </ul>
    </section>
  )
}

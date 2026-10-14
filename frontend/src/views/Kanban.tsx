import { useCallback, useEffect, useState } from 'react'
import { ReactFlow, Background, Controls } from 'reactflow'
import 'reactflow/dist/style.css'
import { api, type Card } from '../lib/api'
import { toFlow } from '../lib/kanban'

const NEXT: Record<Card['status'], Card['status'][]> = {
  backlog: ['progreso'],
  progreso: ['pruebas', 'backlog'],
  pruebas: ['listo', 'progreso'],
  listo: [],
}

export default function Kanban({
  projectId,
  onSelect,
}: {
  projectId: string
  onSelect: (card: Card | null) => void
}) {
  const [cards, setCards] = useState<Card[]>([])
  const [selected, setSelected] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    if (!projectId) return
    setCards(await api.listCards(projectId).catch(() => []))
  }, [projectId])

  useEffect(() => {
    setSelected(null)
    onSelect(null)
    refresh().catch(() => null)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projectId])

  async function transition(id: string, status: Card['status']) {
    await api.patchCard(id, status).catch(() => null)
    refresh().catch(() => null)
  }

  const { nodes, edges } = toFlow(cards)
  const current = cards.find((c) => c.id === selected) ?? null

  return (
    <section>
      <div className="flex items-center gap-2">
        <h2 className="font-bold">Kanban</h2>
        <button className="border px-2 text-sm" onClick={() => refresh()}>
          actualizar
        </button>
      </div>
      <div id="kanban-board" className="border mt-1 h-96">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodeClick={(_, n) => {
            setSelected(n.id)
            onSelect(cards.find((c) => c.id === n.id) ?? null)
          }}
          fitView
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>
      {current && (
        <div className="flex gap-2 mt-2 text-sm items-center">
          <span>
            {current.title} [{current.status}]{current.blocked ? ' ⛔ bloqueada' : ''}
          </span>
          {NEXT[current.status].map((s) => (
            <button key={s} className="border px-2" onClick={() => transition(current.id, s)}>
              → {s}
            </button>
          ))}
        </div>
      )}
    </section>
  )
}

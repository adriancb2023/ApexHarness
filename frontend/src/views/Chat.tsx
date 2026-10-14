import { useEffect, useRef, useState } from 'react'
import { api, chatSocket } from '../lib/api'

type Status = 'idle' | 'working' | 'done' | 'needs_approval'

export default function Chat({ sessionId }: { sessionId: string }) {
  const [log, setLog] = useState<string[]>([])
  const [input, setInput] = useState('')
  const [status, setStatus] = useState<Status>('idle')
  const ws = useRef<WebSocket | null>(null)

  useEffect(() => {
    setLog([])
    if (!sessionId) return
    api.getMessages(sessionId).then(
      (ms) => setLog(ms.map((m) => `${m.role}: ${m.content}`)),
      () => setLog([]),
    )
    const sock = chatSocket(sessionId)
    ws.current = sock
    let current = ''
    sock.onmessage = (ev) => {
      const m = JSON.parse(ev.data)
      if (m.delta) {
        current += m.delta
        setLog((prev) => [...prev.slice(0, -1), `assistant: ${current}`].slice(-200))
      }
      if (m.done) setStatus(m.status === 'done' ? 'done' : 'needs_approval')
    }
    sock.onclose = () => setStatus((s) => (s === 'working' ? 'done' : s))
    return () => sock.close()
  }, [sessionId])

  function send() {
    if (!input || ws.current?.readyState !== 1) return
    setStatus('working')
    setLog((prev) => [...prev, `user: ${input}`, 'assistant: '])
    ws.current.send(JSON.stringify({ content: input }))
    setInput('')
  }

  async function interrupt() {
    if (!sessionId) return
    await api.interrupt(sessionId).catch(() => null)
    setStatus('done')
  }

  if (!sessionId) return <p className="text-gray-500">elige sesión</p>
  return (
    <section>
      <div className="flex items-center gap-2">
        <h2 className="font-bold">Chat</h2>
        <span id="task-status" data-state={status} className="text-xs border px-1">
          {status}
        </span>
        <button id="interrupt-btn" className="border px-2 text-sm" onClick={interrupt}>
          interrumpir
        </button>
      </div>
      <div id="chat-log" className="border h-64 overflow-auto p-2 mt-2 text-sm">
        {log.map((l, i) => (
          <div key={i}>{l}</div>
        ))}
      </div>
      <div className="flex gap-2 mt-2">
        <input
          id="chat-input"
          className="border px-2 flex-1"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && send()}
          placeholder="habla con opencode"
        />
        <button className="border px-2" onClick={send}>
          enviar
        </button>
      </div>
    </section>
  )
}

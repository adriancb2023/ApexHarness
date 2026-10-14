export interface Turn {
  from: string
  to: string
  content: string
}

export function splitTurns(turns: Turn[]): { backend: Turn[]; frontend: Turn[] } {
  return {
    backend: turns.filter((t) => t.from === 'backend'),
    frontend: turns.filter((t) => t.from === 'frontend'),
  }
}

export function needsIntervention(status: string): boolean {
  return status === 'needs_intervention'
}

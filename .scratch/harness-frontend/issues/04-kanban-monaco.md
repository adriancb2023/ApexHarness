# 04: Kanban Flow + Monaco

**What to build:** Grafo de dependencias y visor de código.

**Blocked by:** 01 scaffold-api.

**Status:** ready-for-agent

- [x] Nodos tarjetas + edges depends_on + badges bloqueo en React Flow
- [x] Transiciones de estado desde el tablero
- [x] Visor Monaco read-only de archivos de la tarjeta
- [ ] E2E manual (kanban con dependencias, visor de archivo real)

## Comments

Implementado (`views/Kanban.tsx` + `FileViewer.tsx` + `lib/kanban.ts` con 2 tests + `GET /api/files` con guardia cwd y 2 tests). Transiciones limitadas a adyacentes.

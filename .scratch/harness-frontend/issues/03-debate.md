# 03: Debate 3 columnas + approve

**What to build:** Paridad del debate inter-agente con stepping visible.

**Blocked by:** 01 scaffold-api.

**Status:** ready-for-agent

- [x] Columnas backend|debate|frontend con turnos y pendientes
- [x] Botón aprobar/rechazar funcional
- [x] Estado needs_intervention visible
- [ ] E2E manual (crear 2 sesiones, debate, proponer, aprobar, llegar a cap)

## Comments

Implementado (`views/Debate.tsx` + `lib/debate.ts` con 2 tests). Proponer/aprobar vía api.ts.

# 02: Chat + interrupt + tokens

**What to build:** Paridad de chat con streaming, parada y contadores.

**Blocked by:** 01 scaffold-api.

**Status:** ready-for-agent

- [x] Chat con streaming WS y task-status como hoy
- [x] Botón interrumpir funcional
- [x] Panel tokens por proyecto/feature
- [ ] E2E manual (checklist abajo)

## Comments

Implementado (`views/Chat.tsx`, `views/Tokens.tsx`, selector de sesión; `tsc+build` ok, Vitest 3/3). Sin lógica pura nueva → sin tests front nuevos.

E2E manual: `uvicorn app.main:app` con `HARNESS_DB` tmp + `npm run dev`; crear proyecto, crear sesión (vía API), elegirla, enviar mensaje, ver streaming + status, pulsar interrumpir, revisar panel tokens.

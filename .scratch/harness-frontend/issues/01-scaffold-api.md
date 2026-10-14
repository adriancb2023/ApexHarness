# 01: Scaffold + api.ts + servir dist

**What to build:** Base Vite corriendo contra el backend con cliente API tipado.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [x] Scaffold react-ts con proxy /api+/ws a FastAPI
- [x] api.ts con todas las llamadas + 1+ tests Vitest con fetch mockeado
- [x] Vista mínima: selector proyectos + sesiones desde backend real
- [x] Backend sirve frontend/dist si existe, si no la estática (test)

## Comments

Implementado (Vite + Tailwind + api.ts + App mínima, Vitest 3/3, `tsc+build` ok). `dist/` y `node_modules/` ignorados; tests GUI fijan la estática para no depender del build local.

Status: ready-for-agent

# Spec: Frontend Vite (2C)

## Problem Statement

La GUI actual es un HTML estático servido por FastAPI: sin grafo de dependencias, sin visor de código y sin estructura para crecer. El Harness necesita su centro de control visual: kanban con flechas, debate a 3 columnas y visor de archivos.

## Solution

App React + Vite + Tailwind con React Flow (flechas del Kanban) y Monaco read-only (visor). Paridad con la GUI estática más grafo y visor. Dev con proxy a FastAPI; en prod FastAPI sirve `frontend/dist` con fallback a la estática.

## User Stories

1. As un desarrollador, I want selector de proyectos y lista de sesiones en React, so that cambio de contexto visualmente.
2. As un desarrollador, I want chat con streaming WS igual que hoy, so that hablo con OpenCode.
3. As un desarrollador, I want botón interrumpir visible junto al chat, so that paro ejecuciones.
4. As un supervisor, I want debate backend|debate|frontend con botón aprobar, so that controlo el tráfico inter-agente.
5. As un desarrollador, I want Kanban con flechas de dependencia (React Flow) y badges de bloqueo, so that veo el grafo.
6. As un desarrollador, I want panel de tokens por proyecto/feature, so that controlo consumo.
7. As un revisor, I want visor Monaco read-only de archivos de la tarjeta, so that leo cambios sin editar.
8. As un desarrollador, I want `npm run dev` con proxy y `npm run build` servido por el backend, so that un solo puerto en prod.

## Implementation Decisions

- `frontend/` con `lib/api.ts` (único acceso a HTTP/WS), vistas por dominio, sin lógica de negocio fuera de `lib`.
- React Flow solo para el grafo Kanban (nodos = tarjetas, edges = `depends_on`); resto layout Tailwind.
- Monaco read-only; edición/aprobación fuera de alcance.
- Backend: servir `frontend/dist` si existe, si no la estática actual. Sin cambios de API.
- Proxy dev `/api` + `/ws` → `localhost:8000` en `vite.config.ts`.

## Testing Decisions

- Vitest para `lib` y lógica de presentación con fetch/WS mockeados; sin e2e automático en 2C.
- E2E manual contra backend (checklist: sesiones, chat, kanban, debate, tokens, interrupt).
- Backend: test de que `/` sirve `dist` cuando existe y estática si no.

## Out of Scope

- Edición y aprobación en Monaco, diff viewer.
- E2E automático (Playwright), Design Mode headless.
- Cambios de API del backend, refactoring de stores.
- PWA, i18n, theming.

## Further Notes

- Toolchain verificado: node 24 + npm 11.
- Siguiente: `to-tickets` en `.scratch/harness-frontend/issues/`.

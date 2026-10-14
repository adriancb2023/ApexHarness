Status: ready-for-agent

# Spec: Gateway real OpenCode (2B)

## Problem Statement

El Harness habla con un eco fake: no hay respuestas reales, los tokens son estimados por longitud y no hay streaming del agente. Para valor real debe ser cliente del `serve` de OpenCode con sesiones vinculadas a IDs reales.

## Solution

`OpencodeGateway` con dos implementaciones: Fake (actual, tests) y Serve (HTTP contra `serve` v2 con auth Basic). Sesiones Harness guardan `opencode_session_id`; mensajes van a `POST /api/session/{id}/prompt`; eventos `/api/event` (SSE) alimentan el WS; `interrupt` expuesto. Tokens reales desde serve al leer el resumen. Service global por defecto, serve dedicado por proyecto opcional. Todo tras flag: tests siempre fake.

Hechos verificados contra serve real (no supuestos):
- `GET /api/session` devuelve sesiones con `tokens{input,output,reasoning,cache}`, `cost`, `model`, `agent`, `outcome`, `time`, `title`, `location.directory`.
- Auth: Basic `opencode:<password de ~/.config/opencode/service.json>` (200 verificado; sin auth 401).
- `/api/event` es stream (la petición queda abierta).
- Existen `/api/session/{id}/prompt|interrupt|background|inbox`, `/api/session/active`, `/api/experimental/session/stats`.
- OpenAPI completo guardado como referencia de implementación.
- Puerto vía `opencode service status`; serve dedicado con `opencode serve --port X <directory>`.

## User Stories

1. As un desarrollador, I want crear una sesión Harness vinculada a una sesión real de OpenCode, so that hablo con el agente de verdad.
2. As un desarrollador, I want enviar un mensaje y recibir el streaming real vía WS, so that veo trabajar al agente.
3. As un desarrollador, I want interrumpir una ejecución larga desde la GUI, so that paro gastos o errores.
4. As un desarrollador, I want ver tokens reales (input/output/cache) por sesión/proyecto, so that el contador es verdad.
5. As un supervisor, I want usar el service global por defecto y un serve dedicado por proyecto si quiero, so that elijo aislamiento.
6. As un desarrollador, I want configurar rutas y serve por env (`HARNESS_DB`, `HARNESS_QDRANT`, `HARNESS_OPENCODE`), so that el `app` de módulo persiste (cierra deuda 2A).
7. As un contribuidor, I want que los tests nunca gasten tokens ni necesiten serve, so that la suite es segura y rápida.

## Implementation Decisions

- `OpencodeGateway`: `list_sessions`, `send_prompt(session_id, text)`, `interrupt(session_id)`, `stream_events()` (SSE → eventos normalizados). Fake conserva eco determinista; Serve usa httpx con Basic auth y base URL configurable.
- Descubrimiento: puerto de `opencode service status`, password de `service.json`; override total por env. Serve dedicado: lanzar `opencode serve --port <libre> <cwd>` por proyecto (gestión mínima: start + URL por proyecto).
- Sesiones Harness: nuevo campo `opencode_session_id` (nullable; null = fake). Mensajes con session vinculada van al serve; sin vínculo, fake.
- Tokens: en modo real, `summary` sincroniza desde `GET /api/session` (input+output+reasoning como total); en fake, conteo actual.
- WS chat: en modo real reenvía deltas del SSE; mantiene protocolo `{delta}/{done}` actual.
- Interrupt: `POST /api/session/{id}/interrupt` + botón GUI (`task-status` → interrupt).
- Config env con defaults actuales (memoria) para no romper tests.

## Testing Decisions

- Buen test: HTTP del Harness con gateway fake (20 actuales intactos) + gateway Serve con transporte HTTP mockeado (verifica auth, paths, parseo SSE) sin red ni gasto.
- Contra serve vivo: solo pruebas manuales documentadas (listar, prompt en sesión de prueba, interrupt), nunca en suite.
- Prior art: TestClient + dobles; MockTransport de httpx para el Serve.

## Out of Scope

- Frontend Vite (2C), worktrees físicos, GitPython.
- `inbox` inter-agente nativo (se evalúa tras ver debate propio en real).
- Background workers propios (el serve ya ejecuta en background).
- Embedding real, costes USD.

## Further Notes

- No hacer `prompt` reales durante implementación salvo prueba manual explícita del usuario (gasta tokens del proveedor).
- Siguiente: `to-tickets` en `.scratch/harness-gateway/issues/`.

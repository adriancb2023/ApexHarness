Status: ready-for-agent

# Spec: Persistencia SQLite file (2A)

## Problem Statement

El backend MVP guarda todo en memoria: al reiniciar el proceso se pierden proyectos, sesiones, mensajes, tarjetas, debates, locks, contadores y secuencia de Engrams. Para uso real el Harness debe sobrevivir a reinicios sin cambiar sus APIs.

## Solution

Mover los stores tras interfaces repositorio con dos implementaciones: memoria (tests, comportamiento actual) y SQLite file vía stdlib (producción). Qdrant pasa de `:memory:` a path local. Las APIs HTTP/WS no cambian.

## User Stories

1. As un desarrollador, I want reiniciar el backend sin perder proyectos ni sesiones, so that retomo donde estaba.
2. As un desarrollador, I want que el historial de chat sobreviva a reinicios, so that la trazabilidad es real.
3. As un supervisor, I want que Kanban, debates, locks y contadores persistan, so that nada se resetea.
4. As un agente, I want que los Engrams persistan en disco, so that la memoria es a largo plazo de verdad.
5. As un desarrollador, I want que los tests sigan corriendo en memoria y rápidos, so that TDD no se relentiza.

## Implementation Decisions

- Un interfaz repositorio por store (proyectos, sesiones, mensajes, tarjetas, debates, locks, tokens/feature, secuencia Engram). La app se construye con una factoría que inyecta memoria o SQLite según configuración.
- SQLite vía stdlib (`sqlite3`), esquema mínimo espejo de las estructuras actuales, una tabla por store más tabla de contadores. Sin ORM ni migraciones en 2A.
- Qdrant con path local en vez de `:memory:`; misma colección y vectores.
- Sin cambios en contratos HTTP/WS: los tests actuales deben pasar sin modificarse.
- El embedding hash y el conteo fake de tokens no cambian en 2A.

## Testing Decisions

- Buen test: comportamiento externo vía HTTP (crear, recrear app sobre mismo fichero, verificar supervivencia), nunca SQL directo.
- Módulos bajo test: cada repositorio (round-trip persistencia) más el test de reinicio end-to-end vía TestClient.
- Prior art: los 16 tests MVP existentes como red de seguridad sin modificar.

## Out of Scope

- Cambios de API, nuevos endpoints o GUI.
- SQLAlchemy, migraciones, Postgres.
- Gateway real contra `serve` (fase 2B), frontend Vite (fase 2C).
- Embedding real, conteo real de tokens.

## Further Notes

- Fichero SQLite por defecto junto al backend, ruta configurable por env. Añadir al `.gitignore` (ya cubierto: `backend/harness.db`).
- Siguiente: `to-tickets` en `.scratch/harness-sqlite/issues/`.

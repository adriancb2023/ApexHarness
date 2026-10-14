# 03: Kanban automático + grafo

**What to build:** Tablero automático alimentado por agentes con dependencias visuales tipo diagrama.

**Blocked by:** 01 skeleton-sesiones.

**Status:** ready-for-agent

- [x] Agentes crean/actualizan tarjetas con dependencias explícitas
- [x] Columnas Backlog / En Progreso / Pruebas / Listo funcionales
- [x] Flechas de dependencia derivadas y bloqueo visual si dep no en Done
- [x] Desbloqueo automático al mover dependencia a Done
- [x] Tests externos de contrato, transiciones y derivación de bloqueos

## Comments

Implementado (CRUD tarjetas + `blocked` derivado + `kanban-edges`, 3 tests nuevos). Flechas como lista `data-edge` en GUI estática; React Flow visual llega con frontend Vite. Deuda: sin validación de proyecto en POST cards, `blocked` global (no por proyecto).

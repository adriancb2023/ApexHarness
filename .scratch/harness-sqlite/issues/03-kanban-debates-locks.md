# 03: Kanban, debates y locks en SQLite

**What to build:** Tarjetas, debates y locks persistidos en SQLite file.

**Blocked by:** 01 factoria-proyectos-sesiones.

**Status:** ready-for-agent

- [x] Tarjetas con estado/dependencias y `blocked` derivado correctos tras reinicio
- [x] Debates con turns/pending/status correctos tras reinicio
- [x] Locks activos correctos tras reinicio
- [x] Tests actuales siguen verdes sin modificarse

## Comments

Implementado (tablas cards/debates/locks con JSON para listas, 1 test nuevo). De paso se corrigió `consolidate_engram` al store.

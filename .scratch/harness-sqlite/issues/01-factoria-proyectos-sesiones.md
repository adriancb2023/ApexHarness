# 01: Factoría repositorios + proyectos/sesiones SQLite

**What to build:** Stores tras interfaces con impl memoria (tests) e impl SQLite file (prod), empezando por proyectos y sesiones que sobreviven a reinicio.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [x] Crear datos vía API, recrear app sobre mismo fichero, verificar que sobreviven
- [x] Tests actuales de sesiones siguen verdes sin modificarse
- [x] Resto de stores aún en memoria

## Comments

Implementado (`store.py` Memory/SQLite + `db_path`, 1 test nuevo). Resto (mensajes, tarjetas, debates, locks) en tickets 02-03.

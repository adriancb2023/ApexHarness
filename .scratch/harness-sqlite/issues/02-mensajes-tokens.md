# 02: Mensajes y tokens en SQLite

**What to build:** Historial de chat y contadores de tokens persistidos en SQLite file.

**Blocked by:** 01 factoria-proyectos-sesiones.

**Status:** ready-for-agent

- [x] Mensajes con tokens/ts/feature sobreviven a reinicio
- [x] Resumen de tokens por sesión/proyecto/feature consistente tras reinicio
- [x] Tests actuales de chat y tokens siguen verdes sin modificarse

## Comments

Implementado (tablas messages + feature_tokens, 1 test nuevo). Orden por `seq` autoincremental.

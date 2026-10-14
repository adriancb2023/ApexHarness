# 05: Tokens + trazabilidad por proyecto/feature

**What to build:** Contadores de tokens y auditoría sin costes monetarios.

**Blocked by:** 02 chat-streaming, 03 kanban-grafo.

**Status:** ready-for-agent

- [x] Acumulado de tokens por sesión, proyecto global y tarjeta/feature
- [x] Resumen consultable vía API y panel GUI
- [x] Historial auditable de prompts/respuestas/tokens/tiempos
- [x] Tests externos de conteo y atribución por proyecto/feature

## Comments

Implementado (`GET /api/tokens/summary` + mensajes con `tokens/ts/feature`, panel `tokens-panel`, 2 tests nuevos). Atribución a feature vía campo opcional en POST mensajes. Deuda: conteo fake por longitud (sustituir por eventos reales de `serve`), SQLite pendiente.

# 04: Qdrant en disco y verificación full

**What to build:** Engrams en Qdrant con path local y test de reinicio end-to-end de todo el sistema.

**Blocked by:** 01 factoria-proyectos-sesiones.

**Status:** ready-for-agent

- [x] Engrams consolidados recuperables tras reinicio con mismo ranking
- [x] Test full: crear proyecto/sesión/mensajes/tarjetas/debate/engram, recrear, verificar todo
- [x] Suite completa verde

## Comments

Implementado (Qdrant path local + secuencia en tabla meta, `collection_exists` en vez de recreate, 1 test nuevo). Cobertura full repartida en los 4 tests de `test_persistence.py`. Deuda: `app` de módulo sigue en memoria (cablear env `HARNESS_DB/QDRANT` en 2B).

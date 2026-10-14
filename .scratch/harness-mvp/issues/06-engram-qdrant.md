# 06: Engram Qdrant + consolidación

**What to build:** Memoria a largo plazo con calidad sobre cantidad.

**Blocked by:** 03 kanban-grafo, 05 tokens-trazabilidad.

**Status:** ready-for-agent

- [x] Guardar resumen estructurado solo al pasar a Done (Problema/Solución/Archivos/Lecciones)
- [x] Recuperar experiencias similares como contexto al iniciar tarea
- [x] Qdrant embebido local sin servicios externos en MVP
- [x] Tests externos de consolidación y recuperación con store fake

## Comments

Implementado (Qdrant `:memory:` + embedding determinista md5-64d, guard 409 si no Done, `GET /api/engrams/search`). Deuda: embedding hash (sustituir por modelo real), persistencia en disco (path Qdrant local), panel GUI de memoria.

# `.harness/` — artefactos del pipeline

Directorio runtime del Engineering Agent Harness; lo escribe el Orchestrator
(es el único agente con permiso de edición aquí).

## `state.md` — estado del pipeline de la tarea en curso
Máquina de estados visible: task, pipeline, estado actual, agent/skills elegidas
y descartadas, memoria consultada, transiciones con evidencia y timestamps.
Formato en harness-core §6. Se sobrescribe por tarea (≤40 líneas).

## `cache.md` — verification cache
`| check | comando | inputs (files+hash/mtime) | result | ts |`.
Un check con resultados válidos no se repite si no cambió código; cualquier edit
en los inputs invalida su fila. Reglas en harness-core §7.

## `metrics.jsonl` — métricas por tarea (append)
Una línea JSON por tarea completada. Esquema en harness-core §10 y protocolo de
comparación (con/sin memoria) en `docs/METRICS.md`. Este fichero crece — es el
registro para responder "¿de verdad el harness/Engram mejora las tareas?".

Limpieza: state.md y cache.md pueden resetearse entre tareas; metrics.jsonl
consérvalo.

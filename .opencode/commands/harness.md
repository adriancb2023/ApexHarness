---
description: Ejecuta una tarea a través del protocolo completo del Harness (clasificar → memoria → route → ejecutar → verificar → memoria → DONE)
agent: Apex_Harness
---

Tarea: $ARGUMENTS

Sigue el protocolo completo del Orchestrator: carga `harness-core`, clasifica la
tarea, aplica el gate de memoria, selecciona agente y skills, ejecuta vía subagente
con handoff compacto, verifica con evidencia y emite veredicto con estados
COMPLETED / FAILED / BLOCKED / UNVERIFIED. Registra el pipeline en
`.harness/state.md` y cierra con métricas (`.harness/metrics.jsonl`) y
`mem_session_summary`.

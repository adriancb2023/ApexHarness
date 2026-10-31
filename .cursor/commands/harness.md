---
description: Ejecuta una tarea con el protocolo completo del Apex Harness
---

Tarea: $ARGUMENTS

Sigue el protocolo completo del Orchestrator Apex Harness en Cursor:

1. Carga `harness-core` y clasifica (BUG / DEV / Answer).
2. Gate de memoria Engram; skills Matt 2–4 con valor (anota descartadas).
3. Delega implementación/diagnóstico según `.cursor/rules/apex-roles.mdc` con handoff compacto.
4. Verifica con evidencia (comando + salida). Emite COMPLETED / FAILED / BLOCKED / UNVERIFIED.
5. Actualiza `.harness/state.md`, métricas en `.harness/metrics.jsonl`, y memoria reutilizable al cierre.

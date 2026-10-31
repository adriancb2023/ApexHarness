---
name: harness-core
description: >-
  Core del Engineering Harness — tablas de clasificación de tareas, routing de
  skills y agentes, reglas de memoria Engram, máquina de estados, handoffs,
  verificación y Definition of Done. Cargar al empezar cualquier tarea del
  harness (/harness o pipeline Apex).
---

# Harness Core (Cursor shim)

**Fuente canónica (no duplicar tablas aquí):**

- `.opencode/skills/harness-core/SKILL.md`
- `.opencode/skills/harness-core/references/registry.md` (solo si dudas de una skill)

## Instrucciones

1. Lee el SKILL.md canónico completo con la herramienta Read.
2. Aplica sus tablas (§1–§12) sin re-decidir lo ya resuelto.
3. En Cursor, los agentes `Apex_*` se emulan vía `.cursor/rules/apex-roles.mdc` (no hay allowlist de host).
4. Skills Matt (`tdd`, `code-review`, `diagnosing-bugs`, …): deben existir bajo `.cursor/skills/<id>/` tras el paso de instalación documentado en `docs/CURSOR.md` / README. Si faltan, dilo y no inventes el contenido de la skill.

---
name: harness-core
description: >-
  Core of the Engineering Harness — task classification tables, skill and agent
  routing, Engram memory rules, state machine, handoffs, verification, and
  Definition of Done. Load it at the start of any harness task (/harness or the
  Apex pipeline).
---

# Harness Core (Cursor shim)

**Canonical source (do not duplicate the tables here):**

- `.opencode/skills/harness-core/SKILL.md`
- `.opencode/skills/harness-core/references/registry.md` (only if you are unsure about a skill)

## Instructions

1. Read the canonical SKILL.md in full with the Read tool.
2. Apply its tables (§1–§12) without re-deciding what is already settled.
3. On Cursor, `Apex_*` agents are emulated via `.cursor/rules/apex-roles.mdc` (there is no host allowlist).
4. Matt skills (`tdd`, `code-review`, `diagnosing-bugs`, …): they must exist under `.cursor/skills/<id>/` after the install step documented in `docs/CURSOR.md` / README. If they are missing, say so and do not invent the skill's content.

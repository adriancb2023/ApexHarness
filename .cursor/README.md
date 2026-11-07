# `.cursor/` — Apex Harness installed in Cursor

| Piece | Role |
| --- | --- |
| `rules/apex-harness.mdc` | Orchestrator (`alwaysApply`) |
| `rules/apex-roles.mdc` | Delegates to `apex-*` subagents |
| `agents/apex-harness.md` | Orchestrator subagent (`/apex-harness`) |
| `agents/apex-dev.md` | Implementation |
| `agents/apex-bug.md` | Diagnosis |
| `agents/apex-verifier.md` | `readonly` verification |
| `commands/harness.md` | `/harness <task>` |
| `skills/harness-core/` | Shim → `.opencode/skills/harness-core/` |
| `skills/<matt-id>/` | Skills for Real Engineers (gitignored) |
| `mcp.json` | Local Engram |

## Activate / repair

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-cursor-harness.ps1
```

Then **restart Cursor** (full quit). Check Settings → Tools & MCP → `engram` and that the `apex-*` subagents appear when delegating.

Guide: `docs/CURSOR.md`.

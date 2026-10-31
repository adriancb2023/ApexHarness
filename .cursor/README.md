# `.cursor/` — Apex Harness instalado en Cursor

| Pieza | Rol |
| --- | --- |
| `rules/apex-harness.mdc` | Orchestrator (`alwaysApply`) |
| `rules/apex-roles.mdc` | Delega a subagentes `apex-*` |
| `agents/apex-harness.md` | Subagente orchestrator (`/apex-harness`) |
| `agents/apex-dev.md` | Implementación |
| `agents/apex-bug.md` | Diagnóstico |
| `agents/apex-verifier.md` | Verificación `readonly` |
| `commands/harness.md` | `/harness <tarea>` |
| `skills/harness-core/` | Shim → `.opencode/skills/harness-core/` |
| `skills/<matt-id>/` | Skills for Real Engineers (gitignored) |
| `mcp.json` | Engram local |

## Activar / reparar

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-cursor-harness.ps1
```

Luego **reinicia Cursor** (quit completo). Comprueba Settings → Tools & MCP → `engram` y que los subagentes `apex-*` aparezcan al delegar.

Guía: `docs/CURSOR.md`.

# Portabilidad a Cursor (implementada)

El harness funciona en Cursor vía `.cursor/` (rules, commands, skills shim, MCP).
Las **27 skills de Matt Pocock no van en el repo** (opción A): son paso de instalación
obligatorio, igual que en OpenCode.

## Mapa (verificado en esta máquina / docs Cursor 2026)

| Componente OpenCode | Cursor |
| --- | --- |
| `AGENTS.md` + Orchestrator | `.cursor/rules/apex-harness.mdc` (`alwaysApply: true`) |
| Roles `Apex_*` | `.cursor/agents/apex-{harness,dev,bug,verifier}.md` (subagentes nativos; verifier `readonly`) + `rules/apex-roles.mdc` |
| `harness-core` | `.cursor/skills/harness-core/` (shim → canónico `.opencode/skills/harness-core/`) |
| Skills mattpocock | `.cursor/skills/<id>/` tras instalar (gitignored) |
| `/harness` | `.cursor/commands/harness.md` |
| Policies hard-deny | Soft en rules (Cursor no replica `policies[]` de OpenCode) |
| Engram MCP | `.cursor/mcp.json` → `engram mcp --tools=agent` (binario local en PATH) |
| `.harness/state.md` | Igual |

## Instalación Cursor (tras clonar el harness)

En un repo que ya trae `.cursor/`:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-cursor-harness.ps1
```

Eso verifica agents/rules/commands, bootstrap de las 27 skills Matt (OpenCode+Cursor) y fija MCP Engram.

Manual equivalente:

1. Asegura `.cursor/agents/apex-*.md`, rules, `commands/harness.md`, shim `harness-core`.
2. Skills Matt → `.cursor/skills/` + `.opencode/skills/` (gitignored salvo `harness-core`):
   `npx skills@latest add mattpocock/skills -a opencode -a cursor -y --copy`
   o `.\scripts\bootstrap-matt-skills.ps1 -FromOpenCodeGlobal`
3. Reinicia Cursor (quit completo). Comprueba Settings → Tools & MCP → `engram`;
   subagentes `apex-*`; `/harness <tarea>`.

## Un solo harness

- Solo `apex-harness.mdc` + `apex-roles.mdc` como reglas always-apply del pipeline.
- Borra reglas de un harness anterior que compitan por el mismo paso.
- OpenCode y Cursor pueden coexistir en el mismo repo: `.opencode/` + `.cursor/`.

## Limitaciones vs OpenCode

- Sin hard-deny de spawn/edit: el Verifier es disciplina de prompt, no permiso de host.
- Sin `default_agent`: la regla always-apply hace de orchestrator en cada chat.
- Cloud Engram (`https://mcp.engram.page`) es otro producto; este harness usa el **Engram local** (`mem_*` vía `engram.exe`), alineado con OpenCode.

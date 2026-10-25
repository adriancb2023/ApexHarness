# Hallazgos de capacidades (inspección real, 2026-10-25)

Este MVP se diseñó tras inspeccionar el entorno, no tras la documentación ideal.
Todo lo que sigue se comprobó contra el sistema real de la máquina o contra el
repositorio oficial / docs V2.

## OpenCode

- **Versión:** `opencode v2.1.1` (global, `%APPDATA%\npm`), Windows 11.
- **Mecanismos nativos usados en este MVP:**
  - Agentes Markdown: `.opencode/agents/<id>.md` con frontmatter `description`,
    `mode` (primary/subagent), `permissions` (ordered rules allow/ask/deny con
    last-match-wins), `steps` (tope de pasos con degradación controlada), `color`.
  - Comandos: `.opencode/commands/<id>.md` con `agent:` y `$ARGUMENTS`.
  - Skills: `.opencode/skills/<id>/SKILL.md` + archivos de soporte; publicidad vía
    `description`, carga perezosa por ID con la herramienta `skill`;
    `disable-model-invocation` las esconde del modelo (se cargan por ID explícito).
  - Permisos/Policies: `permissions[]` (fricción y allowlist) + `policies[]`
    (hard-deny imbatible incluso para reglas de agente y aprobaciones guardadas).
  - `AGENTS.md` se inyecta como instrucciones del proyecto.
  - Subagentes: contexto fresco; `description` del frontmatter es lo que ve el
    parent al elegir; permisos del child, no heredados.
- **Config global existente:** `~/.config/opencode/opencode.jsonc` declara MCP
  `engram` (`engram.exe mcp --tools=agent`) y MCP `rea`. `~/.config/opencode/plugins/
  engram.ts` (plugin de memoria: registra sesiones, inyecta protocolo Engram en
  cada system prompt, nudge de save cada ~15 min, hook de compaction que persiste
  summary + reinyecta contexto, captura pasiva del output de Task).
- **Preexistente de usuario:** un agente global `apex` (prompt monolítico estilo
  "carga 27 skills y decide") — el MVP del harness lo sustituye en este repo vía
  `default_agent: Apex_Harness`; el agente global no se toca.

## Skills de Matt Pocock

- Instaladas en `~/.config/opencode/skills/` (27): ask-matt, code-review,
  codebase-design, diagnosing-bugs, domain-modeling, grill-me, grill-with-docs,
  grilling, handoff, implement, implement-spec, improve-codebase-architecture, pr,
  prototype, research, retro, setup-matt-pocock-skills, tdd, teach,
  to-questionnaire, to-spec, to-tickets, triage, wait-what, wayfinder, wizard,
  writing-for-agents.
- **Verificación contra el repo oficial** (api.github.com, árbol `main`,
  2026-10-25): el set instalado coincide exactamente con `skills/engineering/`
  (20) + `skills/productivity/` (7). Existen además en el repo `skills/misc/`,
  `skills/in-progress/` y `skills/deprecated/` que el instalador no trae.
- **Re-instalación hoy:** `npx skills@latest add mattpocock/skills -a opencode`
  falla en esta máquina con `spawn git ENOENT` (el instalador clona con git y
  **git no está instalado**). El set en disco está completo y es reciente
  (2026-10-09), por lo que no es bloqueante; para actualizar: instalar git y
  relanzar el instalador.
- Deps de tracker: implement, implement-spec, to-spec, to-tickets, triage y
  wayfinder asumen un issue tracker configurado (`setup-matt-pocock-skills`;
  variantes GitHub/GitLab/local). Sin git instalado, la ruta útil es la local.

## Engram (MCP)

Herramientas verificadas (catálogo del plugin en esta sesión): `mem_save`,
`mem_search` (FTS5; scope de proyecto por defecto; `all_projects` opt-in),
`mem_context`, `mem_save_prompt`, `mem_session_summary`, `mem_get_observation`,
`mem_suggest_topic_key`, `mem_update`, `mem_delete`, `mem_stats`, `mem_timeline`,
`mem_session_start/end`, `mem_capture_passive`, `mem_doctor`, `mem_pin/unpin`,
`mem_judge`, `mem_compare`, `mem_current_project`, `mem_merge_projects`.

Detalles que condicionan el diseño:
- `mem_save` puede devolver `judgment_required` con `candidates[]` +
  `judgment_id` → protocolo `mem_judge` (veredicto con relation: related/
  compatible/scoped/conflicts_with/supersedes/not_conflict). Para
  `supersedes`/`conflicts_with` sobre decision/architecture/policy: preguntar al
  usuario primero (regla implementada en harness-core §9).
- Tipos válidos de observación: decision, architecture, bugfix, pattern, config,
  discovery, learning (default manual). `topic_key` permite upsert (evita duplicados).
  HYPOTHESIS no es type: se marca con prefijo `[HYPOTHESIS]` en el título.
- El proyecto se detecta por nombre de directorio (o git remote si hubiere).

## Limitaciones detectadas del entorno

1. **`git` ausente** (verificado: no en PATH ni en ubicaciones estándar). El
   directorio conserva el `.git` de un proyecto anterior distinto (harness externo
   runtime, ya descartado; historial sin tocar) cuyo working tree se vació.
   Consecuencias: `git diff/log/build gates` → UNVERIFIED; `pr`, `triage` con
   tracker remoto → degradados; proyecto Engram se llama `apexharness` por
   basename. Recomendación: `winget install Git.Git` y relanzar el instalador.
2. **Cursor no instalado** en esta máquina (`~/.cursor` inexistente). Puerta de
   portabilidad y mapeo propuesta: `docs/CURSOR.md`. No se implementó el adapter.
3. **Tokens**: OpenCode no expone al agente un contador de tokens de su propio
   turno. Las métricas de tokens se capturan del panel del TUI
   (`tokensTui`) o vía API de sesiones; automatización completa vía plugin → roadmap.
4. El plugin global Engram inyecta su propio protocolo de memoria (más agresivo
   que el Memory Router del harness). En este repo, las reglas de harness-core
   refinan el mínimo: gate + máx 2 búsquedas + escritor único. No se edita el
   plugin global (propiedad del usuario, compartida por otros proyectos).
5. REA (MCP de reverse-engineering) está disponible pero fuera del alcance del
   MVP: no se ruta hacia él.

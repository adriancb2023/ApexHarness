# ApexHarness — Engineering Agent Harness para OpenCode (portable a Cursor)

**Autor y propietario:** Adrián Cruz Barranco

Capa de orquestación de **agentes, skills, memoria, contexto, verificación y
políticas** para **OpenCode** y **Cursor**. Sin runtime externo propio: el host
ejecuta; este repo aporta la coordinación (`.opencode/` + `.cursor/`).

**Dependencia externa (no incluida en el repo):** [Skills for Real Engineers](https://github.com/mattpocock/skills) (`mattpocock/skills`). El harness solo las **rutea** por ID.

```text
                    TAREA (texto o /harness)
                           │
                    ORCHESTRATOR  ← agente `Apex_Harness` (primary)
                           │  · clasifica (tabla determinista)
                           │  · gate de memoria (Engram, ≤2 búsquedas)
                           │  · elige 2–4 skills + skills descartadas
                           │  · handoff compacto
              ┌────────────┼────────────┐
              ▼            ▼            ▼
           AGENT DEV    AGENT BUG    VERIFIER   ← Apex_Dev / Apex_Bug / Apex_Verifier
        (implementa) (diagnostica) (verifica, read-only)
              │            │            │
              ▼            ▼            ▼
        Skills mattpocock (carga perezosa por ID, registry en harness-core)
              │
        REPAIR ← evidencia FAIL (máx 2 ciclos)
              │
              ▼
   MEMORY WRITER (Engram, upsert por topic_key) ──► .harness/{state,cache}.md + metrics.jsonl
              │
              ▼
        COMPLETED (solo con evidencia) | UNVERIFIED | BLOCKED
```

## Qué NO es

- No es un runtime externo (nada de Node/Python/CLI que ejecutar).
- No sustituye a OpenCode; lo coordina.
- No re-implementa las skills de Matt Pocock: las **compone y las rutear** — carga por ID, tablas de decisión, verificación.
- No es un prompt gigante: la inteligencia está en tablas pequeñas con reglas
  de carga/descarte, no en volumen de contexto.

## Componentes → mecanismo nativo

| Componente | Implementación | Mecanismo |
| --- | --- | --- |
| Orchestrator | `.opencode/agents/Apex_Harness.md` (primary, `default_agent`) | solo edita `.harness/*`; delega el resto |
| Agentes DEV / BUG | `.opencode/agents/Apex_Dev.md` / `Apex_Bug.md` (subagent) | contexto fresco; `question`/`subagent` denegados |
| Verificación independiente | `.opencode/agents/Apex_Verifier.md` (subagent) | `edit` DENEGADO por permisos |
| Skill Registry + routing | `.opencode/skills/harness-core/SKILL.md` (+ `references/registry.md`) | skill; carga bajo demanda |
| Memory Router/Writer | reglas en harness-core §3/§9 | MCP Engram (`mem_*`), upsert con `topic_key` |
| Estado del pipeline | `.harness/state.md` (máquina de estados visible) | fichero; único escritor: Orchestrator |
| Verification cache | `.harness/cache.md` | invalidación por inputs editados |
| Políticas | `opencode.json` (`permissions[]` + `policies[]`) hard-deny de `git push --force`, `git reset --hard`, borrados destructivos; explicada en `policies/SAFETY.md` | enforcement del host |
| Métricas | `.harness/metrics.jsonl` | A/B con/sin memoria → `docs/METRICS.md` |
| Entrada explícita | `.opencode/commands/harness.md` → `/harness <tarea>` | comando con `agent: Apex_Harness` |
| Cursor (nativo) | `.cursor/rules`, `.cursor/commands/harness.md`, shim `harness-core`, `mcp.json` | ver `docs/CURSOR.md` |

## Uso

0. **Skills Matt (obligatorio, una vez por máquina/proyecto):** no vienen en el clone;
   viven en `.opencode/skills/` y `.cursor/skills/` (gitignored salvo `harness-core`).
   ```bash
   npx skills@latest add mattpocock/skills -a opencode -a cursor -y --copy
   ```
   Requiere `git`. Sin git, con set global ya instalado:
   `pwsh ./scripts/bootstrap-matt-skills.ps1 -FromOpenCodeGlobal` (ambos hosts).
1. Abre este repo en OpenCode (v2) o Cursor. En OpenCode el default es `Apex_Harness`; en Cursor aplica la regla `apex-harness`.
2. Habla normal o usa `/harness <tarea>`. Ejemplos:

   ```text
   /harness Añade búsqueda de propuestas al dashboard          (dev, estándar)
   /harness Al subir un PDF el dashboard se queda cargando     (bug)
   /harness ¿Por qué el routing descarta research aquí?        (respuesta directa)
   ```

3. Lo que verás: `Apex_Harness` carga `harness-core`, clasifica, consulta Engram solo
   si el gate justifica, lanza `Apex_Dev`/`Apex_Bug` con handoff compacto, y cierra con
   `Apex_Verifier` → veredicto + métricas + memoria actualizada.

Agentes concretos disponibles: `Apex_Harness`, `Apex_Dev`, `Apex_Bug`,
`Apex_Verifier` (más los built-in de OpenCode: `build`, `plan`, `general`,
`explore`).
Si quieres trabajo manual sin protocolo, cambia de agente en el TUI.

## Validación del MVP (receta)

Abrir una sesión limpia y correr cada tarea; observar en qué NO se mete:

1. **Trivial** — `/harness Añade una cabecera de comentario a AGENTS.md enumerando los agentes`
   → esperado: sin research/grill/spec/tickets, edit vía `Apex_Dev`, verificación leve,
   COMPLETED con evidencia.
2. **Estándar** — una feature pequeña real del repo de destino
   → esperado: memory gate, `tdd`, `code-review`, `Apex_Verifier` PASS antes de DONE.
3. **Bug** — `/harness Al ejecutar <comando> falla <exactamente esto>`
   → esperado: el agente `Apex_Bug` recorre su ruta completa antes de tocar código
   (reproduce → minimiza → hipótesis → confirma), fix + regression test,
   `Apex_Verifier` con repro.

Criterio de validación del pipeline: en state.md y metrics.jsonl quedan
clasificación, skills elegidas/descartadas, consultas de memoria y veredictos —
si algo es incorrecto, corregir las tablas de `harness-core` (no el agente).

## Instalación en otro repo (un solo harness garantizado)

**Paso 1 — harness (este repo):**

- OpenCode: los 4 `Apex_*.md` → `.opencode/agents/`; `harness-core` →
  `.opencode/skills/`; comando → `.opencode/commands/`; en `opencode.json`
  **fusión** (merge): `default_agent: "Apex_Harness"` + `policies[]` + ask de
  `git clean`.
- Cursor: copia también `.cursor/` (rules, commands, `skills/harness-core`,
  `mcp.json`). Detalle: **docs/CURSOR.md**.

**Paso 2 — Skills for Real Engineers (obligatorio, no están en el repo):**

```bash
npx skills@latest add mattpocock/skills -a opencode -a cursor -y --copy
# o, sin git:
pwsh ./scripts/bootstrap-matt-skills.ps1 -FromOpenCodeGlobal
```

Quedan en el proyecto: `.opencode/skills/<id>/` y `.cursor/skills/<id>/` (no se
versionan). Sin este paso el router apunta a IDs (`tdd`, `code-review`, …) que no
existen. Procedimiento completo: **harness-core §12**.

Por qué no se mezclan dos harnesses: (1) IDs namespaced (`Apex_*`, `harness-core`,
`/harness`) — no colisionan con agentes/skills ajenos; (2) `default_agent` del
proyecto pisa el global, así que la sesión abre siempre como Apex_Harness; (3)
el #spawn# de Apex_Harness está en #allowlist# (deny `*` → allow solo
Apex_Dev/Apex_Bug/Apex_Verifier): un `apex` u otro agente global ni siquiera
aparece en su catálogo de tareas; (4) `policies[]` hard-deny manda en cualquier
capa. Si el repo destino tenía un harness viejo (agentes sin prefijo), desactívalo
con `"agent": {"harness": {"disable": true}}` o borrando/renombrando sus ficheros.
En Cursor: una sola pareja `apex-harness` + `apex-roles`; borra reglas rivales.

## Estructura

```text
AGENTS.md                reglas del proyecto (inyectadas por OpenCode)
opencode.json            default_agent + permissions/policies (hard-deny)
policies/SAFETY.md       explicación de las políticas y cómo endurecerlas
.opencode/agents/*.md    Apex_Harness, Apex_Dev, Apex_Bug, Apex_Verifier
.opencode/commands/      /harness
.opencode/skills/harness-core/   SKILL.md (routing/memoria/estados/DoD) + references/registry.md
.cursor/rules/           apex-harness.mdc + apex-roles.mdc (alwaysApply)
.cursor/agents/          apex-harness, apex-dev, apex-bug, apex-verifier
.cursor/commands/        /harness (Cursor)
.cursor/skills/harness-core/  shim → canónico en .opencode/...
.cursor/mcp.json         Engram local
scripts/install-cursor-harness.ps1   instala/repara harness en Cursor
scripts/bootstrap-matt-skills.ps1    fallback sin git → .opencode/skills + .cursor/skills
.harness/                state.md, cache.md, metrics.jsonl (runtime, por tarea)
docs/CAPABILITIES.md     qué se inspeccionó de OpenCode/skills/Engram y qué limita
docs/METRICS.md          protocolo de medición y A/B de Engram
docs/CURSOR.md           port Cursor (implementado) + paso skills Matt
```

## Estado del MVP y roadmap

MVP incluido (todo config/markdown, cero código): Orchestrator → AUTO/DEV/BUG →
skill router → Engram → implementación → verificación → memory writer, con
policies hard-deny, state machine documental, verification cache y métricas.

Siguiente capa (por validar el MVP): presupuesto adaptativo por complejidad,
agentes en paralelo (worktrees), grafo de tickets (`to-tickets` nativo), hook de
plugin que escriba `metrics.jsonl` automáticamente, allowlists estrechas de shell
por agente, tracker local para las skills con `requires/issues`.

## Limitaciones de entorno conocidas (ver docs/CAPABILITIES.md)

- `git` NO está instalado: checks `git diff/log` salen UNVERIFIED y `pr` se
  descarta; el instalador oficial de skills falla (`spawn git ENOENT`).
  Desbloqueo: `winget install Git.Git`. Fallback skills (ambos hosts):
  `scripts/bootstrap-matt-skills.ps1 -FromOpenCodeGlobal`.
- Port Cursor: implementado en `.cursor/` (ver `docs/CURSOR.md`).
- Tokens por fase no automatizados en el MVP (se capturan del TUI).

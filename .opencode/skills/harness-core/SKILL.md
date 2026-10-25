---
name: harness-core
description: Core del Engineering Harness — tablas de clasificación de tareas, routing de skills y agentes, reglas de memoria Engram, máquina de estados, handoffs, verificación y Definition of Done. Cárgalo al empezar cualquier tarea y aplica sus tablas sin re-decidir.
---

# Harness Core

Fuente de verdad del pipeline. Si una decisión está aquí, aplícala tal cual y
anota solo el porqué en una línea. Metadatos completos de cada skill (triggers,
requires, produces, verificación, cuándo NO cargarla): `references/registry.md`,
solo cuando tengas duda sobre una skill concreta.

Reglas de tokens: este documento es el presupuesto orientativo completo (~2k
tokens); no lo vuelvas a imprimir en el chat; cita secciones por §.

## 1. Clasificación de tareas (determinista)

Escanea el texto de la tarea con la tabla; primera coincidencia gana.

| Gatillos | Agente / pipeline |
| --- | --- |
| `bug`, `error`, `crash`, `exception`, `fails`, `broken`, `regression`, "no funciona", "falla", "se queda", "no carga", "rompe", "petazo", "stack trace", "se cuelga" | **BUG** (subagente Apex_Bug) |
| `implement`, `add`, `create`, `build`, `feature`, `develop`, `refactor`, `migrate`, "añade", "agrega", "implementa", "crea", "nueva versión de", "soporte para" | **DEV** (subagente Apex_Dev) |
| Análisis, explicación, exploración, preguntas, planes, revisión de un punto concreto | **Answer directo** del Orchestrator, sin spawn |

Ambigua → razona el porqué en una línea y elige; sigue en duda → pipeline estándar
(§2). Si la tabla no resolvió y usaste el modelo para decidir, anótalo en state.md.

Tareas no-código (docs, config del harness, meta-tareas del propio repo) se
tratan como DEV/Answer según su forma. Si la tarea toca el propio harness, recuerda:
el Orchestrator solo puede editar `.harness/**`; los cambios al resto de archivos
los ejecuta Apex_Dev (el agente con permiso de edit real).

## 2. Complejidad → variante de pipeline

| Nivel | Señal | Pipeline |
| --- | --- | --- |
| Trivial | ≤1 archivo, ≤~30 LOC, sin interfaz nueva ni dominio nuevo | memory (gate) → Apex_Dev → verify leve (salida del implementador) → memory-write → DONE |
| Estándar | 2–4 archivos o tests afectados | classify → memory → route → Apex_Dev (+`tdd`) → `code-review` → Apex_Verifier → memory-write → DONE |
| Compleja | dominio nuevo, interfaz nueva, multi-sistema, incertidumbre grande | research (si hay incertidumbre factual) → grill-with-docs → to-spec → to-tickets → implement-spec por ticket → tdd → code-review → Apex_Verifier → retro (opcional) → memory-write → DONE |

Cada paso opcional (research, grill, spec, tickets, retro) se incluye solo con
valor: cuando lo saltes, una línea dice por qué. El conteo típico es 2–4 skills
por tarea; un número mayor exige justificación explícita.

## 3. Memory Router (Engram)

**Gate (antes de buscar, coste 0):** ¿la tarea podría repetir trabajo previo,
heredar una decisión, o tocar un bug/convención ya conocido? No → cero búsquedas;
anota "memory skip: gate no aplicable". Sí → cadena:

1. `mem_context` — barato, una vez.
2. `mem_search` — keywords de tema/archivos (máx 2 búsquedas; scope de proyecto
   por defecto: otros proyectos quedan excluidos automáticamente).
3. `mem_get_observation` — solo para los 1–2 resultados que inyectarás.

**Cap:** ≤5 observaciones relevantes en contexto. Descarta observaciones
triviales/otro-área/sin relación con la tarea.

| Tipo de memoria | Regla |
| --- | --- |
| decision / architecture | Aplicable a la tarea → inyecta. Si contradice el código: investiga; git/código manda; no la cambies silenciosamente |
| bugfix | Área similar → inyecta causa+fix. Si no → descarta |
| pattern / config | Inyecta si toca el área |
| Progreso | Punto de partida; git/código manda si difieren |
| `learning` con título `[HYPOTHESIS]` | Nunca como hecho; úsala solo para señalar incertidumbre |

**Contradicciones:** tests/evidencia > código actual > Engram > suposiciones del
agente. Si Engram difiere del código: investiga y resuelve, y luego registra el
veredicto (§9). Nunca adoptes una memoria sin verificarla contra el código actual.

## 4. Contexto mínimo

Nunca el repo entero. Orden: memoria relevante → archivos/símbolos implicados
(lectura dirigida / grep) → tests alrededor → implementación. Si con 3 archivos se
responde, no leas 10. Skills y contextos fuera de la tarea no se cargan.

## 5. Skill Router

Regla: `¿esta skill aporta valor a ESTA tarea?` no → no se carga (anótalo).
Detalles por skill: `references/registry.md`.

| Necesidad | Skill | Carga si | Skip si |
| --- | --- | --- | --- |
| Bug | `diagnosing-bugs` | SIEMPRE en pipeline BUG | — |
| Implementar | `tdd` | slice testable posible | no hay runtime/tests o es doc/config |
| Handoff con spec/ticket | `implement-spec` | pipeline viene de to-spec/to-tickets | spec informal |
| Cambio grande | `code-review` | >1 archivo o feature completa | cambio de ≤30 LOC bien cubierto por verify |
| Interfaz/arquitectura | `codebase-design` | cambia forma/interfaz de módulo | solo retocar |
| Conceptos de dominio | `domain-modeling` | conceptos nuevos/ambiguos | dominio conocido y estable |
| Incertidumbre factual | `research` | tecnología/dependencia/API desconocida que BLOQUEA | el dato está en código/docs locales |
| Compleja y ambigua | `grill-with-docs` | pipeline compleja | trivial/estándar |
| Compleja multi-paso | `to-spec` → `to-tickets` | se va a implementar en varios tickets | no caben tickets |
| Cierre de compleja | `retro` | aprendizaje de proceso relevante | estándar/trivial |

Nota: `implement`, `to-spec`, `to-tickets`, `retro`, `triage`, `wayfinder`,
`grill-with-docs` son user-invoked (`disable-model-invocation: true`): NO aparecen
anunciadas; llámalas por ID exacto con la herramienta `skill` cuando el routing las
elija. Las model-invoked (`tdd`, `code-review`, `diagnosing-bugs`, `research`,
`codebase-design`, `domain-modeling`, `prototype`, `pr`) se anuncian solas, pero la
decisión de cargarlas es igual de explícita.

## 6. Máquina de estados y artefactos

Estados: `RECEIVED CLASSIFYING MEMORY_LOOKUP PLANNING RESEARCHING IMPLEMENTING
DIAGNOSING VERIFYING REVIEWING REPAIRING COMPLETED FAILED BLOCKED UNVERIFIED`.

`.harness/state.md` (≤40 líneas; el Orchestrator actualiza en cada salto):

```markdown
# Harness state — 2026-10-25 hh:mm
task: <1 línea>
pipeline: dev | bug | answer
state: VERIFYING (prev: IMPLEMENTING)
selected: agent=Apex_Dev skills=[tdd, code-review] dropped=[research (dato local), grill (estándar)]
memory: gate=hit ids=[12, 34] injected=2 est_tokens=~600
transitions:
| hh:mm | IMPLEMENTING → VERIFYING | implementación terminada | evidence se va a Apex_Verifier |
...
```

Cada transición con from → to, reason, evidence y (si disponible) tokens. Los
subagentes no escriben state.md; el Orchestrator es el único escritor.

## 7. Verificación y cache

1. Evidencia: por cada check, comando ejecutado + salida (resumen). Nunca aserción.
2. Verificación de no-trivial es independiente: la hace el subagente Apex_Verifier
   (read-only por permisos). Trivial: la salida del implementador con comandos
   adjuntos, revisada por el Orchestrator.
3. Checks típicos: tests del área, suite completa, typecheck, lint, build,
   reproducción del bug, `git diff`/`git log` (si hay git; si no: UNVERIFIED para
   ese check concreto, no para la tarea).
4. Cache (`.harness/cache.md`): `| check | comando | inputs (files+hash/mtime) |
   result | ts |`. Un test que ya pasó sin cambios de código → no se repite.
   Cualquier edit en los inputs → check invalidado.

FAIL → REPAIRING (máx 2 ciclos; handoff con evidencia de lo malo) → re-verify SOLO
lo invalidado. Pasado el límite: UNVERIFIED o BLOCKED con lo aprendido registrado.

## 8. Handoff entre agentes (compacto; nunca la conversación entera)

```markdown
from: Apex_Harness | to: Apex_Dev | type: implement-request | 2026-10-25
objetivo: <1–2 líneas>
contexto: <archivos, símbolos, criterios; sin volcados>
memory: [#12 decisión X, #34 bug Y con su fix]  (líneas exigidas)
criteria: <qué debe demostrar Apex_Verifier>
relevantMemoryIds: [12, 34]
```

Variantes: `repair-request` (con rootCause/evidence para Apex_Dev) y `verify-request`
(para Apex_Verifier con la lista de checks). Si un resultado vuelve insuficiente, el
siguiente handoff incluye solo el delta necesario.

## 9. Memory Writer (solo al cerrar; escritor único: Orchestrator)

```
¿Hay conocimiento reutilizable? NO → no guardar (el silencio es válido)
SÍ → ¿existe memoria similar del tema? SÍ → mem_save con el mismo topic_key (upsert) / mem_update con id
                                   NO → mem_save nuevo
```

**Guardar:** decisiones y su why; arquitectura establecida; causa raíz de bugs
(qué era, fix, test, cómo reproducir en una línea); convenciones; config/entorno;
hito de progreso (1 observación por fila); referencia a ficheros clave.

**No guardar:** logs, diffs completos, código completo, conversaciones, pasos
triviales, pensamientos internos, cada comando ejecutado.

Formato nativo: `title` corta buscable; `type` topical (decision / architecture /
bugfix / pattern / config / discovery / learning); `content` con
**What / Why / Where / Learned**; `topic_key` estable (si dudas:
`mem_suggest_topic_key`). Hipótesis pendiente → título con prefijo `[HYPOTHESIS]`.

Post-save: si la respuesta trae `judgment_required`, itera `candidates[]` y llama
`mem_judge` con el `judgment_id` de CADA candidato. `supersedes`/`conflicts_with`
sobre decision/architecture/policy → preguntar al usuario antes; el resto se
resuelve en silencio. Nunca duplicar memoria: antes de crear, busca tema; el
criterio default es upsert.

Cierre de sesión: `mem_session_summary` (Goal / Instructions / Discoveries /
Accomplished / Next Steps / Relevant Files — formato del plugin Engram).

## 10. Métricas (`.harness/metrics.jsonl`)

Una línea JSON por tarea al cerrar:

```json
{"ts":"2026-10-25T10:34:31","task":"...","pipeline":"dev","agents":["Apex_Dev","Apex_Verifier"],
 "skillsUsed":["tdd","code-review"],"skillsSkipped":["research (dato local)"],
 "memoryQueries":1,"memoryResults":2,"contextFiles":3,"verification":{"checks":3,"pass":3},
 "retryCount":0,"finalState":"COMPLETED","tokensTui":null}
```

`tokensTui`: el número real del panel de tokens del TUI (lo anota el Orchestrator
si lo tiene a mano; `null` si no). Para responder "¿Engram ahorra tokens?":
ejecuta la misma tarea dos veces (una con lookup de memoria, otra marcando
"memory skip") en sesiones limpias y compara tokens/steps/reintentos de ambas líneas
del JSONL. Protocolo completo: `docs/METRICS.md`.

## 11. Anti-patterns (abortar si te pilla)

1. Prompt gigante: todas las skills + todo el repo + todo Engram a la vez.
2. Pipeline rígido: ejecutar research/grill/spec/tickets cuando la tarea es trivial.
3. `mem_search` "por si acaso" sin gate.
4. PASS por aserción del implementador sin comando ejecutado.
5. Reescribir/repasando trabajo ya verificado cuando nada cambió.
6. Un agente que hace todo (planifica, codifica, diagnostica, revisa) — usa los roles.

## 12. Aislamiento e instalación: solo un harness manda

En cualquier repo con este harness instalado, el único pipeline activo es el de
`Apex_*`. Instalación (config-only, todo se puede copiar a mano):

| Pieza | Destino (por defecto: proyecto) | Conflicto con harness/agentes previos |
| --- | --- | --- |
| 4 ficheros `Apex_*.md` | `<repo>/.opencode/agents/` | Los IDs `Apex_*` no chocan con agentes ajenos: coexisten y no se invocan entre sí. Si el repo ya tenía `harness.md`/`dev.md`/`bug.md`/`verifier.md` SIN prefijo (otro harness), desactívalos: borra/renombra esos ficheros o añade `disable: true` para cada uno en `opencode.json` (`"agent": {"harness": {"disable": true}, ...}`) |
| `harness-core` | `<repo>/.opencode/skills/harness-core/` | Los IDs de skill deben ser únicos entre ubicaciones: si ya existe `harness-core` en `~/.config/opencode/skills/` (versión vieja), bórrala del global |
| comando `/harness` | `<repo>/.opencode/commands/harness.md` | Si existía otro comando con ese ID, lo reemplaza (mismo path) |
| `opencode.json` | `<repo>/opencode.json` — MERGE, no sustituir | Añade `default_agent: "Apex_Harness"`, `policies[]` hard-deny y `permission: {"git clean -d*": "ask"}`; conserva lo demás del repo |
| reglas | Si el repo ya tiene `AGENTS.md`: añade un bloque `## Harness (Apex_)` al final (no lo sustituyas). Alternativa sin tocar AGENTS.md: en `opencode.json`, `instructions: [".opencode/skills/harness-core/SKILL.md"]` |

Garantías duras (aplicadas por el HOST, no por prompts):

1. `policies[]` hard-deny se aplica en cualquier capa; ninguna config o agentes
   Ranking pueden saltarla (docs: OpenCode 2).
2. `subagent` de Apex_Harness: deny `*` → allow SOLO `Apex_Dev`/`Apex_Bug`/
   `Apex_Verifier`. Con `deny`, los demás agentes (p. ej. un `apex` global,
   `build`, `general`) **desaparecen del catálogo de spawn** del Orchestrator:
   no hay ruta de escape por la que se cuele otro harness dentro de la pipeline.
3. `default_agent` a nivel proyecto pisa el global → la sesión abre SIEMPRE como
   Apex_Harness aunque el global diga otra cosa; y si el global no existe, el
   proyecto lo fija.
4. Nombres namespaced (`Apex_*`, `harness-core`, `/harness`) → cero colisión
   accidental con agentes/skills de Matt Pocock o de terceros.

Instalación global (todos los repos): mismo contenido en `~/.config/opencode/`
(agents/skills/commands) y `default_agent` + `policies[]` en el config global.
Un proyecto que defina su propio `default_agent` pisará el global (decisión
consciente, nuestra config se respeta en el resto de keys). Los 27 skills de
Matt son el SUELO compartido (globales, sin duplicar: los 2 harness los usan hijo
de lo mismo); lo namespaced no se mezcla. Cursor: ver docs/CURSOR.md (reglas
namespaced; borra las reglas de un harness anterior para evitar dos salidas al mismo paso).

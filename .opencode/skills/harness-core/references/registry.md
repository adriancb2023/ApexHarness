# Skill Registry — metadatos del harness

Base de verificación real: `~/.config/opencode/skills/` (27 skills instaladas por el
instalador oficial `npx skills add mattpocock/skills -a opencode`, set completo
`engineering/` 20 + `productivity/` 7; comparado con el árbol del repo oficial el
2026-10-25). Los IDs son los de directorio; cada uno vive como `skills/<id>/SKILL.md`.

Convenciones:
- **user-invoked** (`disable-model-invocation: true`): el modelo NO la ve anunciada;
  hay que cargarla por ID exacto con la herramienta `skill`.
- **model-invoked**: se anuncia sola; la decisión de cargarla sigue siendo explícita.
- `requires/issues`: la skill asume un issue tracker configurado por
  `setup-matt-pocock-skills` (GitHub/GitLab/local). Sin git, usar la variante local.

## 1. Flow — implementación (user-invoked)

```yaml
implement:
  type: user-invoked
  agents: [Apex_Dev]
  purpose: implementar el trabajo de un spec o un set de tickets
  triggers: [handoff con spec, ticket registrado, tracer bullet]
  requires: [spec o tickets, relevant-code-context]
  produces: [code-change, commit]
  verification: [typecheck, tests por módulo, suite al final, code-review]
  notes: llama a tdd en las seams pactadas y code-review al final
implement-spec:
  type: user-invoked
  agents: [Apex_Dev]
  purpose: implementar el output de to-spec + to-tickets
  triggers: [spec nuevo, bloque de tickets listo]
  requires: [spec publicado, relevant-code-context]
  produces: [code-change]
  verification: [tests, code-review, diff]
```

## 2. Flow — planificación (user-invoked)

```yaml
grill-with-docs:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: entrevista que afina un plan y deja ADRs + glosario como side effect
  triggers: [tarea compleja/ambigua, diseño nuevo, alineación con el dominio]
  requires: [usuario disponible para responder]
  produces: [plan afinado, ADRs, GLOSSARY.md]
  verification: [respuestas registradas, docs escritos]
grill-me:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: entrevista de afinamiento sin docs
  load-when: compleja pero el dominio ya está modelado
to-spec:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: sintetizar la conversación actual en un spec publicado
  triggers: [pipeline compleja aprobado, plan estable]
  produces: [spec publicado]
  verification: [spec revisado por el usuario]
  requires/issues: tracker configurado
to-tickets:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: partir plan/spec en tracer-bullet tickets con edges de bloqueo
  produces: [tickets con dependencias]
  verification: [grafo de bloqueos sin ciclos]
  requires/issues: tracker configurado (o variante local)
retro:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: retrospectiva de sesión de coding
  load-when: cierre de pipeline compleja o petición del usuario
triage:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: mover issues/PRs externos por una state machine de triage con briefs agent-ready
  load-when: el usuario pide triage/issues, no como paso interno de una tarea
  requires/issues: tracker configurado
wayfinder:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: plan de trabajo enorme como mapa de tickets de decisión, resueltos de a uno
  load-when: el trabajo no cabe en una sesión
  requires/issues: tracker configurado
improve-codebase-architecture:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: escaneo de oportunidades de deepening reportadas en HTML + grill del elegido
  load-when: petición explícita de mejora arquitectónica
setup-matt-pocock-skills:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: configurar tracker, labels y layout de docs del repo; correr una vez
  load-when: primer uso de las skills con tracker en un repo nuevo
```

## 3. Model-invoked — disciplina

```yaml
tdd:
  type: model-invoked
  agents: [Apex_Dev, Apex_Bug]
  purpose: red-green-refactor por slices verticales en las seams
  triggers: [feature, fix, cambio con slice testable]
  requires: [test framework del repo, relevant-code-context]
  produces: [test failing → green, code-change]
  verification: [test suite, el test cubre el comportamiento nuevo]
diagnosing-bugs:
  type: model-invoked
  agents: [bug]
  purpose: loop de diagnóstico para bugs duros y regresiones de performance
  triggers: [bug, error, crash, regression, "no funciona", lentitud inexplicable]
  requires: [reproducción]
  produces: [root-cause con evidencia, fix mínimo]
  verification: [repro antes, repro después, regression test]
  notes: SIEMPRE en pipeline BUG; nada de fix sin causa confirmada
code-review:
  type: model-invoked
  agents: [Apex_Dev, Apex_Bug, Apex_Harness]
  purpose: review 2 ejes — Standards (repo) y Spec (issue origen) en subagentes paralelos
  triggers: [antes de commit/PR, diff posterior a implement]
  requires: [punto fijo (commit/branch/tag) o diff]
  produces: [findings por severidad con file:line]
  verification: [los findings se cierran antes de pasar a COMPLETED]
  skip-when: cambio ≤30 LOC ya cubierto por la verificación directa
research:
  type: model-invoked
  agents: [Apex_Harness, Apex_Dev, Apex_Bug]
  purpose: investigar contra fuentes primarias de confianza y escribir findings en el repo
  triggers: [tecnología/dependencia/API desconocida, falta información factual que BLOQUEA]
  requires: [pregunta acotada]
  produces: [findings markdown]
  verification: [fuentes citadas; sin fuentes no hay conclusión]
  skip-when: el dato está en código, docs locales o Engram validado
codebase-design:
  type: model-invoked
  agents: [Apex_Dev, Apex_Harness]
  purpose: vocabulario de deep modules — interfaces pequeñas, seams, testabilidad
  triggers: [cambio que altera forma/interfaz de un módulo]
  produces: [diseño de módulo, decisiones de seam]
domain-modeling:
  type: model-invoked
  agents: [Apex_Dev, Apex_Harness]
  purpose: construir/afinar el modelo de dominio — GLOSSARY.md y ADRs
  triggers: [conceptos nuevos/ambiguos, registro de decisiones de dominio]
  produces: [GLOSSARY.md, ADRs]
prototype:
  type: model-invoked
  agents: [Apex_Harness]
  purpose: prototipo desechable para responder una pregunta de diseño
  load-when: duda de diseño que un código desechable resuelve más rápido que teorizar
pr:
  type: model-invoked
  agents: [Apex_Harness]
  purpose: cuerpo del PR
  requires: [git + remote; git no está disponible en esta máquina → skip]
wizard:
  type: model-invoked
  agents: [Apex_Harness]
  purpose: asistente bash interactivo para pasos que solo un humano puede hacer
  load-when: provisioning/credenciales/dashboards externos/migraciones manuales
grilling:
  type: model-invoked
  agents: [Apex_Harness]
  purpose: grill del usuario sobre un plan/decisión (variante model-invoked)
  load-when: el usuario pide stress-test explícito
```

## 4. Productividad (support)

```yaml
handoff:
  type: model-invoked
  purpose: compactar la conversación actual en un documento de handoff
  notes: alinea con §8 del SKILL.md del harness (contratos compactos); el formato
    base es el de esta skill alineado con el contrato del harness
writing-for-agents:
  type: model-invoked
  purpose: redactar docs para agentes (skills, AGENTS.md)
  load-when: MANTIENES el propio harness (editando skills/agents del repo)
ask-matt:
  type: user-invoked
  purpose: router meta sobre el repositorio de skills
  load-when: la petición no encaja en ninguna otra tabla
teach: {type: user-invoked, purpose: enseñar un concepto en el workspace, load-when: petición de enseñanza}
to-questionnaire: {type: user-invoked, purpose: convertir una decisión no respondible en cuestionario, load-when: hay terceros que deben responder}
wait-what: {type: user-invoked, purpose: re-pitch de un mensaje que no aterrizó, load-when: repetición de comunicación}
```

## 5. Composiciones canónicas (agentes)

```yaml
auto: # = Apex_Harness (Orchestrator) + composición adaptativa con Apex_Dev
  core: [implement-spec|implement, tdd, code-review]
  optional: [research, grill-with-docs, to-spec, to-tickets, retro,
             domain-modeling, codebase-design, wayfinder]
  flow-trivial: [memory(0-1) → Apex_Dev → verify] # sin research/grill/spec/tickets/retro
Apex_Dev:
  core: [implement*, tdd, code-review, codebase-design, domain-modeling]
  optional: [research, implement-spec]
  evita: arquitectura completa cuando la tarea no la requiere
Apex_Bug:
  core: [diagnosing-bugs, tdd, code-review]
  optional: [research, codebase-design, domain-modeling]
  nunca: código antes de causa raíz confirmada
Apex_Verifier: # subagente independiente, read-only
  core: [ejecutar los checks del handoff verify-request]
  skill-loading: no suele necesitar skills del repo
```

## 6. Agentes OpenCode del harness (`.opencode/agents/`)

| ID | modo | permiso clave | propósito |
| --- | --- | --- | --- |
| `Apex_Harness` | primary | edit solo en `.harness/*` | clasificar/rutear/coordinar/memoria/verificación |
| `Apex_Dev` | subagent | subagent/question denegados | implementación con verificación propia |
| `Apex_Bug` | subagent | subagent/question denegados | diagnóstico de causa raíz con evidencia |
| `Apex_Verifier` | subagent | edit DENEGADO | verificación independiente con veredicto |

Mantener este registry actualizado cuando cambie el set de skills (re-instalar,
añadir o deprecarse una). La fuente de verdad son los ficheros en disco, no la
documentación; si un ID no existe en disco, no se ruta hacia él.

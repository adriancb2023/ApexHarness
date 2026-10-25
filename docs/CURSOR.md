# Portabilidad a Cursor (propuesta, sin implementar)

Cursor no está instalado en esta máquina (no existe `~/.cursor`), así que no se pudo
inspeccionar ni verificar qué soporta hoy. Esta nota es el mapa de portabilidad a
realizar cuando haya una instalación disponible; **se verifican las capacidades
reales antes de implementar nada** (regla del proyecto: no inventar APIs).

## Mapeo propuesto (por verificar cada punto contra docs.cursor.com)

| Componente del harness (OpenCode) | Cursor: candidato | Verificar con la instalación |
| --- | --- | --- |
| `AGENTS.md` (reglas del proyecto) | `.cursor/rules/*.mdc` (rules, always-apply) | formato de frontmatter actual |
| Skills de mattpocock en `~/.config/opencode/skills` | regla por skill o skills nativas si Cursor lo soporta | ¿existe SKILL.md/carga lazy en Cursor? |
| Agentes (`Apex_Harness`, `Apex_Dev`, `Apex_Bug`, `Apex_Verifier`) | sin sustituto directo confirmado | ¿subagents? ¿plans? ¿permission modes? |
| Comando `/harness` | `.cursor/commands` (si existe) o regla con frase disparadora | verificación |
| `opencode.json` policies (denegar git reset --hard, push --force...) | settings de permissions de Cursor / hooks | ¿deny/ask equivalentes? |
| MCP Engram | mismo protocolo MCP; misma config de server | config UI/JSON de Cursor |
| `.harness/state.md` artesanal | igual (ficheros marco) | — |

## Notas de portabilidad

- `harness-core` es markdown puro: su contenido puede reproducirse como reglas de
  Cursor casi 1:1 (tablas incluidas). Es el trasplante más sencillo.
- El trabajo de los subagentes en OpenCode se apoya en contexto fresco y en los
  permisos read-only del Apex_Verifier; si Cursor no tiene algo equivalente, esa
  separación se pierde y hay que compensar: verificación en otro chat/herramienta
  o una segunda pasada de revisión por el propio Orchestrator.
- Engram es independiente del host (MCP local vía `engram.exe`), así que la memoria
  persistente es portable tal cual.

### Un solo harness (repo con reglas previas)

En Cursor no hay IDs de agente: la única "fuente de verdad" es el fichero de
reglas. Para que no se mezclen dos harnesses: (1) un SOLO fichero namespaced
(p. ej. `.cursor/rules/apex-harness.mdc`) con `alwaysApply: true`; (2) borra o
vacía las reglas del harness anterior del repo — que no queden dos rutas para el
mismo paso; (3) si el repo se abre también en OpenCode, incluye esas reglas en
`opencode.json` con `instructions: [".cursor/rules/apex-harness.mdc"]` y evita
duplicar AGENTS.md. Las garantías duras (allowlist de subagentes, policies)
solo existen bajo OpenCode; en Cursor son reglas instruccionales (verificación
más blanda).

Plan realista de port: 1) abrir un repo piloto en Cursor, 2) crear una regla con
el contenido de harness-core, 3) configurar Engram MCP, 4) comprobar el
comportamiento con las 3 tareas de validación del README, 5) decidir si las
limitaciones de agent/subagent implican recortes.

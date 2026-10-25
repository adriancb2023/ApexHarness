# ApexHarness — reglas del proyecto

**Propietario:** Adrián Cruz Barranco

Este repositorio **es** el Engineering Agent Harness: una capa de orquestación
(Orchestrator, Skill Router, Memory Router/Writer, Verification, Policies) que vive
dentro de OpenCode y reutiliza sus mecanismos nativos. No hay runtime externo:
no Node, no CLI, no servicio. OpenCode sigue ejecutando todo; el harness da la
coordinación.

## Mapa

| Ruta | Rol |
| --- | --- |
| `.opencode/agents/Apex_Harness.md` | Orchestrator (agente primario). Clasifica, enruta, coordina, verifica, actualiza memoria. No codifica. |
| `.opencode/agents/Apex_Dev.md` | Agente DEV (subagente). Implementación con TDD. |
| `.opencode/agents/Apex_Bug.md` | Agente BUG (subagente). Diagnóstico con causa raíz probada. |
| `.opencode/agents/Apex_Verifier.md` | Verificación independiente (subagente read-only). |
| `.opencode/commands/harness.md` | `/harness <tarea>`: entrada explícita al protocolo completo. |
| `.opencode/skills/harness-core/` | Registro + tablas de routing, memoria, estados, verificación y DoD. Única fuente; cárgala al empezar cualquier tarea. |
| `opencode.json` | Políticas de permisos (referencia en `/docs/CAPABILITIES.md` y `policies/SAFETY.md`). |
| `.harness/` | Artefactos por tarea: `state.md`, `cache.md`, `metrics.jsonl`. |
| `docs/` | Hallazgos de capacidades, métricas, portabilidad a Cursor, metodologías. |

## Reglas universales (todos los agentes, en cualquier proyecto con este harness)

1. **Evidencia > aserción.** Nunca declares COMPLETED/PASS sin comando ejecutado y salida.
2. **Prioridad de fuentes:** tests/evidencia > código actual > Engram > supuestos.
   Una memoria que contradice el código se investiga; no se obedece.
3. **Skills bajo demanda:** carga solo lo que aporta valor a esta tarea (2–4 típicas);
   di en una línea qué descartas y por qué.
4. **Contexto mínimo:** archivos/símbolos implicados en la tarea, no el repo entero.
5. **Engram:** se consulta solo cuando hay un gate que lo justifique; se escribe solo
   conocimiento reutilizable (reglas en harness-core §3 y §9).
6. **Handoffs compactos:** entre agentes viaja un contrato, nunca la conversación entera.
7. **Estado del pipeline** (`.harness/state.md`) y métricas (`.harness/metrics.jsonl`)
   se mantienen al día; los escribe el Orchestrator.
8. Los agentes no editan la configuración global del usuario (`~/.config/opencode/**`).
9. Responde en el idioma del usuario.
10. **Un solo harness:** Apex_Harness es el único Orchestrator válido en un repo
   con este harness; no rutes a agentes ajenos (`apex` global, `build`, `general`,
   `explore`) — el allowlist de `subagent` de Apex_Harness los bloquea a nivel de
   permisos (ver harness-core §12).

## Notas de entorno

- `git` no está instalado en esta máquina: cualquier check `git diff/log` se marca
  UNVERIFIED y se sustituye por tests/evidencia de archivo. Instalar git lo desbloquea.
- `git` de este directorio conserva historial de un proyecto anterior distinto
  (harness externo runtime, descartado). No se toca.

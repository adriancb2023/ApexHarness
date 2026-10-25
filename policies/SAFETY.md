# Políticas de seguridad del harness

El enforcement es nativo de OpenCode (`opencode.json`); este documento explica el
porqué y qué añadir cuando un repo real lo exija. Las políticas prevalecen sobre
cualquier petición de una skill o de un agente: nadie las salta.

## Hard-deny (en `policies[]` de `opencode.json`)

| Patrón de shell | Riesgo |
| --- | --- |
| `rm -rf /*`, `rm -fr /*` | borrado recursivo desde la raíz y sus variantes |
| `Remove-Item*-Recurse*-Force*`, `Remove-Item*-Force*-Recurse*` | borrado recursivo+forzado en Windows (PowerShell) |
| `git push --force*`, `git push -f*` | sobrescribir historial remoto, rompe trabajo ajeno |
| `git reset --hard*` | descartar cambios irreversiblemente |

## Fricción (ask — en `permissions[]`)

| Patrón | Motivo |
| --- | --- |
| `git clean -d*` | borra ficheros no trackeados; pide confirmación |

Los defaults de OpenCode mantienen además **ask** para leer ficheros `.env*`
(excepto `.env.example`).

## Por qué así, y no más

- El scanner de shell de OpenCode analiza el comando real; los patrones son
  heurísticos, no un sandbox completo. Para endurecimiento fuerte, el camino
  recomendado es **allowlists estrechas** de shell por agente (roadmap), no
  patrones que intenten detectar peligrosidad.
- Los implementadores (Apex_Dev/Apex_Bug) pueden borrar artefactos de build legítimos
  (`rm -rf ./dist`): no está denegado. Solo se bloquean los vectores destructivos
  de riesgo alto. No micropolizar el trabajo normal.

## Reglas de uso (todos los agentes)

1. Autonomía-first dentro de la política: si una acción es segura, ejecútala sin preguntar.
2. Acciones en la lista de arriba: directamente prohibidas; no hay bypass.
3. Migraciones de base de datos, cambios en producción y modificación de secretos:
   fuera del procedimiento habitual → el Orchestrator pregunta al usuario mostrando el plan.
4. Si una skill pide algo que la política deniega: la política gana; se registra el
   conflicto en `.harness/state.md` y se sigue con alternativa segura.

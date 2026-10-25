# Métricas: cómo saber si el harness funciona

Sin medición, "el harness mejora" es una hipótesis. Este MVP registra lo
medible con medios nativos.

## Qué se registra por tarea (`metrics.jsonl`, una línea por tarea)

| Campo | Fuente | Nota |
| --- | --- | --- |
| `ts`, `task`, `pipeline`, `agents` | Orchestrator | identidad de la tarea |
| `skillsUsed` / `skillsSkipped` | routing (harness-core §5) | crucial medir si el router acierta; cada skip con su porqué |
| `memoryQueries` / `memoryResults` | llamadas/respuesta de Engram | 0 = gate decidió no buscar |
| `contextFiles` | conteo de archivos leídos en EXECUTE | disciplina de contexto |
| `verification.checks` / `.pass` | report de Apex_Verifier | evidencia por check |
| `retryCount` | ciclos REPAIR | objetivo: cercano a 0 |
| `finalState` | COMPLETED / FAILED / BLOCKED / UNVERIFIED | |
| `tokensTui` | panel de tokens del TUI | número real capturado a mano; `null` si no dispuso |

Todo el camino de la tarea (clasificar → memoria → skills → contexto →
implement → verify → retry) queda cubierto aquí; "más detalle por fase" es roadmap
(automatizable vía plugin hook, no en el MVP).

## Pregunta clave: ¿Engram ahorra tokens de verdad?

No se asume: se A/B. Protocolo mínimo:

1. Misma tarea, dos sesiones limpias:
   - A) `/harness <tarea>` con el protocolo completo (memory gate activo).
   - B) misma tarea idéntica con "memory skip" forzado (misma condiciones;
     solo cambia el lookup de memoria). Alternativa: ejecutarla con el agente
     `build` para comparar además sin protocolo.
2. En cada par compara: `tokensTui`, pasos, re-trabajo detectado
   (¿repitió investigación ya hecha?), `finalState` y calidad del resultado.
3. Hipótesis esperada: la memoria ahorra en tareas repetidas o del área ya conocida
   (evita redescubrir), y cuesta tokens en tareas netamente nuevas
   (búsquedas sin valor). Si A/B no muestra ventaja en tareas repetidas, el gate
   está mal calibrado — ajústalo y repite el experimento.

Registro del experimento: añade en cada línea JSONL del run una meta-nota
(`"ab": "A-memory|B-nomemory"` con referencia cruzada a la tarea gemela).

## Cuantitativo mínimo de salud

- Porcentaje de tareas terminadas COMPLETED con verificación independiente.
- retryCount medio (≥2 ciclos sistemáticos = diagnóstico débil).
- tokensTui medio por clase de complejidad (trivial vs estándar vs compleja).
- skillsSkipped correctas: revisar muestras — ¿el router descarta lo que no hacía falta?

El MVP mide a mano, lo justo para decidir si vale la pena automatizar
(plugin que escriba `metrics.jsonl` desde los eventos de OpenCode y el panel de
tokens de la API de sesiones).

Status: ready-for-agent

# Spec: Harness MVP — Control OpenCode multi-sesión + Kanban automático + Engram

## Problem Statement

El usuario programa con OpenCode (OSS MIT, v2.0.29) en terminal y quiere una GUI web como centro de control: hablar con OpenCode, crear sesiones, cambiar de proyecto, y poner a 2 sesiones (backend / frontend) a colaborar entre sí, con trazabilidad y memoria a largo plazo. Hoy no hay forma visual de supervisar debates inter-agente, ni Kanban ligado a dependencias, ni contadores de tokens por proyecto/feature.

## Solution

MVP con backend Python (FastAPI + uvicorn) que actúa como cliente de `opencode serve` (un serve por workspace/proyecto con distinto `directory`), y GUI mínima React/Vite con chat + streaming WS, vista debate 3 columnas, y Kanban automático alimentado por los propios agentes vía contrato `depends_on` con flechas de dependencia (React Flow). Persistencia operativa en SQLite (sesiones, tarjetas, locks, contadores tokens); memoria Engram en Qdrant embebido local con consolidación post-Done. Sin costes USD: solo contador de tokens por proyecto global y por feature.

## User Stories

1. As un desarrollador, I want abrir la GUI y ver el selector de proyectos, so that cambio de workspace sin tocar la terminal.
2. As un desarrollador, I want crear una sesión ligada a un proyecto, so that retomo contexto donde lo dejé.
3. As un desarrollador, I want listar sesiones de un proyecto (las nativas de OpenCode vía `session list`), so that no pierdo hilos.
4. As un desarrollador, I want enviar un mensaje desde el chat web y ver el streaming de la respuesta de OpenCode, so that hablo con el agente sin recargar.
5. As un desarrollador, I want cambiar de proyecto mientras una tarea larga sigue en segundo plano, so that trabajo en multitarea.
6. As un desarrollador, I want recibir notificación visual cuando una sesión en segundo plano termina o pide aprobación, so that no tengo que vigilarla.
7. As un supervisor de agentes, I want abrir 2 sesiones (backend y frontend) en workspaces aislados (worktrees/directorios), so that trabajan en paralelo sin pisarse.
8. As un agente backend, I want publicar un contrato de API (esquema JSON/OpenAPI resumido) al bus interno, so that el frontend sabe qué consumir.
9. As un agente frontend, I want recibir el contrato en mi inbox y generar componentes mockeados/conectados, so that avanzo sin esperar al humano como intermediario.
10. As un desarrollador, I want ver el debate inter-agente en 3 columnas (backend | debate | frontend), so that superviso la negociación.
11. As un desarrollador, I want modo paso-a-paso por defecto (aprobar cada envío backend→frontend), so that evito bucles descontrolados.
12. As un desarrollador, I want un cap de 5 turnos cruzados por debate, so that el intercambio termina o pide intervención.
13. As un agente, I want crear/actualizar tarjetas Kanban vía contrato (`title, feature, files[], depends_on[]`), so that el tablero se organiza solo.
14. As un desarrollador, I want ver columnas Backlog / En Progreso / Pruebas / Listo con tarjetas de feature/archivo, so that sigo el flujo ágil.
15. As un desarrollador, I want ver flechas de dependencia entre tarjetas derivadas de `depends_on`, so that entiendo bloqueos de un vistazo.
16. As un agente frontend, I want quedar visualmente bloqueado si mi dependencia backend no está en Done, so that no construyo sobre API inexistente.
17. As un agente, I want señalizar desbloqueo al mover mi tarjeta a Done, so that el dependiente retoma.
18. As un desarrollador, I want ver contador de tokens global por proyecto, so that controlo consumo sin hablar de dinero.
19. As un desarrollador, I want ver contador de tokens por feature/tarjeta concreta, so that sé qué cuesta cada esfuerzo.
20. As un auditor, I want historial de prompts/respuestas/tokens/tiempos por sesión, so that todo es trazable (vía `session export` + tabla propia).
21. As un desarrollador, I want locks de archivo (`path, locked_by, ts`) cuando un agente edita un archivo compartido, so that evito merges masivos.
22. As un agente bloqueado por un lock, I want recibir aviso de espera/liberación, so that no corrompo el archivo del otro.
23. As un desarrollador, I want que al mover una tarjeta a Done se consolide un Engram (Problema, Solución, Archivos, Lecciones), so that la memoria guarda calidad no ruido.
24. As un agente que empieza una tarea, I want recuperar Engrams similares como few-shot, so that no repito errores pasados.
25. As un desarrollador, I want botones Git básicos (commit/push/ramas) desde la GUI en fase posterior sin romper el MVP, so that el harness se autogestiona.

## Implementation Decisions

- Módulos MVP: SupervisorSesiones (CRUD sesiones + `cwd` por proyecto), OpencodeGateway (cliente de `opencode serve`: HTTP/WS, `api <method path>`, `session list/export/import`), BusDebate (inboxes + reenvío + cap turnos + paso-a-paso), KanbanStore (tarjetas + grafo `depends_on` + estados), TokenCounter (acumulados por sesión/proyecto/feature), FileLockStore, EngramStore (interfaz; impl Qdrant fase 2 temprana), GUI (chat, selector proyectos, debate 3 columnas, Kanban React Flow, Monaco read-only).
- Integración OpenCode: el Harness no reimplementa el agente; es cliente de `serve` con `--hostname/--port/--cors`, un serve por workspace. Sesiones con IDs nativos (`--session/-s`), continuación/fork soportados. `run` efímero solo como fallback.
- Contrato Kanban automático: los agentes escriben tarjetas con `depends_on[]`; el grafo y las flechas se derivan de ese campo, no de parsear git. Bloqueo visual si alguna dependencia no está en Done.
- Debate: modo paso-a-paso por defecto + `turn_cap=5`. Sin modo autónomo sin límite en MVP. Canal espejo visible, nada invisible.
- Tokens: conteo por sesión/proyecto/feature a partir de eventos de `serve` + `session export`. Sin conversión a USD, sin hard cap monetario.
- Persistencia operativa en SQLite: sesiones, tarjetas, locks, contadores, historial debate. Engram en Qdrant embebido (`qdrant-client` local, sin Docker) con pipeline de consolidación solo en transición a Done/commit.
- GUI: React + Vite + Tailwind + React Flow (flechas) + Monaco (visor). Sin Design Mode headless en MVP.
- Seams de test: seam principal API HTTP FastAPI (TestClient + OpencodeGateway fake); interfaces secundarias OpencodeGateway y Stores (SQLite fake en memoria, Qdrant fake) para no levantar `serve` real en tests.

## Testing Decisions

- Qué es buen test: solo comportamiento externo vía HTTP/WS (crear sesión, postear mensaje, publicar tarjeta con `depends_on`, verificar bloqueo/desbloqueo, verificar contador tokens, verificar lock), nunca detalles de implementación del gateway o del grafo.
- Módulos bajo test: SupervisorSesiones, BusDebate (cap + stepping), KanbanStore (transiciones + derivación de flechas), TokenCounter, FileLockStore. EngramStore solo a nivel de interfaz + consolidación (integración Qdrant real en ticket separado).
- Prior art: repo greenfield, sin tests previos; patrón a seguir es FastAPI TestClient + dobles fake del gateway.

## Out of Scope

- Backend Rust, binario Windows optimizado, Docker.
- Postgres, ChromaDB, Qdrant server dedicado.
- Observabilidad Phoenix / Langfuse / LangSmith en MVP.
- Chunking AST, filtro por grafo de código, caché de contexto proveedor.
- Design Mode con Puppeteer/Playwright y validación visual.
- Costes USD, presupuestos monetarios, kill-switch por dinero.
- Autografo de Kanban leyendo git; GitPython commit/push automáticos (solo botones manuales fase posterior).
- Merge coordinado multi-rama, worktrees simultáneos con compilación aislada completa.

## Further Notes

- Remote `origin`: `https://github.com/adriancb2023/ApexHarness.git` (rama `main`). Tracker MVP local por falta de `gh` CLI; migrar a GitHub Issues tras instalarlo.
- `git` disponible solo embebido en GitHubDesktop `app-3.6.6/.../git/cmd/git.exe`, no en `PATH`. Añadir al `PATH` o instalar `Git.Git` vía winget para worktrees.
- OpenCode flags verificados: `serve --hostname --port --cors --service`, `service start/stop/status`, `session list/export/import`, `api <method path>`.
- SQLite = operativo; Qdrant = Engram. No mezclar: la pregunta Q9 queda resuelta así.
- Siguiente paso: `to-tickets` para vertical slices en `.scratch/harness-mvp/issues/`.

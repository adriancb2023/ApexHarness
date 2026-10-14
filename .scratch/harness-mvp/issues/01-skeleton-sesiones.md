# 01: Skeleton + sesiones multi-proyecto

**What to build:** Backend FastAPI operativo con selector de proyectos y sesiones ligadas a workspace. Crear/listar sesiones nativas OpenCode y cambiar de proyecto retomando contexto.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [x] Crear sesión ligada a proyecto y listarla por proyecto vía API HTTP
- [x] Cambiar de proyecto conserva sesiones y `cwd` aislado por workspace
- [x] GUI muestra selector de proyectos + lista de sesiones
- [x] Tests externos vía TestClient con gateway fake, sin `serve` real

## Comments

Implementado en `b621763` (API sesiones + GUI estática + gateway fake, 2 tests en verde). Deuda: stores en memoria (SQLite file pendiente), GUI estática (Vite React desde ticket 03), integración `serve` real pendiente (ticket 02).

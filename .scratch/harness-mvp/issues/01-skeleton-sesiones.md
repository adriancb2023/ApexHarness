# 01: Skeleton + sesiones multi-proyecto

**What to build:** Backend FastAPI operativo con selector de proyectos y sesiones ligadas a workspace. Crear/listar sesiones nativas OpenCode y cambiar de proyecto retomando contexto.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [ ] Crear sesión ligada a proyecto y listarla por proyecto vía API HTTP
- [ ] Cambiar de proyecto conserva sesiones y `cwd` aislado por workspace
- [ ] GUI muestra selector de proyectos + lista de sesiones
- [ ] Tests externos vía TestClient con gateway fake, sin `serve` real

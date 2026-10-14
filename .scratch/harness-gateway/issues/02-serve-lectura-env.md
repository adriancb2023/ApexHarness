# 02: Serve lectura + config env

**What to build:** ServeGateway de lectura contra serve real con discovery y config por env.

**Blocked by:** 01 interfaz-fake.

**Status:** ready-for-agent

- [x] Auth Basic opencode:service.json y base URL configurable/descubierta
- [x] Sesiones reales listadas y vinculadas por opencode_session_id
- [x] Tokens reales en summary en modo real
- [x] Env HARNESS_DB/QDRANT/OPENCODE cableado en app de módulo
- [x] Tests con HTTP mockeado, sin red ni gasto

## Comments

Implementado (`ServeGateway` + discovery + `build_app`, 4 tests nuevos). Verificado en vivo solo-lectura: 50 sesiones, tokens parseados. Hallazgo: `opencode` es shim ps1 — discovery usa el exe real. Prompt/streaming en 03.

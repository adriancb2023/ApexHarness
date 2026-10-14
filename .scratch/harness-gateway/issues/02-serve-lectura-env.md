# 02: Serve lectura + config env

**What to build:** ServeGateway de lectura contra serve real con discovery y config por env.

**Blocked by:** 01 interfaz-fake.

**Status:** ready-for-agent

- [ ] Auth Basic opencode:service.json y base URL configurable/descubierta
- [ ] Sesiones reales listadas y vinculadas por opencode_session_id
- [ ] Tokens reales en summary en modo real
- [ ] Env HARNESS_DB/QDRANT/OPENCODE cableado en app de módulo
- [ ] Tests con HTTP mockeado, sin red ni gasto

# 03: Prompt + streaming + interrupt reales

**What to build:** Envío, streaming y parada contra sesiones reales.

**Blocked by:** 02 serve-lectura-env.

**Status:** ready-for-agent

- [x] send_prompt a sesión vinculada con respuesta persistida
- [x] Puente SSE→WS con protocolo delta/done actual
- [x] Interrupt con botón en GUI
- [ ] Vivo manual: prompt + streaming + interrupt en sesión de prueba (PENDIENTE APROBACIÓN GASTO)

## Comments

Implementado (prompt/interrupt/messages/bridge + rama real en WS + botón, 7 tests nuevos). Interrupt verificado en vivo (`False` en idle, sin gasto). Polling de `message` en vez de parsear SSE a ciegas. Pendiente: 1 prompt vivo de validación.

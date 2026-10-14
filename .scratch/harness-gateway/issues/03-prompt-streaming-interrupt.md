# 03: Prompt + streaming + interrupt reales

**What to build:** Envío, streaming y parada contra sesiones reales.

**Blocked by:** 02 serve-lectura-env.

**Status:** ready-for-agent

- [x] send_prompt a sesión vinculada con respuesta persistida
- [x] Puente SSE→WS con protocolo delta/done actual
- [x] Interrupt con botón en GUI
- [x] Vivo manual: prompt + streaming + interrupt en sesión de prueba

## Comments

Validación viva 2026-10-14 en `ses_ed0b1f27` (vacía): prompt aceptado (inbox), agente respondió en ~1s, gasto 9247 in + 11 out + 20 reasoning, cost 0. Hallazgos aplicados: el bridge tomaba assistants[-1] por posición y tragó un assistant viejo → filtro `since` + orden por `created`; los inbox van a INBOX y drenan solo con runner activo; existe mensaje `idle`; `message` pagina por cursor.

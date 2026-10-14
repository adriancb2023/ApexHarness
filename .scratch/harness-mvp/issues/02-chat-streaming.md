# 02: Chat WS streaming

**What to build:** Hablar con OpenCode desde la GUI con streaming en tiempo real, historial por sesión y notificación de tareas background.

**Blocked by:** 01 skeleton-sesiones.

**Status:** ready-for-agent

- [x] Enviar mensaje desde GUI y recibir streaming vía WS
- [x] Historial persistido por sesión y recuperable al cambiar de sesión
- [x] Notificación visual cuando background termina o pide aprobación
- [x] Tests externos de envío/streaming/historial con gateway fake

## Comments

Implementado (REST mensajes + WS deltas/done + `task-status` en GUI, 4 tests nuevos). Gateway fake con eco determinista; integración `serve` real y worker background asíncrono pendientes. Tokens base por mensaje (acumulado por sesión) — desglose proyecto/feature en ticket 05.

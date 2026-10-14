# 04: Debate backend-frontend + locks

**What to build:** Dos sesiones colaborando con supervisión humana y protección de archivos compartidos.

**Blocked by:** 02 chat-streaming, 03 kanban-grafo.

**Status:** ready-for-agent

- [x] Dos sesiones aisladas con inboxes y reenvío de contratos API
- [x] Vista 3 columnas con debate visible y aprobación paso-a-paso
- [x] Cap de 5 turnos cruzados con petición de intervención al exceder
- [x] Lock de archivo compartido con aviso de espera/liberación
- [x] Tests externos de debate, cap, stepping y locks

## Comments

Implementado (debates con pending/turns/cap 5 + locks con 409 y dueño, vista 3 columnas, 4 tests nuevos). Deuda: sin validación cruzada debate↔sesiones, entrega al inbox del receptor como turnos (no inyección real al `serve`), locks en memoria.

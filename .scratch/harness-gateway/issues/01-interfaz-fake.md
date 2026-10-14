# 01: Interfaz gateway + Fake extraído

**What to build:** Interfaz OpencodeGateway con el eco actual como FakeGateway, sin cambiar comportamiento.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [x] Interfaz con list/prompt/interrupt/events usada por los endpoints de chat
- [x] Fake con eco determinista y streaming en 2 deltas como hoy
- [x] 20 tests actuales verdes sin modificarse

## Comments

Implementado (`gateway.py`: `OpencodeGateway` + `FakeGateway`, 0 tests tocados). `gateway_fake` aún sin efecto; Serve en 02.

---
name: memory-audit-fastapi
description: >-
  Retención en FastAPI: Depends, background tasks y estado de app.
  Cárgala al auditar memoria de una app FastAPI. Carga también memory-audit-python.
---

# Memory audit — FastAPI

Úsala junto con `memory-audit-core` y `memory-audit-python`. El informe JSON lo dicta el core. Esta skill solo aporta los antipatrones y la forma del parche.

## Cuándo cuenta como cargada

Hecho cuando Discovery nombró un import de `fastapi` o la dependencia fastapi con su ruta, o cuando Apex_MemoryFixer ve esa tecnología en el hallazgo.

## Antipatrones

1. `Depends` que abre sesión, archivo o cliente. Señal: hace `return` en vez de `yield` con close en el `finally`. Recommendation: yield y close.
2. `BackgroundTasks` que captura el body entero o un `UploadFile` leído a memoria. Señal: lo guarda en un módulo. Recommendation: no retener el body; pasar solo el id.
3. `dict` de módulo o `app.state` usado como caché de respuestas. Señal: sin máximo. Recommendation: tope y TTL.
4. `StreamingResponse` o `FileResponse`. Señal: el iterator deja el archivo abierto si el cliente corta. Recommendation: cerrar en `finally`.
5. Middleware que hace append del body o de `request.state`. Señal: la lista vive el proceso. Recommendation: no acumular; medir sin guardar el body.

## Evidencia

CONFIRMED solo con perfilador o contador citado: tracemalloc. Si tracemalloc no está, PROBABLE con archivo y línea. Sin archivo y línea no hay finding.

## Cierre

Hecho cuando cada antipatrón de esta lista tiene archivo y línea o queda marcado ausente.

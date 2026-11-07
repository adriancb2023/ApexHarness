---
name: memory-audit-node
description: >-
  Retención en Node: cachés de proceso, streams y listeners.
  Cárgala al auditar memoria de un servidor o worker Node.
---

# Memory audit — Node

Úsala junto con `memory-audit-core`. El informe JSON lo dicta el core. Esta skill solo aporta los antipatrones y la forma del parche.

## Cuándo cuenta como cargada

Hecho cuando Discovery nombró un `package.json` con runtime node, o express/fastify/nest/koa, con su ruta, o cuando Apex_MemoryFixer ve esa tecnología en el hallazgo.

## Antipatrones

1. Map u objeto de módulo como caché de respuestas o sesiones, incluido `lru-cache` o memoizee. Señal: sin `max` o sin `maxAge`. Recommendation: max y TTL.
2. Stream (`fs`, `http`, busboy). Señal: sin `destroy` o sin `pipeline` en el camino de error y de close. Recommendation: pipeline o destroy en el error y en el close.
3. `emitter.on` en un cliente o en el request. Señal: no hay `off` al acabar. Recommendation: off en el finish o el close.
4. El handler hace push de `req.body` o del buffer a un array de módulo. Señal: el body vive fuera del request. Recommendation: no retener el body fuera del request.
5. `setInterval` de módulo que cierra sobre un buffer creciente. Señal: el intervalo sigue vivo en el shutdown. Recommendation: clearInterval al cerrar el servidor y no acumular el buffer.

Un Agent keep-alive no es finding por sí solo.

## Evidencia

CONFIRMED solo con perfilador o contador citado: `node --inspect` o clinic heapprofiler, RSS base contra N peticiones. PROBABLE con archivo y línea. Sin eso no hay finding.

## Cierre

Hecho cuando cada antipatrón de esta lista tiene archivo y línea o queda marcado ausente.

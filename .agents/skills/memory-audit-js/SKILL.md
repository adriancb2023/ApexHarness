---
name: memory-audit-js
description: >-
  Retención en JavaScript y TypeScript: cierres, Map sin tope, timers.
  Cárgala al auditar memoria de código JS o TS, en navegador o en servidor.
---

# Memory audit — JavaScript

Úsala junto con `memory-audit-core`. El informe JSON lo dicta el core. Esta skill solo aporta los antipatrones y la forma del parche.

## Cuándo cuenta como cargada

Hecho cuando Discovery nombró `package.json` o un import `.js`/`.ts`/`.mjs` con su ruta, o cuando Apex_MemoryFixer ve esa tecnología en el hallazgo.

## Antipatrones

1. Cierre que retiene el scope grande. Señal: callback, handler o promesa que captura un buffer, el body o un array que ya no hace falta. Recommendation: soltar esa referencia al acabar el ciclo (anular la variable o no capturarla).
2. Map, Set, Array u objeto de módulo que crece en cada llamada. Señal: sin tope, sin TTL y sin delete. Recommendation: límite de entradas y TTL, o delete al terminar.
3. `setInterval` o `setTimeout` recurrente. Señal: no hay `clearInterval`/`clearTimeout` en el mismo ciclo de vida. Recommendation: guardar el id y hacer clear en el teardown.
4. Global accidental que acumula peticiones o vistas. Señal: asignación sin `let`/`const`, o `globalThis`. Recommendation: variable local, o vaciar el global al cerrar el ciclo.
5. `then`/`catch` que conserva el payload completo después de extraer el campo útil. Señal: el callback sigue cerrado sobre el objeto entero. Recommendation: no cerrar sobre el payload; guardar solo el campo.

## Evidencia

CONFIRMED solo con perfilador o contador citado: Chrome DevTools heap o `node --inspect` / clinic heapprofiler. PROBABLE con archivo y línea. Sin eso no hay finding.

## Cierre

Hecho cuando cada antipatrón de esta lista tiene archivo y línea o queda marcado ausente.

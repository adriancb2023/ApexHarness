---
name: memory-audit-java
description: >-
  Retención en Java: colecciones static, ThreadLocal y streams.
  Cárgala al auditar memoria de un servicio Java.
---

# Memory audit — Java

Úsala junto con `memory-audit-core`. El informe JSON lo dicta el core. Esta skill solo aporta los antipatrones y la forma del parche.

## Cuándo cuenta como cargada

Hecho cuando Discovery nombró `pom.xml`, `build.gradle` o `src/main/java` con su ruta, o cuando Apex_MemoryFixer ve esa tecnología en el hallazgo.

## Antipatrones

1. `List` o `Map` static, o caché Guava/Caffeine, que acumula por request. Señal: sin `maximumSize` ni expire. Recommendation: `maximumSize` y `expireAfterWrite`.
2. `ThreadLocal.set` en un pool de hilos del servidor. Señal: no hay `remove` en un `finally`. Recommendation: remove en finally.
3. Listener u Observer registrado. Señal: nunca se quita. Recommendation: deregister en el shutdown o al cerrar el scope.
4. `Stream`, `Connection` o `InputStream`. Señal: fuera de try-with-resources. Recommendation: try-with-resources.
5. Sesión HTTP que guarda el grafo entero del usuario. Señal: la sesión no tiene cota. Recommendation: guardar el id, no el grafo.

Un static que solo guarda configuración inmutable no es finding.

## Evidencia

CONFIRMED solo con perfilador o contador citado: `jcmd GC.heap_dump` o VisualVM, si están. Si no están, PROBABLE con archivo y línea. Sin archivo y línea no hay finding.

## Cierre

Hecho cuando cada antipatrón de esta lista tiene archivo y línea o queda marcado ausente.

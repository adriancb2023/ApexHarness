---
name: memory-audit-workers
description: >-
  Retención en workers y colas: payloads, prefetch y listeners.
  Cárgala al auditar memoria de BullMQ, Celery, Hangfire, Channel o un cron.
---

# Memory audit — Workers

Úsala junto con `memory-audit-core`. El informe JSON lo dicta el core. Esta skill solo aporta los antipatrones y la forma del parche.

## Cuándo cuenta como cargada

Hecho cuando Discovery nombró una cola, un worker, `IHostedService`, Celery, Hangfire o un cron con su ruta, o cuando Apex_MemoryFixer ve esa tecnología en el hallazgo. Carga además la skill del runtime (`memory-audit-node`, `memory-audit-python`, `memory-audit-java` o `memory-audit-dotnet`) si el discovery la demuestra.

## Antipatrones

1. Payload de un job fallido o completado guardado entero en un array o mapa del proceso. Señal: en BullMQ, `removeOnComplete`/`removeOnFail` ausentes y un listener que hace push de `job.data`. Recommendation: política de borrado con cuenta o edad, y no guardar job.data.
2. Concurrencia o prefetch sin techo, de modo que el proceso materializa N payloads grandes a la vez. Señal: concurrency de BullMQ, `worker_prefetch_multiplier`, BasicQos prefetch 0, o Channel sin cota. Recommendation: techo de concurrencia y prefetch.
3. Listener de completed/failed/message registrado al arrancar y cerrado sobre el buffer. Señal: sigue registrado en el shutdown. Recommendation: quitar el listener al cerrar.
4. Scheduler o `setInterval` que solapa ejecuciones. Señal: cada tick retiene su lote. Recommendation: no solapar; soltar el lote al terminar.
5. Reintentos que guardan el error junto con el payload completo en una lista de módulo. Señal: la lista no tiene tope. Recommendation: guardar id y mensaje, con máximo de intentos.

Si el payload grande sale de un SELECT, recommendation = invocar a @Apex_SqlAuditor.

## Evidencia

CONFIRMED solo con el perfilador del runtime, o con RSS base contra una ráfaga de jobs. PROBABLE con archivo y línea. Sin eso no hay finding.

## Cierre

Hecho cuando cada antipatrón de esta lista tiene archivo y línea o queda marcado ausente.

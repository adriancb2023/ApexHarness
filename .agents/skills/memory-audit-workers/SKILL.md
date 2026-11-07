---
name: memory-audit-workers
description: >-
  Retention in workers and queues: payloads, prefetch, and listeners.
  Load it when auditing memory in BullMQ, Celery, Hangfire, Channel, or a cron.
---

# Memory audit — Workers

Use it together with `memory-audit-core`. The core dictates the JSON report. This skill only supplies the antipatterns and the shape of the patch.

## When it counts as loaded

Done when Discovery named a queue, a worker, `IHostedService`, Celery, Hangfire, or a cron with its path, or when Apex_MemoryFixer sees that technology in the finding. Also load the runtime skill (`memory-audit-node`, `memory-audit-python`, `memory-audit-java`, or `memory-audit-dotnet`) if discovery demonstrates it.

## Antipatterns

1. The payload of a failed or completed job kept whole in a process array or map. Signal: in BullMQ, `removeOnComplete`/`removeOnFail` are absent and a listener pushes `job.data`. Recommendation: a deletion policy by count or age, and do not store job.data.
2. Concurrency or prefetch with no ceiling, so the process materializes N large payloads at once. Signal: BullMQ concurrency, `worker_prefetch_multiplier`, BasicQos prefetch 0, or an unbounded Channel. Recommendation: a concurrency ceiling and a prefetch cap.
3. A completed/failed/message listener registered at startup and closed over the buffer. Signal: it is still registered at shutdown. Recommendation: remove the listener on close.
4. A scheduler or `setInterval` that overlaps runs. Signal: each tick retains its batch. Recommendation: do not overlap; release the batch when it finishes.
5. Retries that store the error together with the full payload in a module list. Signal: the list has no cap. Recommendation: store the id and the message, with a maximum number of attempts.

If the large payload comes from a SELECT, recommendation = invoke @Apex_SqlAuditor.

## Evidence

CONFIRMED only with the runtime profiler, or with baseline RSS against a burst of jobs. PROBABLE with file and line. Without that, there is no finding.

## Close

Done when every antipattern on this list has a file and a line, or is marked absent.

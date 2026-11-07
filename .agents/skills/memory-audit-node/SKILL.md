---
name: memory-audit-node
description: >-
  Retention in Node: process caches, streams, and listeners.
  Load it when auditing memory in a Node server or worker.
---

# Memory audit — Node

Use it together with `memory-audit-core`. The core dictates the JSON report. This skill only supplies the antipatterns and the shape of the patch.

## When it counts as loaded

Done when Discovery named a `package.json` with a node runtime, or express/fastify/nest/koa, with its path, or when Apex_MemoryFixer sees that technology in the finding.

## Antipatterns

1. A module Map or object used as a cache of responses or sessions, including `lru-cache` or memoizee. Signal: no `max` or no `maxAge`. Recommendation: max and TTL.
2. A stream (`fs`, `http`, busboy). Signal: no `destroy` and no `pipeline` on the error path and the close path. Recommendation: pipeline, or destroy on error and on close.
3. `emitter.on` on a client or on the request. Signal: there is no `off` when it finishes. Recommendation: off on finish or close.
4. The handler pushes `req.body` or the buffer onto a module array. Signal: the body lives outside the request. Recommendation: do not retain the body outside the request.
5. A module `setInterval` closed over a growing buffer. Signal: the interval is still alive at shutdown. Recommendation: clearInterval when the server closes, and do not accumulate the buffer.

An Agent keep-alive is not a finding by itself.

## Evidence

CONFIRMED only with a cited profiler or counter: `node --inspect` or clinic heapprofiler, baseline RSS against N requests. PROBABLE with file and line. Without that, there is no finding.

## Close

Done when every antipattern on this list has a file and a line, or is marked absent.

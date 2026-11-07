---
name: memory-audit-java
description: >-
  Retention in Java: static collections, ThreadLocal, and streams.
  Load it when auditing memory in a Java service.
---

# Memory audit — Java

Use it together with `memory-audit-core`. The core dictates the JSON report. This skill only supplies the antipatterns and the shape of the patch.

## When it counts as loaded

Done when Discovery named `pom.xml`, `build.gradle`, or `src/main/java` with its path, or when Apex_MemoryFixer sees that technology in the finding.

## Antipatterns

1. A static `List` or `Map`, or a Guava/Caffeine cache, that accumulates per request. Signal: no `maximumSize` and no expire. Recommendation: `maximumSize` and `expireAfterWrite`.
2. `ThreadLocal.set` on a server thread pool. Signal: there is no `remove` in a `finally`. Recommendation: remove in finally.
3. A registered Listener or Observer. Signal: it is never removed. Recommendation: deregister on shutdown or when the scope closes.
4. `Stream`, `Connection`, or `InputStream`. Signal: outside try-with-resources. Recommendation: try-with-resources.
5. An HTTP session that stores the user's entire object graph. Signal: the session has no bound. Recommendation: store the id, not the graph.

A static that only holds immutable configuration is not a finding.

## Evidence

CONFIRMED only with a cited profiler or counter: `jcmd GC.heap_dump` or VisualVM, if they are present. If they are absent, PROBABLE with file and line. Without file and line there is no finding.

## Close

Done when every antipattern on this list has a file and a line, or is marked absent.

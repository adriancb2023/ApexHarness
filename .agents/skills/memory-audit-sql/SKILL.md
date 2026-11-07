---
name: memory-audit-sql
description: >-
  Retention from SQL and ORMs: full result sets, N+1, and connections.
  Load it when auditing memory of queries or of an ORM, on any engine.
---

# Memory audit — SQL

Use it together with `memory-audit-core`. The core dictates the JSON report. This skill only supplies the antipatterns and the shape of the patch.

## When it counts as loaded

Done when Discovery named embedded SQL, a repository, or an ORM/driver dependency with its path, or when Apex_MemoryFixer sees that technology in the finding.

## Antipatterns

1. `SELECT *` or a full entity from a large table. Signal: no limit, keyset, or cursor, and it brings columns the caller does not use. Recommendation: explicit columns and a limit or cursor.
2. `fetchall`, `ToList`, or `getResultList` of a large result. Signal: it materializes the result instead of streaming or paging. Recommendation: stream or page.
3. A connection, cursor, or reader that never returns to the pool. Signal: no close, no `using`, no `with`, or an ORM session that lives outside the request. Recommendation: return it in `finally`; a session per request.
4. N+1. Signal: a query or lazy load inside a loop that instantiates one model per row. Recommendation: one batched query or a join.
5. An identity map or ORM session stored on a singleton. Signal: every entity that was read lives for the process. Recommendation: a session per request, not a singleton.

If the engine is PostgreSQL, also load memory-audit-postgresql. Do not look at the frontend.

## Evidence

CONFIRMED only with a cited profiler or counter: row count and process RSS before and after the query. If there is no runtime, PROBABLE with file and line. Without file and line there is no finding.

## Close

Done when every antipattern on this list has a file and a line, or is marked absent.

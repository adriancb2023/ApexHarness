---
name: memory-audit-postgresql
description: >-
  PostgreSQL-specific retention: cursors, fetch size, jsonb, and pools.
  Load it when auditing memory against PostgreSQL, together with memory-audit-sql.
---

# Memory audit — PostgreSQL

Use it together with `memory-audit-core` and `memory-audit-sql`. The core dictates the JSON report. This skill only supplies the antipatterns and the shape of the patch.

## When it counts as loaded

Done when Discovery named a `pg` driver, psycopg, asyncpg, Npgsql, `jdbc:postgresql`, or SQLAlchemy with postgres, with its path, or when Apex_MemoryFixer sees that technology in the finding.

## Antipatterns

1. `ORDER BY`, `DISTINCT`, or an aggregation over a large set. Signal: no `LIMIT` and no cursor; the client receives every row. Recommendation: a limit, keyset, or server-side cursor.
2. A client that materializes the SELECT. Signal: psycopg `fetchall`, node-pg `query()` of a large result, Npgsql without SequentialAccess/stream, JDBC without `setFetchSize`. Recommendation: fetch size or a cursor (DECLARE/FETCH), not one single byte[].
3. A wide `jsonb` or `text` column in the SELECT. Signal: the code uses a single key. Recommendation: project the key, not the whole column.
4. `COPY` or a dump read all at once into a string or `byte[]`. Signal: the client keeps the full dump. Recommendation: read in blocks and release each block.
5. `LISTEN` whose client queues notifications. Signal: the list has no cap. Recommendation: a cap, and drop the notification once it is processed.
6. A pool (`pg.Pool`, NpgsqlDataSource, Hikari, SQLAlchemy pool) with `BEGIN`. Signal: the error path does not `COMMIT`/`ROLLBACK`. Recommendation: close the transaction in `finally` and return the connection.

Do not ask to change postgresql.conf as an Apex_MemoryFixer patch. EXPLAIN or the client-side row count is evidence.

## Evidence

CONFIRMED only with a cited profiler or counter: EXPLAIN or the client-side row count. Without a runtime, PROBABLE with file and line. Without file and line there is no finding.

## Close

Done when every antipattern on this list has a file and a line, or is marked absent.

---
name: memory-audit-postgresql
description: >-
  Retención específica de PostgreSQL: cursores, fetch size, jsonb y pools.
  Cárgala al auditar memoria contra PostgreSQL, junto con memory-audit-sql.
---

# Memory audit — PostgreSQL

Úsala junto con `memory-audit-core` y `memory-audit-sql`. El informe JSON lo dicta el core. Esta skill solo aporta los antipatrones y la forma del parche.

## Cuándo cuenta como cargada

Hecho cuando Discovery nombró un driver `pg`, psycopg, asyncpg, Npgsql, `jdbc:postgresql` o SQLAlchemy con postgres, con su ruta, o cuando Apex_MemoryFixer ve esa tecnología en el hallazgo.

## Antipatrones

1. `ORDER BY`, `DISTINCT` o agregación sobre un conjunto grande. Señal: sin `LIMIT` ni cursor; el cliente recibe todas las filas. Recommendation: límite, keyset o cursor de servidor.
2. Cliente que materializa el SELECT. Señal: psycopg `fetchall`, node-pg `query()` de un result grande, Npgsql sin SequentialAccess/stream, JDBC sin `setFetchSize`. Recommendation: fetch size o cursor (DECLARE/FETCH), no un byte[] único.
3. Columna `jsonb` o `text` ancha en el SELECT. Señal: el código usa una sola clave. Recommendation: proyectar la clave, no la columna entera.
4. `COPY` o un volcado leído de una vez a string o `byte[]`. Señal: el cliente conserva el volcado completo. Recommendation: leer por bloques y soltar cada bloque.
5. `LISTEN` cuyo cliente encola notificaciones. Señal: la lista no tiene tope. Recommendation: tope y descarte de la notificación ya procesada.
6. Pool (`pg.Pool`, NpgsqlDataSource, Hikari, pool de SQLAlchemy) con `BEGIN`. Señal: el error no hace `COMMIT`/`ROLLBACK`. Recommendation: cerrar la transacción en `finally` y devolver la conexión.

No pidas cambiar postgresql.conf como parche de Apex_MemoryFixer. EXPLAIN o el conteo de filas en el cliente sirve de evidencia.

## Evidencia

CONFIRMED solo con perfilador o contador citado: EXPLAIN o el conteo de filas en el cliente. Sin runtime, PROBABLE con archivo y línea. Sin archivo y línea no hay finding.

## Cierre

Hecho cuando cada antipatrón de esta lista tiene archivo y línea o queda marcado ausente.

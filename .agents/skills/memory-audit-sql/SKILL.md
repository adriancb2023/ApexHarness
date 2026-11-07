---
name: memory-audit-sql
description: >-
  Retención por SQL y ORMs: resultados enteros, N+1 y conexiones.
  Cárgala al auditar memoria de consultas o de un ORM, en cualquier motor.
---

# Memory audit — SQL

Úsala junto con `memory-audit-core`. El informe JSON lo dicta el core. Esta skill solo aporta los antipatrones y la forma del parche.

## Cuándo cuenta como cargada

Hecho cuando Discovery nombró SQL embebido, un repositorio o una dependencia de ORM/driver con su ruta, o cuando Apex_MemoryFixer ve esa tecnología en el hallazgo.

## Antipatrones

1. `SELECT *` o entidad completa de una tabla grande. Señal: sin límite, keyset ni cursor, y trae columnas que el llamador no usa. Recommendation: columnas explícitas y límite o cursor.
2. `fetchall`, `ToList` o `getResultList` de un resultado grande. Señal: materializa el resultado en vez de stream o página. Recommendation: stream o página.
3. Conexión, cursor o reader que no vuelve al pool. Señal: sin close, sin `using`, sin `with`, o sesión de ORM viva fuera del request. Recommendation: devolverla en `finally`; sesión por request.
4. N+1. Señal: query o lazy load dentro de un bucle que instancia un modelo por fila. Recommendation: una query en lote o un join.
5. Identity map o sesión de ORM guardada en un singleton. Señal: cada entidad leída vive el proceso. Recommendation: sesión por request, no singleton.

Si el motor es PostgreSQL, carga también memory-audit-postgresql. No mires el frontend.

## Evidencia

CONFIRMED solo con perfilador o contador citado: contador de filas y RSS del proceso antes y después de la consulta. Si no hay runtime, PROBABLE con archivo y línea. Sin archivo y línea no hay finding.

## Cierre

Hecho cuando cada antipatrón de esta lista tiene archivo y línea o queda marcado ausente.

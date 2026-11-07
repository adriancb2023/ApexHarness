---
name: memory-audit-python
description: >-
  Retención en Python: lru_cache, globales y recursos sin cerrar.
  Cárgala al auditar memoria de código Python.
---

# Memory audit — Python

Úsala junto con `memory-audit-core`. El informe JSON lo dicta el core. Esta skill solo aporta los antipatrones y la forma del parche.

## Cuándo cuenta como cargada

Hecho cuando Discovery nombró `pyproject.toml`, `requirements.txt` o un `*.py` de servidor o worker con su ruta, o cuando Apex_MemoryFixer ve esa tecnología en el hallazgo.

## Antipatrones

1. `functools.lru_cache` o `cache` sobre una función cuyo argumento es grande o no acotado. Señal: `maxsize` ausente o `None`. Recommendation: maxsize finito, o no cachear el argumento grande.
2. `list`, `dict` o `set` de módulo. Señal: `append` por request, sin tope ni `clear`. Recommendation: tope o clear al acabar.
3. Archivo, generador o conexión. Señal: sin `close` y sin `with`. Recommendation: `with` o close en `finally`.
4. `Thread` o `ThreadPoolExecutor`. Señal: sin `shutdown`, o un hilo que retiene el frame. Recommendation: shutdown en el teardown.
5. Una lista de módulo guarda `traceback` o `logging.exception` de cada fallo. Señal: el objeto de error completo entra en la lista. Recommendation: guardar solo tipo y mensaje, con tope.
6. pandas o numpy leyendo el dataset entero (`read_csv`/`read_sql` sin `chunksize` ni límite) y dejándolo en un global. Señal: el llamador pide una página y el global conserva el dataset. Recommendation: `chunksize` o límite, sin global.

## Evidencia

CONFIRMED solo con perfilador o contador citado: tracemalloc, si está. Si tracemalloc no está, PROBABLE con archivo y línea. Sin archivo y línea no hay finding.

## Cierre

Hecho cuando cada antipatrón de esta lista tiene archivo y línea o queda marcado ausente.

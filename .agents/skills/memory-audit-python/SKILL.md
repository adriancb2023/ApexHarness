---
name: memory-audit-python
description: >-
  Retention in Python: lru_cache, globals, and resources that are never closed.
  Load it when auditing memory in Python code.
---

# Memory audit — Python

Use it together with `memory-audit-core`. The core dictates the JSON report. This skill only supplies the antipatterns and the shape of the patch.

## When it counts as loaded

Done when Discovery named `pyproject.toml`, `requirements.txt`, or a server or worker `*.py` with its path, or when Apex_MemoryFixer sees that technology in the finding.

## Antipatterns

1. `functools.lru_cache` or `cache` on a function whose argument is large or unbounded. Signal: `maxsize` is missing or `None`. Recommendation: a finite maxsize, or do not cache the large argument.
2. A module `list`, `dict`, or `set`. Signal: `append` per request, with no cap and no `clear`. Recommendation: a cap, or clear when finished.
3. A file, generator, or connection. Signal: no `close` and no `with`. Recommendation: `with`, or close in `finally`.
4. `Thread` or `ThreadPoolExecutor`. Signal: no `shutdown`, or a thread that retains the frame. Recommendation: shutdown on teardown.
5. A module list stores the `traceback` or `logging.exception` of every failure. Signal: the full error object goes into the list. Recommendation: store only the type and the message, with a cap.
6. pandas or numpy reading the whole dataset (`read_csv`/`read_sql` with no `chunksize` and no limit) and leaving it on a global. Signal: the caller asks for a page and the global keeps the dataset. Recommendation: `chunksize` or a limit, with no global.

## Evidence

CONFIRMED only with a cited profiler or counter: tracemalloc, if it is present. If tracemalloc is absent, PROBABLE with file and line. Without file and line there is no finding.

## Close

Done when every antipattern on this list has a file and a line, or is marked absent.

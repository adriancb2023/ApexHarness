---
name: memory-audit-fastapi
description: >-
  Retention in FastAPI: Depends, background tasks, and app state.
  Load it when auditing memory in a FastAPI app. Also load memory-audit-python.
---

# Memory audit — FastAPI

Use it together with `memory-audit-core` and `memory-audit-python`. The core dictates the JSON report. This skill only supplies the antipatterns and the shape of the patch.

## When it counts as loaded

Done when Discovery named a `fastapi` import or the fastapi dependency with its path, or when Apex_MemoryFixer sees that technology in the finding.

## Antipatterns

1. A `Depends` that opens a session, file, or client. Signal: it `return`s instead of `yield` with close in the `finally`. Recommendation: yield and close.
2. `BackgroundTasks` that captures the whole body or an `UploadFile` read into memory. Signal: it stores that on a module. Recommendation: do not retain the body; pass only the id.
3. A module `dict` or `app.state` used as a response cache. Signal: no maximum. Recommendation: a cap and a TTL.
4. `StreamingResponse` or `FileResponse`. Signal: the iterator leaves the file open if the client disconnects. Recommendation: close in `finally`.
5. Middleware that appends the body or `request.state`. Signal: the list lives for the process. Recommendation: do not accumulate; measure without storing the body.

## Evidence

CONFIRMED only with a cited profiler or counter: tracemalloc. If tracemalloc is absent, PROBABLE with file and line. Without file and line there is no finding.

## Close

Done when every antipattern on this list has a file and a line, or is marked absent.

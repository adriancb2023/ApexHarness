---
name: memory-audit-js
description: >-
  Retention in JavaScript and TypeScript: closures, unbounded Map, timers.
  Load it when auditing memory in JS or TS code, in the browser or on the server.
---

# Memory audit — JavaScript

Use it together with `memory-audit-core`. The core dictates the JSON report. This skill only supplies the antipatterns and the shape of the patch.

## When it counts as loaded

Done when Discovery named `package.json` or a `.js`/`.ts`/`.mjs` import with its path, or when Apex_MemoryFixer sees that technology in the finding.

## Antipatterns

1. A closure that retains a large scope. Signal: a callback, handler, or promise that captures a buffer, the body, or an array that is no longer needed. Recommendation: drop that reference when the cycle ends (null the variable, or do not capture it).
2. A Map, Set, Array, or module object that grows on every call. Signal: no cap, no TTL, and no delete. Recommendation: an entry limit and a TTL, or delete when finished.
3. A recurring `setInterval` or `setTimeout`. Signal: there is no `clearInterval`/`clearTimeout` in the same lifecycle. Recommendation: keep the id and clear it on teardown.
4. An accidental global that accumulates requests or views. Signal: an assignment without `let`/`const`, or `globalThis`. Recommendation: a local variable, or clear the global when the cycle closes.
5. A `then`/`catch` that keeps the full payload after the useful field was extracted. Signal: the callback stays closed over the whole object. Recommendation: do not close over the payload; keep only the field.

## Evidence

CONFIRMED only with a cited profiler or counter: Chrome DevTools heap, or `node --inspect` / clinic heapprofiler. PROBABLE with file and line. Without that, there is no finding.

## Close

Done when every antipattern on this list has a file and a line, or is marked absent.

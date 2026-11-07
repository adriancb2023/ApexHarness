---
name: memory-audit-react
description: >-
  Retention in React: effects without cleanup, data caches, and URL objects.
  Load it when auditing memory in React components.
---

# Memory audit — React

Use it together with `memory-audit-core`. The core dictates the JSON report. This skill only supplies the antipatterns and the shape of the patch.

## When it counts as loaded

Done when Discovery named the `react` dependency or a `react` import with its path, or when Apex_MemoryFixer sees that technology in the finding.

## Antipatterns

1. `useEffect` or `useLayoutEffect` with a listener, interval, WebSocket, or observer. Signal: the effect does not return a cleanup function. Recommendation: return the unsubscribe.
2. `fetch` or axios inside an effect. Signal: there is no `AbortController` in the cleanup. Recommendation: abort in the cleanup.
3. React Query, SWR, or a router cache. Signal: infinite `gcTime`/`cacheTime`, or a module-level `QueryClient` that does not release pages on route change. Recommendation: a finite gcTime, and do not retain page data on a module.
4. A ref that stores a DOM node, or `URL.createObjectURL`. Signal: the ref stays set and there is no `revokeObjectURL` on unmount. Recommendation: cleanup that nulls and revokes.
5. A large await result stored on a module or in a store after the component unmounted. Signal: a write outside the component after unmount, or history accumulated on the module. Recommendation: do not write outside the component if the effect already cleaned up, and do not accumulate history on the module.

A new `value={{...}}` on every render is not a finding.

## Evidence

CONFIRMED only with a cited profiler or counter: Chrome DevTools, comparing the heap after unmount. PROBABLE with file and line. Without that, there is no finding.

## Close

Done when every antipattern on this list has a file and a line, or is marked absent.

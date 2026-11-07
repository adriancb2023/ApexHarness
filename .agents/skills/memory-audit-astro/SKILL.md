---
name: memory-audit-astro
description: >-
  Retention in Astro: client scripts, View Transitions, and islands.
  Load it when auditing memory in an Astro project.
---

# Memory audit — Astro

Use it together with `memory-audit-core`. The core dictates the JSON report. This skill only supplies the antipatterns and the shape of the patch.

## When it counts as loaded

Done when Discovery named `astro.config` or the `astro` dependency with its path, or when Apex_MemoryFixer sees that technology in the finding.

## Antipatterns

1. A page or layout script with `addEventListener` or `setInterval` on `window`/`document`. Signal: with View Transitions there is no removal on `astro:before-swap`, `pagehide`, or `beforeunload`. Recommendation: remove the listener on `astro:before-swap`.
2. `client:load` (or `client:idle`/`client:visible`) on a component that only displays data. Signal: the component has no interaction. Recommendation: remove the client directive.
3. nanostore, a module map, or `window.__STATE`. Signal: it accumulates data from every navigation. Recommendation: reset on page transition.
4. `URL.createObjectURL` or image blobs in a client script. Signal: there is no `revokeObjectURL`. Recommendation: revoke when the view is released.

Use of astro:assets is not a finding.

## Evidence

CONFIRMED only with a cited profiler or counter: Chrome DevTools after navigating with View Transitions. PROBABLE with file and line. Without that, there is no finding.

## Close

Done when every antipattern on this list has a file and a line, or is marked absent.

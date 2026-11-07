---
name: memory-audit-dotnet
description: >-
  Retention in .NET: events, IDisposable, unbounded channels, and ArrayPool.
  Load it when auditing memory in a .NET process.
---

# Memory audit — .NET

Use it together with `memory-audit-core`. The core dictates the JSON report. This skill only supplies the antipatterns and the shape of the patch.

## When it counts as loaded

Done when Discovery named a `*.csproj` with its path, or when Apex_MemoryFixer sees that technology in the finding.

## Antipatterns

1. A type with a `Stream`, an event, or a native handle. Signal: the caller does not use `using` or `Dispose`. Recommendation: `using`.
2. `+=` on an event of a long-lived object (static or singleton). Signal: there is no `-=`. Recommendation: `-=` in `Dispose` or when the scope closes.
3. `ConcurrentDictionary` or `IMemoryCache`. Signal: no `SizeLimit` and no expiration, or `GetOrCreate` of the whole graph. Recommendation: SizeLimit and expiration; do not cache the graph.
4. `Channel.CreateUnbounded` or a job `List` on a field of `BackgroundService`/`IHostedService`. Signal: the channel or the list has no bound. Recommendation: `Channel.CreateBounded`.
5. A `byte[]`, `MemoryStream`, or the HTTP content of every request. Signal: accumulated on a static field. Recommendation: do not accumulate; use it and release it.
6. `ArrayPool.Shared.Rent`. Signal: there is no `Return` in the `finally`. Recommendation: `Return` in finally.

If the retainer is a singleton `DbContext` with a huge `ToList`, the finding stays here only when the field belongs to the process. If the cause is the query, recommendation = invoke @Apex_SqlAuditor.

## Evidence

CONFIRMED only with a cited profiler or counter: dotnet-counters or dotnet-gcdump, if they are present. If they are absent, PROBABLE with file and line. Without file and line there is no finding.

## Close

Done when every antipattern on this list has a file and a line, or is marked absent.

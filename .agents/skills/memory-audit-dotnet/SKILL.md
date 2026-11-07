---
name: memory-audit-dotnet
description: >-
  Retención en .NET: eventos, IDisposable, canales sin cota y ArrayPool.
  Cárgala al auditar memoria de un proceso .NET.
---

# Memory audit — .NET

Úsala junto con `memory-audit-core`. El informe JSON lo dicta el core. Esta skill solo aporta los antipatrones y la forma del parche.

## Cuándo cuenta como cargada

Hecho cuando Discovery nombró un `*.csproj` con su ruta, o cuando Apex_MemoryFixer ve esa tecnología en el hallazgo.

## Antipatrones

1. Tipo con `Stream`, evento o handle nativo. Señal: el llamador no usa `using` ni `Dispose`. Recommendation: `using`.
2. `+=` a un evento de un objeto de larga vida (static o singleton). Señal: no hay `-=`. Recommendation: `-=` en `Dispose` o al cerrar el scope.
3. `ConcurrentDictionary` o `IMemoryCache`. Señal: sin `SizeLimit` ni expiración, o `GetOrCreate` del grafo entero. Recommendation: SizeLimit y expiración; no cachear el grafo.
4. `Channel.CreateUnbounded` o una `List` de jobs en un campo de `BackgroundService`/`IHostedService`. Señal: el canal o la lista no tienen cota. Recommendation: `Channel.CreateBounded`.
5. `byte[]`, `MemoryStream` o contenido HTTP de cada request. Señal: acumulado en un campo static. Recommendation: no acumular; usar y soltar.
6. `ArrayPool.Shared.Rent`. Señal: no hay `Return` en el `finally`. Recommendation: `Return` en finally.

Si el retenedor es un `DbContext` singleton con un `ToList` enorme, el finding queda aquí solo cuando el campo es del proceso. Si la causa es la consulta, recommendation = invocar a @Apex_SqlAuditor.

## Evidencia

CONFIRMED solo con perfilador o contador citado: dotnet-counters o dotnet-gcdump, si están. Si no están, PROBABLE con archivo y línea. Sin archivo y línea no hay finding.

## Cierre

Hecho cuando cada antipatrón de esta lista tiene archivo y línea o queda marcado ausente.

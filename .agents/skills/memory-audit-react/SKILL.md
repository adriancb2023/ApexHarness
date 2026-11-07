---
name: memory-audit-react
description: >-
  Retención en React: effects sin cleanup, cachés de datos y objetos URL.
  Cárgala al auditar memoria de componentes React.
---

# Memory audit — React

Úsala junto con `memory-audit-core`. El informe JSON lo dicta el core. Esta skill solo aporta los antipatrones y la forma del parche.

## Cuándo cuenta como cargada

Hecho cuando Discovery nombró la dependencia `react` o un import de `react` con su ruta, o cuando Apex_MemoryFixer ve esa tecnología en el hallazgo.

## Antipatrones

1. `useEffect` o `useLayoutEffect` con listener, interval, WebSocket u observer. Señal: el effect no devuelve función de cleanup. Recommendation: devolver la desuscripción.
2. `fetch` o axios en un effect. Señal: no hay `AbortController` en el cleanup. Recommendation: abort en el cleanup.
3. React Query, SWR o caché de router. Señal: `gcTime`/`cacheTime` infinito, o un `QueryClient` de módulo que no libera páginas al cambiar de ruta. Recommendation: gcTime finito y no retener el page data en un módulo.
4. Ref que guarda un nodo DOM, o `URL.createObjectURL`. Señal: el ref sigue puesto y no hay `revokeObjectURL` al desmontar. Recommendation: cleanup que anula y revoca.
5. Resultado grande de un await guardado en un módulo o en un store después de que el componente se desmontó. Señal: escritura fuera del componente tras el unmount, o históricos acumulados en el módulo. Recommendation: no escribir fuera del componente si el efecto ya limpió, y no acumular históricos en el módulo.

Un `value={{...}}` nuevo en cada render no es finding.

## Evidencia

CONFIRMED solo con perfilador o contador citado: Chrome DevTools, comparando el heap tras unmount. PROBABLE con archivo y línea. Sin eso no hay finding.

## Cierre

Hecho cuando cada antipatrón de esta lista tiene archivo y línea o queda marcado ausente.

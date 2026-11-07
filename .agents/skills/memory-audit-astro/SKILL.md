---
name: memory-audit-astro
description: >-
  Retención en Astro: scripts de cliente, View Transitions e islas.
  Cárgala al auditar memoria de un proyecto Astro.
---

# Memory audit — Astro

Úsala junto con `memory-audit-core`. El informe JSON lo dicta el core. Esta skill solo aporta los antipatrones y la forma del parche.

## Cuándo cuenta como cargada

Hecho cuando Discovery nombró `astro.config` o la dependencia `astro` con su ruta, o cuando Apex_MemoryFixer ve esa tecnología en el hallazgo.

## Antipatrones

1. Script de página o layout con `addEventListener` o `setInterval` en `window`/`document`. Señal: con View Transitions no hay retirada en `astro:before-swap`, `pagehide` o `beforeunload`. Recommendation: quitar el listener en `astro:before-swap`.
2. `client:load` (o `client:idle`/`client:visible`) en un componente que solo muestra datos. Señal: el componente no tiene interacción. Recommendation: quitar la directiva de cliente.
3. nanostore, mapa de módulo o `window.__STATE`. Señal: acumula datos de cada navegación. Recommendation: reset en la transición de página.
4. `URL.createObjectURL` o blobs de imagen en un script de cliente. Señal: no hay `revokeObjectURL`. Recommendation: revocar al soltar la vista.

El uso de astro:assets no es finding.

## Evidencia

CONFIRMED solo con perfilador o contador citado: Chrome DevTools tras navegar con View Transitions. PROBABLE con archivo y línea. Sin eso no hay finding.

## Cierre

Hecho cuando cada antipatrón de esta lista tiene archivo y línea o queda marcado ausente.

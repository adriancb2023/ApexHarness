# Compat: redirige al bootstrap unificado OpenCode + Cursor.
param(
  [switch]$FromOpenCodeGlobal,
  [switch]$OfficialInstaller
)

& "$PSScriptRoot\bootstrap-matt-skills.ps1" -Target Cursor @PSBoundParameters

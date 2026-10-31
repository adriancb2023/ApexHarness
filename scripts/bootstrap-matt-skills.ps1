# Bootstrap Skills for Real Engineers into project paths (OpenCode + Cursor).
# No se versionan en git (salvo harness-core). Preferencia: instalador oficial (git).
# Fallback: copia desde ~/.config/opencode/skills

param(
  [ValidateSet("Both", "OpenCode", "Cursor")]
  [string]$Target = "Both",
  [switch]$FromOpenCodeGlobal,
  [switch]$OfficialInstaller
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$globalSrc = Join-Path $env:USERPROFILE ".config\opencode\skills"

function Copy-MattSkills([string]$dst) {
  if (-not (Test-Path $globalSrc)) {
    throw "No existe $globalSrc. Instala primero: npx skills add mattpocock/skills -a opencode -y"
  }
  New-Item -ItemType Directory -Force -Path $dst | Out-Null
  $n = 0
  Get-ChildItem $globalSrc -Directory | ForEach-Object {
    if ($_.Name -eq "harness-core") { return }
    $target = Join-Path $dst $_.Name
    if (Test-Path $target) { Remove-Item $target -Recurse -Force }
    Copy-Item $_.FullName $target -Recurse -Force
    $n++
  }
  Write-Host "OK: $n skills -> $dst"
}

if ($OfficialInstaller) {
  Push-Location $root
  try {
    $agents = @()
    if ($Target -eq "Both" -or $Target -eq "OpenCode") { $agents += "opencode" }
    if ($Target -eq "Both" -or $Target -eq "Cursor") { $agents += "cursor" }
    $agentArgs = @()
    foreach ($a in $agents) { $agentArgs += @("-a", $a) }
    & npx skills@latest add mattpocock/skills @agentArgs -y --copy
  } finally {
    Pop-Location
  }
  Write-Host "OK: instalador oficial. Si falló por falta de git, usa -FromOpenCodeGlobal."
  exit 0
}

if ($Target -eq "Both" -or $Target -eq "OpenCode") {
  Copy-MattSkills (Join-Path $root ".opencode\skills")
}
if ($Target -eq "Both" -or $Target -eq "Cursor") {
  Copy-MattSkills (Join-Path $root ".cursor\skills")
}

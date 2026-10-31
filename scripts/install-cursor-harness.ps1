# Instala / repara el Apex Harness en este repo para Cursor.
# Idempotente: agents, rules, commands, skills Matt, MCP Engram.

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$cursor = Join-Path $root ".cursor"

Write-Host "== Apex Harness → Cursor =="
Write-Host "root: $root"

# 1) Estructura mínima
@(
  "agents", "rules", "commands", "skills"
) | ForEach-Object {
  New-Item -ItemType Directory -Force -Path (Join-Path $cursor $_) | Out-Null
}

$required = @(
  ".cursor\rules\apex-harness.mdc",
  ".cursor\rules\apex-roles.mdc",
  ".cursor\commands\harness.md",
  ".cursor\agents\apex-harness.md",
  ".cursor\agents\apex-dev.md",
  ".cursor\agents\apex-bug.md",
  ".cursor\agents\apex-verifier.md",
  ".cursor\skills\harness-core\SKILL.md",
  ".cursor\mcp.json"
)
$missing = @()
foreach ($rel in $required) {
  if (-not (Test-Path (Join-Path $root $rel))) { $missing += $rel }
}
if ($missing.Count) {
  throw "Faltan piezas del harness en el repo:`n - $($missing -join "`n - ")"
}

# 2) Skills Matt
& (Join-Path $PSScriptRoot "bootstrap-matt-skills.ps1") -Target Both -FromOpenCodeGlobal

# 3) MCP Engram (ruta absoluta si existe)
$engramCmd = Get-Command engram -ErrorAction SilentlyContinue
$engram = if ($engramCmd) { $engramCmd.Source } elseif (Test-Path "$env:USERPROFILE\bin\engram.exe") {
  "$env:USERPROFILE\bin\engram.exe"
} else { "engram" }

$mcpPath = Join-Path $cursor "mcp.json"
@{
  mcpServers = @{
    engram = @{
      command = $engram
      args    = @("mcp", "--tools=agent")
    }
  }
} | ConvertTo-Json -Depth 5 | Set-Content -Path $mcpPath -Encoding utf8

$matt = (Get-ChildItem (Join-Path $cursor "skills") -Directory | Where-Object { $_.Name -ne "harness-core" }).Count
Write-Host "OK agents: $((Get-ChildItem (Join-Path $cursor 'agents')).Count)"
Write-Host "OK rules:  $((Get-ChildItem (Join-Path $cursor 'rules')).Count)"
Write-Host "OK matt skills: $matt"
Write-Host "OK mcp engram: $engram"
Write-Host ""
Write-Host "Siguiente: reinicia Cursor (quit completo) y prueba /harness <tarea>."
Write-Host "Comprueba Settings → Tools & MCP → engram; subagentes apex-* en el catálogo."

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$bundledPython = "C:\Users\chu\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$pythonCommand = Get-Command $bundledPython, python, py -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $pythonCommand) {
  throw "Python was not found. Install Python or restore the bundled Codex runtime."
}
$port = 5190

Set-Location -LiteralPath $root
Write-Host "Serving JoyaVault Joyagoo Spreadsheet"
Write-Host "Open http://127.0.0.1:$port/en/"
Write-Host "Press Ctrl+C in this window to stop the preview server."

& $pythonCommand.Source (Join-Path $root "scripts/preview-server.py") --port $port

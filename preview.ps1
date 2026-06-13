$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$bundledPython = "C:\Users\chu\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$pythonCommand = Get-Command $bundledPython, python, py -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $pythonCommand) {
  throw "Python was not found. Install Python or restore the bundled Codex runtime."
}
$port = 5190

Set-Location -LiteralPath $root
Write-Host "Serving MaisonLooks Streetwear Spreadsheet"
Write-Host "Open http://127.0.0.1:$port/index.html"
Write-Host "Press Ctrl+C in this window to stop the preview server."

& $pythonCommand.Source -m http.server $port --bind 127.0.0.1 --directory $root

param(
  [ValidateSet('estimate','translate','build','verify')][string]$Action = 'estimate',
  [string[]]$Languages = @('de','fr','pt','pl','it','ar'),
  [int]$MaxCharacters = 0
)
$ErrorActionPreference = 'Stop'
$bundledPython = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$pythonCommand = if (Test-Path -LiteralPath $bundledPython) { $bundledPython } else { (Get-Command python -ErrorAction Stop).Source }
Push-Location $PSScriptRoot
try {
  if ($Action -eq 'verify') {
    foreach ($script in @('test-site-translation.py','test-locales.py')) {
      & $pythonCommand (Join-Path $PSScriptRoot "scripts/$script")
      if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
  } else {
    $arguments = @((Join-Path $PSScriptRoot 'scripts/translate-site.py'), $Action, '--languages') + $Languages
    if ($MaxCharacters -gt 0) { $arguments += @('--max-characters', "$MaxCharacters") }
    & $pythonCommand @arguments
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  }
} finally { Pop-Location }

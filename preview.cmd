@echo off
setlocal

set "ROOT=%~dp0"
set "BUNDLED_PYTHON=C:\Users\chu\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
set "PORT=5190"

if exist "%BUNDLED_PYTHON%" (
  set "PYTHON=%BUNDLED_PYTHON%"
) else (
  where python >nul 2>nul
  if not errorlevel 1 (
    set "PYTHON=python"
  ) else (
    where py >nul 2>nul
    if errorlevel 1 (
      echo Python was not found. Install Python or restore the bundled Codex runtime.
      exit /b 1
    )
    set "PYTHON=py"
  )
)

cd /d "%ROOT%"
echo Serving JoyaVault Joyagoo Spreadsheet
echo Open http://127.0.0.1:%PORT%/en/
echo Press Ctrl+C in this window to stop the preview server.
echo.

"%PYTHON%" "%ROOT%scripts\preview-server.py" --port %PORT%

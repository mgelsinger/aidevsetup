$ErrorActionPreference = 'Stop'
$venvPy = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $venvPy)) {
  Write-Host "No .venv found. Run .\bootstrap.ps1 first." -ForegroundColor Red
  exit 1
}
# Run uvicorn with reload
& $venvPy -m uvicorn app.server:app --reload --host 127.0.0.1 --port 8000
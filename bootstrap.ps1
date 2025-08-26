Param(
  [switch]$Force
)

$ErrorActionPreference = 'Stop'

Write-Host "=== AI Dev Sandbox — Bootstrap ===" -ForegroundColor Cyan

# 1) Ensure Python
$python = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $python) {
  Write-Host "Python not found on PATH. Please install Python 3.10+ and re-run." -ForegroundColor Red
  exit 1
}

# 2) Create .venv if missing
if (Test-Path .\.venv) {
  if ($Force) {
    Write-Host "Removing existing .venv due to -Force..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .\.venv
  } else {
    Write-Host ".venv already exists. Skipping venv creation." -ForegroundColor Yellow
  }
}

if (-not (Test-Path .\.venv)) {
  Write-Host "Creating virtual environment (.venv)..." -ForegroundColor Cyan
  python -m venv .venv
}

# 3) Upgrade pip & install deps
$pip = ".\.venv\Scripts\python.exe"
& $pip -m pip install --upgrade pip
if (Test-Path .\requirements.txt) {
  Write-Host "Installing requirements..." -ForegroundColor Cyan
  & $pip -m pip install -r .\requirements.txt
} else {
  Write-Host "requirements.txt not found (this template expects it)." -ForegroundColor Red
  exit 1
}

# 4) Ensure .env
if (-not (Test-Path .\.env)) {
  if (Test-Path .\.env.example) {
    Copy-Item .\.env.example .\.env
    Write-Host "Created .env from .env.example — edit it to choose provider and models." -ForegroundColor Green
  } else {
    Write-Host ".env.example missing. Create a .env file with provider settings." -ForegroundColor Yellow
  }
} else {
  Write-Host ".env already present — leaving it as-is." -ForegroundColor Yellow
}

Write-Host "`nAll set. To start the API server:" -ForegroundColor Green
Write-Host "  .\run.ps1" -ForegroundColor Green
Write-Host "`nTo test the chat endpoint:" -ForegroundColor Green
Write-Host "  .\test.ps1" -ForegroundColor Green
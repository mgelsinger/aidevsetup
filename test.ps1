$ErrorActionPreference = 'Stop'
$payload = @{
  messages = @(
    @{ role = "user"; content = "Say 'pong' if you can hear me." }
  )
} | ConvertTo-Json -Depth 5

try {
  $res = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/v1/chat" -ContentType "application/json" -Body $payload
  $res | ConvertTo-Json -Depth 10
}
catch {
  Write-Host "Request failed. Is the server running? Try: .\run.ps1" -ForegroundColor Red
  throw
}
$ErrorActionPreference = "Stop"

$ExpectedContainerName = "ai_decision_app"

Write-Host "Checking port 8000..."

# 1) Docker container check: another container must not be holding port 8000
$portOwner = docker ps --filter "publish=8000" --format "{{.Names}}" | Select-Object -First 1
if ($portOwner -and $portOwner -ne $ExpectedContainerName) {
    throw "Port 8000 is already published by container '$portOwner'. Stop it with 'docker stop $portOwner' before starting the standard demo (expected container: '$ExpectedContainerName')."
}

# 2) Host process check: a stale uvicorn/python on the host can hijack 127.0.0.1:8000
# even when docker compose appears to start successfully.
$hostListener = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue |
    Where-Object { $_.OwningProcess -ne 0 } |
    Select-Object -First 1

if ($hostListener) {
    $proc = Get-Process -Id $hostListener.OwningProcess -ErrorAction SilentlyContinue
    $procName = if ($proc) { $proc.ProcessName } else { "pid=$($hostListener.OwningProcess)" }
    # Docker's own listener also shows up here; ignore it.
    if ($procName -notmatch "com\.docker|vpnkit|docker") {
        throw "A host process ($procName, pid=$($hostListener.OwningProcess)) is already listening on port 8000. Stop it before running the demo so that localhost and 127.0.0.1 both resolve to the demo backend."
    }
}

Write-Host "Starting containers..."
docker compose up --build -d

Write-Host "Waiting for db to be healthy..."
do {
    Start-Sleep -Seconds 2
    $status = docker inspect -f "{{.State.Health.Status}}" ai_decision_db 2>$null
} while ($status -ne "healthy")

Write-Host "Running migrations..."
docker compose exec app alembic upgrade head

Write-Host "Running demo smoke check..."
& .\scripts\demo_smoke_check.ps1 -BaseUrl "http://localhost:8000"

Write-Host "API docs: http://localhost:8000/docs"

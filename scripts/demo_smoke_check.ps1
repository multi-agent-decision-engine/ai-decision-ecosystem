param(
    [string]$BaseUrl = "http://localhost:8000",
    [string]$DemoScenarioName = "[Demo] Final Smoke Scenario"
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "[demo-check] $Message"
}

Write-Step "Checking backend health at $BaseUrl/health"
$health = Invoke-RestMethod -Method Get -Uri "$BaseUrl/health"
if ($health.status -ne "healthy") {
    throw "Health endpoint did not return healthy status."
}

# Idempotent demo scenario seed.
# Presenter must be able to open the frontend, see a *known* demo scenario by
# name and start a simulation without opening Swagger. So instead of "create
# only when DB is totally empty", we always ensure the named demo scenario
# exists (ISSUE-003).
Write-Step "Ensuring demo scenario '$DemoScenarioName' exists"
$pageSize = 100
$offset = 0
$existing = $null
do {
    $page = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/scenarios?limit=$pageSize&offset=$offset"
    if ($page.items) {
        $existing = $page.items | Where-Object { $_.name -eq $DemoScenarioName } | Select-Object -First 1
        if ($existing) { break }
    }
    $offset += $pageSize
} while ($page.items -and $page.items.Count -eq $pageSize)

if ($existing) {
    Write-Step "Found existing demo scenario (id=$($existing.id)); reusing"
    $scenarioId = $existing.id
} else {
    Write-Step "Creating demo scenario '$DemoScenarioName'"
    $body = @{
        name = $DemoScenarioName
        description = "Idempotent demo scenario seeded by scripts/demo_smoke_check.ps1 so the presenter can run a known simulation from the frontend without Swagger."
        budget_million_usd = 5.0
        expected_roi_percent = 30.0
        risk_level = 5
        team_readiness = 7
    } | ConvertTo-Json

    $created = Invoke-RestMethod `
        -Method Post `
        -Uri "$BaseUrl/api/v1/scenarios" `
        -Body $body `
        -ContentType "application/json"

    $scenarioId = $created.scenario_id
}

Write-Step "Running simulation for scenario $scenarioId"
$elapsed = Measure-Command {
    $simulation = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/scenarios/$scenarioId/simulate"
}

if (-not $simulation.final_decision) {
    throw "Simulation response did not include final_decision."
}

Write-Step "Simulation OK: decision=$($simulation.final_decision), score=$($simulation.final_score), seconds=$([math]::Round($elapsed.TotalSeconds, 2))"
Write-Step "Demo smoke check passed (demo scenario '$DemoScenarioName' ready for frontend)"

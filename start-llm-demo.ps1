# Bonus LLM Demo Launcher
#
# Ana (standart) demo deterministik agentlarla calisir; bkz. start.ps1.
# Bu script LLM modunu AYRI bir container'da (`ai_decision_app_llm`) ve AYRI bir
# portta (varsayilan 8010) ayaga kaldirir; standart demo ile ayni anda calisabilir.
# Demo oncesi Ollama isitilir ve LLM-aware smoke check zorunlu calisir.
#
# Kullanim:
#   .\start-llm-demo.ps1                       # varsayilan port 8010, model qwen2.5:7b
#   .\start-llm-demo.ps1 -HostPort 8010 -Model qwen2.5:7b

param(
    [int]   $HostPort       = 8010,
    [string]$Model          = "qwen2.5:7b",
    [string]$OllamaBaseUrl  = "http://localhost:11434",
    [string]$ContainerName  = "ai_decision_app_llm",
    [string]$Network        = "multiagent_default",
    [string]$ImageName      = "multiagent-app"
)

$ErrorActionPreference = "Stop"

Write-Host "[llm-demo] Bonus LLM demo starting (port=$HostPort, model=$Model)"

# 0) Standart demo (deterministik) ayakta degilse uyari — DB ve image gerekli.
$standardUp = docker ps --filter "name=^ai_decision_app$" --format "{{.Names}}" | Select-Object -First 1
if (-not $standardUp) {
    Write-Host "[llm-demo] WARN: 'ai_decision_app' (deterministik) container ayakta degil. Once .\start.ps1 calistirin (DB ve image bu sayede hazirlanir)."
    throw "Standart demo container'i bulunamadi. LLM bonus demo, mevcut DB + image uzerinde calisir."
}

# 1) Port cakismasi kontrolu
$portOwner = docker ps --filter "publish=$HostPort" --format "{{.Names}}" | Select-Object -First 1
if ($portOwner -and $portOwner -ne $ContainerName) {
    throw "Port $HostPort container '$portOwner' tarafindan tutuluyor. Once durdurun ya da farkli -HostPort kullanin."
}

# 2) Eski LLM container'ini temizle (idempotent)
$existing = docker ps -a --filter "name=^$ContainerName$" --format "{{.Names}}" | Select-Object -First 1
if ($existing) {
    Write-Host "[llm-demo] Removing previous '$ContainerName'"
    docker rm -f $ContainerName | Out-Null
}

# 3) LLM container'ini ayri portta baslat
Write-Host "[llm-demo] Launching LLM container on port $HostPort"
docker run -d `
    --name $ContainerName `
    --network $Network `
    -p "${HostPort}:8000" `
    -e DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/ai_decision_engine `
    -e MADE_USE_LLM=1 `
    -e MADE_LLM_MODEL=$Model `
    -e OLLAMA_BASE_URL=http://host.docker.internal:11434 `
    --add-host=host.docker.internal:host-gateway `
    $ImageName | Out-Null

# 4) Health beklemesi
Write-Host "[llm-demo] Waiting for LLM backend health on port $HostPort"
$ready = $false
for ($i = 0; $i -lt 30; $i++) {
    try {
        $h = Invoke-RestMethod -Method Get -Uri "http://localhost:$HostPort/health" -TimeoutSec 3
        if ($h.status -eq "healthy") { $ready = $true; break }
    } catch { Start-Sleep -Seconds 2 }
}
if (-not $ready) {
    docker logs --tail 50 $ContainerName
    throw "LLM backend $HostPort uzerinde 60 saniye icinde healthy olmadi."
}

# 5) Ollama isitma + smoke check
Write-Host "[llm-demo] Running LLM smoke check (warms Ollama and exercises one simulation)"
& .\scripts\llm_smoke_check.ps1 `
    -BaseUrl "http://localhost:$HostPort" `
    -OllamaBaseUrl $OllamaBaseUrl `
    -OllamaModel $Model

Write-Host "[llm-demo] Bonus LLM demo ready at http://localhost:$HostPort/docs"

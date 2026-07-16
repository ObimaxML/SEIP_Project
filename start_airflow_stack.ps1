Param()

$envFile = Join-Path $PSScriptRoot '.env'
$exampleFile = Join-Path $PSScriptRoot '.env.example'

if (-not (Test-Path $envFile)) {
    Write-Host ".env not found. Copying .env.example to .env..."
    Copy-Item -Path $exampleFile -Destination $envFile -Force
    Write-Host "Please review and update .env before continuing, especially POPIA and Airflow secrets."
}

Write-Host "Starting Docker Compose stack..."
docker compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker Compose failed to start. Check output above."
    exit 1
}

Write-Host "Tailing db-init, airflow-webserver, and airflow-scheduler logs..."
docker compose logs --follow db-init airflow-webserver airflow-scheduler

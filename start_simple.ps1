# iStock Simple Startup Script (PowerShell)
# No Chinese characters, no encoding issues

Write-Host "========================================"
Write-Host "iStock Simple Startup Script"
Write-Host "========================================"
Write-Host ""

# Step 1: Check current directory
Write-Host "Step 1: Checking current directory..." -ForegroundColor Cyan
if (-not (Test-Path "docker-compose.yml")) {
    Write-Host "ERROR: Not in iStock project directory!" -ForegroundColor Red
    Write-Host "Current directory: $PWD"
    Write-Host "Please navigate to the iStock project folder."
    pause
    exit 1
}
Write-Host "OK: In iStock project directory" -ForegroundColor Green
Write-Host ""

# Step 2: Check Docker Desktop
Write-Host "Step 2: Checking Docker Desktop..." -ForegroundColor Cyan
$dockerProcess = Get-Process | Where-Object { $_.ProcessName -like "*docker*" }
if (-not $dockerProcess) {
    Write-Host "WARNING: Docker Desktop may not be running" -ForegroundColor Yellow
    Write-Host "Please ensure Docker Desktop is started"
    Write-Host ""
    
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne "y") {
        Write-Host "Exiting..."
        pause
        exit 1
    }
} else {
    Write-Host "OK: Docker Desktop processes detected" -ForegroundColor Green
}
Write-Host ""

# Step 3: Find Docker executable
Write-Host "Step 3: Finding Docker executable..." -ForegroundColor Cyan
$dockerPath = $null

# Check common installation paths
$possiblePaths = @(
    "C:\Program Files\Docker\Docker\resources\bin\docker.exe",
    "$env:LOCALAPPDATA\Docker\resources\bin\docker.exe"
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $dockerPath = Split-Path $path -Parent
        Write-Host "Found Docker at: $dockerPath" -ForegroundColor Green
        break
    }
}

if (-not $dockerPath) {
    Write-Host "ERROR: Could not find Docker executable" -ForegroundColor Red
    Write-Host "Please ensure Docker Desktop is properly installed."
    Write-Host "Paths checked:"
    $possiblePaths | ForEach-Object { Write-Host "  $_" }
    pause
    exit 1
}

# Step 4: Test Docker command
Write-Host "Step 4: Testing Docker command..." -ForegroundColor Cyan
try {
    & "$dockerPath\docker.exe" --version
    Write-Host "OK: Docker command works" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Docker command failed" -ForegroundColor Red
    Write-Host "Docker Desktop may not be fully started"
    pause
    exit 1
}
Write-Host ""

# Step 5: Use fixed docker-compose file
Write-Host "Step 5: Preparing docker-compose..." -ForegroundColor Cyan
if (Test-Path "docker-compose-fixed.yml") {
    Copy-Item "docker-compose-fixed.yml" "docker-compose.yml" -Force
    Write-Host "Using fixed docker-compose with Chinese mirrors" -ForegroundColor Green
} else {
    Write-Host "Using original docker-compose.yml" -ForegroundColor Yellow
}
Write-Host ""

# Step 6: Stop existing services
Write-Host "Step 6: Stopping existing services..." -ForegroundColor Cyan
try {
    & "$dockerPath\docker.exe" compose down 2>$null
    Write-Host "OK: Services stopped (if any were running)" -ForegroundColor Green
} catch {
    Write-Host "Could not stop services (maybe none running)" -ForegroundColor Yellow
}
Write-Host ""

# Step 7: Start core services
Write-Host "Step 7: Starting core services..." -ForegroundColor Cyan
Write-Host "This may take several minutes. Please be patient..." -ForegroundColor Yellow
Write-Host ""

try {
    & "$dockerPath\docker.exe" compose up -d postgres redis backend
    Write-Host "OK: Core services started" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to start services" -ForegroundColor Red
    Write-Host "Error: $_"
    Write-Host ""
    Write-Host "Trying alternative: start minimal version..."
    Start-MinimalVersion
}
Write-Host ""

# Step 8: Wait for startup
Write-Host "Step 8: Waiting for startup (30 seconds)..." -ForegroundColor Cyan
Write-Host "Please wait for services to fully start..." -ForegroundColor Yellow
Start-Sleep -Seconds 30
Write-Host ""

# Step 9: Check service status
Write-Host "Step 9: Checking service status..." -ForegroundColor Cyan
try {
    & "$dockerPath\docker.exe" compose ps
} catch {
    Write-Host "Could not get service status" -ForegroundColor Yellow
}
Write-Host ""

# Show completion information
Write-Host "========================================" -ForegroundColor Green
Write-Host "STARTUP COMPLETED" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "What to do next:" -ForegroundColor Cyan
Write-Host "1. Wait 1-2 minutes for full startup"
Write-Host "2. Open browser and test:"
Write-Host "   - Backend API: http://localhost:8000/health"
Write-Host "   - API Docs:    http://localhost:8000/docs"
Write-Host "   - Frontend:    http://localhost:3000"
Write-Host ""
Write-Host "3. If services aren't running:"
Write-Host "   - Check Docker Desktop is fully started"
Write-Host "   - Wait 2-3 minutes"
Write-Host "   - Run: docker-compose logs"
Write-Host ""
Write-Host "4. For detailed troubleshooting:"
Write-Host "   - Read MANUAL_TEST_GUIDE.md"
Write-Host "   - Read FIX_DOCKER_PATH.md"
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
pause

function Start-MinimalVersion {
    Write-Host "Starting minimal version (backend only)..." -ForegroundColor Cyan
    
    # Build backend image
    Write-Host "Building backend image..." -ForegroundColor Cyan
    try {
        & "$dockerPath\docker.exe" build -f Dockerfile.backend -t istock-backend .
        Write-Host "OK: Backend image built" -ForegroundColor Green
    } catch {
        Write-Host "WARNING: Failed to build backend image" -ForegroundColor Yellow
        Write-Host "Trying to run existing image..." -ForegroundColor Yellow
    }
    
    # Start backend container
    Write-Host "Starting backend container..." -ForegroundColor Cyan
    try {
        & "$dockerPath\docker.exe" run -d --name istock-backend `
          -p 8000:8000 `
          -v "$PWD\backend:/app/backend" `
          -v "$PWD\local:/app/local" `
          -e DATABASE_URL=sqlite:///./istock.db `
          -e DEBUG=true `
          istock-backend `
          sh -c "python -m uvicorn backend.src.api.main:app --host 0.0.0.0 --port 8000 --reload"
        
        Write-Host "OK: Backend container started" -ForegroundColor Green
        Write-Host "Container name: istock-backend" -ForegroundColor Gray
        Write-Host "Port: 8000" -ForegroundColor Gray
    } catch {
        Write-Host "ERROR: Could not start backend container" -ForegroundColor Red
        Write-Host ""
        Write-Host "Alternative: Run local Python development" -ForegroundColor Yellow
        Write-Host "cd backend" -ForegroundColor Gray
        Write-Host "python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload" -ForegroundColor Gray
    }
}
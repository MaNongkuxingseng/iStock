# iStock Quick Test Script
Write-Host "iStock Quick Test" -ForegroundColor Green
Write-Host "================" -ForegroundColor Green
Write-Host ""

# 1. Check current directory
Write-Host "1. Checking current directory..." -ForegroundColor Yellow
if (Test-Path "docker-compose.yml") {
    Write-Host "   OK: In iStock project directory" -ForegroundColor Green
} else {
    Write-Host "   ERROR: Not in iStock directory!" -ForegroundColor Red
    Write-Host "   Current: $PWD" -ForegroundColor Yellow
    exit 1
}

# 2. Check essential files
Write-Host "`n2. Checking essential files..." -ForegroundColor Yellow
$essentialFiles = @(
    "docker-compose.yml",
    "backend/src/database/models.py",
    "Dockerfile.backend",
    "Dockerfile.frontend",
    ".env.example"
)

foreach ($file in $essentialFiles) {
    if (Test-Path $file) {
        Write-Host "   OK: $file" -ForegroundColor Green
    } else {
        Write-Host "   WARNING: $file missing" -ForegroundColor Yellow
    }
}

# 3. Check frontend directory
Write-Host "`n3. Checking frontend directory..." -ForegroundColor Yellow
if (Test-Path "frontend") {
    $frontendFiles = Get-ChildItem "frontend" -File
    if ($frontendFiles.Count -gt 0) {
        Write-Host "   OK: Frontend directory has $($frontendFiles.Count) files" -ForegroundColor Green
        $frontendFiles | Select-Object -First 5 | ForEach-Object {
            Write-Host "     - $($_.Name)" -ForegroundColor Gray
        }
    } else {
        Write-Host "   CRITICAL: Frontend directory is empty!" -ForegroundColor Red
    }
} else {
    Write-Host "   CRITICAL: Frontend directory missing!" -ForegroundColor Red
}

# 4. Check Docker (if available)
Write-Host "`n4. Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    if ($dockerVersion) {
        Write-Host "   OK: Docker found: $dockerVersion" -ForegroundColor Green
    } else {
        Write-Host "   WARNING: Docker command not found in PATH" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   WARNING: Docker check failed" -ForegroundColor Yellow
}

# 5. Check project structure
Write-Host "`n5. Checking project structure..." -ForegroundColor Yellow
$directories = @("backend", "frontend", "docker", "scripts", "data")
foreach ($dir in $directories) {
    if (Test-Path $dir) {
        $itemCount = (Get-ChildItem $dir -Recurse -File | Measure-Object).Count
        Write-Host "   $dir : $itemCount files" -ForegroundColor Gray
    } else {
        Write-Host "   $dir : MISSING" -ForegroundColor Yellow
    }
}

# 6. Check scripts
Write-Host "`n6. Checking test scripts..." -ForegroundColor Yellow
$testScripts = @(
    "scripts/check_status.py",
    "backend/scripts/test_database.py",
    "backend/scripts/seed_data.py"
)

foreach ($script in $testScripts) {
    if (Test-Path $script) {
        Write-Host "   OK: $script" -ForegroundColor Green
    } else {
        Write-Host "   WARNING: $script missing" -ForegroundColor Yellow
    }
}

Write-Host "`n" + "="*50 -ForegroundColor Green
Write-Host "TEST COMPLETE" -ForegroundColor Green
Write-Host "="*50 -ForegroundColor Green

Write-Host "`nSummary:" -ForegroundColor Yellow
Write-Host "1. Project structure: " -NoNewline
if (Test-Path "docker-compose.yml" -and (Test-Path "backend/src/database/models.py")) {
    Write-Host "OK" -ForegroundColor Green
} else {
    Write-Host "PROBLEMS" -ForegroundColor Red
}

Write-Host "2. Frontend: " -NoNewline
if (Test-Path "frontend" -and ((Get-ChildItem "frontend" -File).Count -gt 0)) {
    Write-Host "OK" -ForegroundColor Green
} else {
    Write-Host "CRITICAL - Directory empty!" -ForegroundColor Red
}

Write-Host "3. Docker: " -NoNewline
try {
    if (docker --version 2>$null) {
        Write-Host "Available" -ForegroundColor Green
    } else {
        Write-Host "Not in PATH" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Unknown" -ForegroundColor Yellow
}

Write-Host "`nCritical Issues Found:" -ForegroundColor Red
if (-not (Test-Path "frontend") -or ((Get-ChildItem "frontend" -File).Count -eq 0)) {
    Write-Host "• Frontend directory is empty or missing" -ForegroundColor Red
    Write-Host "  This will prevent Docker from building frontend service" -ForegroundColor Yellow
}

Write-Host "`nRecommendations:" -ForegroundColor Cyan
Write-Host "1. Check if frontend source code exists elsewhere" -ForegroundColor White
Write-Host "2. If missing, you may need to:" -ForegroundColor White
Write-Host "   a) Create a simple React app in frontend/" -ForegroundColor White
Write-Host "   b) Or update docker-compose.yml to skip frontend" -ForegroundColor White
Write-Host "3. Ensure Docker Desktop is running and in PATH" -ForegroundColor White

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
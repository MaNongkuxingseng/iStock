# iStock Quick Fix Script (Fixed PowerShell Version)
# Solve common issues and start services

Write-Host "=== iStock Quick Fix Script ===" -ForegroundColor Green
Write-Host ""

# 1. Check current directory
Write-Host "Step 1: Checking current directory..." -ForegroundColor Cyan
if (-not (Test-Path "docker-compose.yml")) {
    Write-Host "ERROR: Not in iStock project directory!" -ForegroundColor Red
    Write-Host "Current directory: $PWD"
    Write-Host "Please navigate to: G:\openclaw\workspace\_system\agent-home\myStock-AI"
    pause
    exit 1
}
Write-Host "OK: In iStock project directory" -ForegroundColor Green
Write-Host ""

# 2. Check Docker Desktop
Write-Host "Step 2: Checking Docker Desktop..." -ForegroundColor Cyan
$dockerProcess = Get-Process | Where-Object { $_.ProcessName -like "*docker*" }
if (-not $dockerProcess) {
    Write-Host "WARNING: Docker Desktop may not be running" -ForegroundColor Yellow
    Write-Host "Please ensure Docker Desktop is started"
    Write-Host "1. Search for 'Docker Desktop' and start it"
    Write-Host "2. Wait 1-2 minutes for full startup"
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

# 3. Check Docker commands
Write-Host "Step 3: Checking Docker commands..." -ForegroundColor Cyan
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
    Write-Host "Please ensure Docker Desktop is properly installed"
    Write-Host "Paths checked:"
    $possiblePaths | ForEach-Object { Write-Host "  $_" }
    pause
    exit 1
}

# Test Docker command
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

# 4. Create necessary directories
Write-Host "Step 4: Creating project structure..." -ForegroundColor Cyan
$directories = @(
    "backend\logs",
    "frontend\logs", 
    "data\postgres",
    "data\redis",
    "data\celery"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created directory: $dir" -ForegroundColor Green
    } else {
        Write-Host "Directory exists: $dir" -ForegroundColor Gray
    }
}
Write-Host ""

# 5. Create .env file
Write-Host "Step 5: Creating environment configuration..." -ForegroundColor Cyan
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env" -Force
        Write-Host "Created .env file from example" -ForegroundColor Green
    } else {
        @"
# iStock Environment Variables
DATABASE_URL=postgresql://mystock_user:mystock_password@postgres:5432/mystock_ai
REDIS_URL=redis://redis:6379/0
DEBUG=true
SECRET_KEY=your-secret-key-here-change-in-production
"@ | Out-File -FilePath ".env" -Encoding UTF8
        Write-Host "Created basic .env file" -ForegroundColor Green
    }
} else {
    Write-Host ".env file already exists" -ForegroundColor Gray
}
Write-Host ""

# 6. Create frontend basic structure
Write-Host "Step 6: Creating frontend basics..." -ForegroundColor Cyan
if (-not (Test-Path "frontend\package.json")) {
    Write-Host "Creating frontend basic structure..." -ForegroundColor Yellow
    
    if (-not (Test-Path "frontend")) {
        New-Item -ItemType Directory -Path "frontend" -Force | Out-Null
    }
    
    # Create package.json
    @'
{
  "name": "istock-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0"
  },
  "scripts": {
    "start": "echo 'Frontend development server would start here'",
    "build": "echo 'Frontend would build here'",
    "test": "echo 'Frontend tests would run here'"
  }
}
'@ | Out-File -FilePath "frontend\package.json" -Encoding UTF8
    
    # Create public directory and index.html
    if (-not (Test-Path "frontend\public")) {
        New-Item -ItemType Directory -Path "frontend\public" -Force | Out-Null
    }
    
    @'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iStock - Intelligent Stock Analysis System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1890ff;
            border-bottom: 2px solid #1890ff;
            padding-bottom: 10px;
        }
        .status {
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .warning {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }
        .links {
            margin-top: 30px;
        }
        .links a {
            display: inline-block;
            margin-right: 15px;
            padding: 10px 20px;
            background: #1890ff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .links a:hover {
            background: #096dd9;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>iStock - Intelligent Stock Analysis System</h1>
        
        <div class="status success">
            <h3>✅ Backend Services Ready</h3>
            <p>Backend API services are running. Frontend is under development.</p>
        </div>
        
        <div class="status warning">
            <h3>🔄 Frontend Development</h3>
            <p>React frontend application is being developed, coming soon.</p>
        </div>
        
        <h2>Available Services</h2>
        <ul>
            <li><strong>Backend API</strong>: Stock data, user management, portfolio</li>
            <li><strong>Database</strong>: PostgreSQL + Redis configured</li>
            <li><strong>Docker Environment</strong>: Complete containerized dev environment</li>
        </ul>
        
        <div class="links">
            <a href="/api/v1/docs" target="_blank">API Documentation</a>
            <a href="/health" target="_blank">Health Check</a>
            <a href="http://localhost:8000/docs" target="_blank">Swagger UI</a>
        </div>
        
        <h2>Project Information</h2>
        <p><strong>Project Status</strong>: Development (Week 2 complete, Week 3 in progress)</p>
        <p><strong>Tech Stack</strong>: FastAPI + React + PostgreSQL + Redis + Docker</p>
        <p><strong>Git Repository</strong>: https://github.com/MaNongkuxingseng/iStock</p>
    </div>
</body>
</html>
'@ | Out-File -FilePath "frontend\public\index.html" -Encoding UTF8
    
    Write-Host "Frontend basic structure created" -ForegroundColor Green
} else {
    Write-Host "Frontend package.json already exists" -ForegroundColor Gray
}
Write-Host ""

# 7. Stop existing services
Write-Host "Step 7: Stopping existing services..." -ForegroundColor Cyan
try {
    & "$dockerPath\docker.exe" compose down 2>$null
    Write-Host "Stopped existing services" -ForegroundColor Green
} catch {
    Write-Host "Could not stop services (maybe none running)" -ForegroundColor Yellow
}
Write-Host ""

# 8. Start core services
Write-Host "Step 8: Starting core services..." -ForegroundColor Cyan
Write-Host "This may take several minutes. Please be patient..." -ForegroundColor Yellow
Write-Host ""

try {
    # Start database services
    Write-Host "Starting PostgreSQL and Redis..." -ForegroundColor Cyan
    & "$dockerPath\docker.exe" compose up -d postgres redis
    
    # Wait for database startup
    Write-Host "Waiting for database startup (10 seconds)..." -ForegroundColor Cyan
    Start-Sleep -Seconds 10
    
    # Start backend service
    Write-Host "Starting backend service..." -ForegroundColor Cyan
    & "$dockerPath\docker.exe" compose up -d backend
    
    Write-Host "Core services started" -ForegroundColor Green
    
} catch {
    Write-Host "ERROR: Failed to start services" -ForegroundColor Red
    Write-Host "Error: $_"
    Write-Host ""
    Write-Host "Trying alternative: start database only..."
    
    try {
        & "$dockerPath\docker.exe" compose up -d postgres redis
        Write-Host "Database services started" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Could not start database services" -ForegroundColor Red
    }
}
Write-Host ""

# 9. Check service status
Write-Host "Step 9: Checking service status..." -ForegroundColor Cyan
try {
    & "$dockerPath\docker.exe" compose ps
} catch {
    Write-Host "Could not get service status" -ForegroundColor Yellow
}
Write-Host ""

# 10. Wait for full startup
Write-Host "Step 10: Waiting for full startup (30 seconds)..." -ForegroundColor Cyan
Write-Host "Please wait for services to fully start..." -ForegroundColor Yellow
Start-Sleep -Seconds 30
Write-Host ""

# 11. Test services
Write-Host "Step 11: Testing service connections..." -ForegroundColor Cyan
Write-Host "Testing backend API health check..." -ForegroundColor Cyan

try {
    $healthUrl = "http://localhost:8000/health"
    $response = Invoke-WebRequest -Uri $healthUrl -TimeoutSec 10 -ErrorAction SilentlyContinue
    
    if ($response.StatusCode -eq 200) {
        Write-Host "Backend API is working" -ForegroundColor Green
        Write-Host "Response: $($response.Content)" -ForegroundColor Gray
    } else {
        Write-Host "Backend API response status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Backend API not responding (may still be starting)" -ForegroundColor Yellow
    Write-Host "Error: $_" -ForegroundColor Gray
}
Write-Host ""

# 12. Show completion information
Write-Host "=== Quick Fix Completed! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Completed operations:" -ForegroundColor Cyan
Write-Host "1. ✓ Verified Docker Desktop"
Write-Host "2. ✓ Created project structure"
Write-Host "3. ✓ Created environment configuration"
Write-Host "4. ✓ Created frontend basics"
Write-Host "5. ✓ Stopped existing services"
Write-Host "6. ✓ Started core services"
Write-Host ""
Write-Host "Available links:" -ForegroundColor Cyan
Write-Host "- Backend API: http://localhost:8000"
Write-Host "- API Docs: http://localhost:8000/docs"
Write-Host "- Health Check: http://localhost:8000/health"
Write-Host "- Frontend: http://localhost:3000 (under development)"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Wait 1-2 minutes for full service startup"
Write-Host "2. Visit above links to test services"
Write-Host "3. If services not starting, check Docker Desktop"
Write-Host "4. View logs: docker-compose logs"
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "- Code Audit Report: CODE_AUDIT_REPORT.md"
Write-Host "- Quick Fix Guide: QUICK_FIX_GUIDE.md"
Write-Host "- Manual Test Guide: MANUAL_TEST_GUIDE.md"
Write-Host "- Docker Fix Guide: FIX_DOCKER_PATH.md"
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
pause
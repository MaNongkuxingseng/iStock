@echo off
echo iStock Core Verification
echo ========================
echo.

echo 1. Checking essential files...
if exist "docker-compose.yml" (
    echo OK: docker-compose.yml found
) else (
    echo ERROR: docker-compose.yml missing!
    pause
    exit /b 1
)

if exist "backend\src\database\models.py" (
    echo OK: Database models found
) else (
    echo ERROR: Database models missing!
    pause
    exit /b 1
)

if exist "frontend\package.json" (
    echo OK: Frontend package.json found
) else (
    echo WARNING: Frontend package.json missing
)

echo.
echo 2. Checking Docker...
docker --version
if errorlevel 1 (
    echo ERROR: Docker not found!
    pause
    exit /b 1
)

docker info >nul
if errorlevel 1 (
    echo ERROR: Docker daemon not running!
    pause
    exit /b 1
)

echo.
echo 3. Checking Docker Compose...
docker-compose --version
if errorlevel 1 (
    docker compose version
    if errorlevel 1 (
        echo ERROR: Docker Compose not found!
        pause
        exit /b 1
    )
    echo OK: docker compose found
) else (
    echo OK: docker-compose found
)

echo.
echo 4. Testing basic Docker commands...
echo Listing containers:
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | findstr /v "NAMES" || echo No containers found

echo.
echo 5. Testing project scripts...
if exist "scripts\check_status.py" (
    echo OK: Status check script found
) else (
    echo WARNING: Status check script missing
)

if exist "backend\scripts\test_database.py" (
    echo OK: Database test script found
) else (
    echo WARNING: Database test script missing
)

echo.
echo 6. Quick service test...
echo Starting minimal services (PostgreSQL + Redis)...
docker-compose up -d postgres redis 2>nul

if errorlevel 1 (
    echo ERROR: Failed to start services
) else (
    echo OK: Services started
    timeout /t 5 /nobreak >nul
    
    echo Checking service status...
    docker-compose ps
)

echo.
echo ========================
echo VERIFICATION COMPLETE
echo ========================
echo.
echo If all checks passed, you can:
echo 1. Run: docker-compose up -d
echo 2. Wait 2-3 minutes
echo 3. Test: http://localhost:8000/health
echo.
echo For problems:
echo 1. Run: emergency_fix.bat
echo 2. Read: MANUAL_TEST_GUIDE.md
echo.
pause
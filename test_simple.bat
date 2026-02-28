@echo off
echo iStock Simple Test Script
echo =========================
echo.

REM Check if we're in the right directory
if not exist "docker-compose.yml" (
    echo ERROR: Not in iStock project directory
    echo Please run from directory containing docker-compose.yml
    pause
    exit /b 1
)

echo 1. Checking Docker...
docker --version
if errorlevel 1 (
    echo ERROR: Docker not found
    pause
    exit /b 1
)
echo OK: Docker found

echo.
echo 2. Checking Docker Compose...
docker-compose --version
if errorlevel 1 (
    echo WARNING: docker-compose not found, trying docker compose...
    docker compose version
    if errorlevel 1 (
        echo ERROR: Docker Compose not found
        pause
        exit /b 1
    )
    echo OK: docker compose found
) else (
    echo OK: docker-compose found
)

echo.
echo 3. Checking Docker daemon...
docker info >nul
if errorlevel 1 (
    echo ERROR: Docker daemon not running
    echo Please start Docker Desktop
    pause
    exit /b 1
)
echo OK: Docker daemon running

echo.
echo 4. Testing basic Docker commands...
echo Listing Docker images:
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | findstr /i "postgres redis python node" || echo No relevant images found

echo.
echo 5. Testing project structure...
if exist "backend\src\database\models.py" (
    echo OK: Backend models found
) else (
    echo WARNING: Backend models not found
)

if exist "frontend\package.json" (
    echo OK: Frontend package.json found
) else (
    echo WARNING: Frontend package.json not found
)

if exist ".env.example" (
    echo OK: Environment example found
) else (
    echo WARNING: .env.example not found
)

echo.
echo 6. Testing Python scripts...
if exist "backend\scripts\test_database.py" (
    echo OK: Database test script found
) else (
    echo WARNING: Database test script not found
)

echo.
echo =========================
echo TEST COMPLETE
echo =========================
echo.
echo Next steps:
echo 1. Run: docker-compose up -d
echo 2. Wait 1-2 minutes for services to start
echo 3. Test: http://localhost:8000/health
echo 4. Test: http://localhost:3000
echo.
pause
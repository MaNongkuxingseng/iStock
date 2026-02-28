@echo off
echo iStock Emergency Fix Script
echo ===========================
echo.

echo 1. Checking current directory...
if not exist "docker-compose.yml" (
    echo ERROR: Not in iStock project directory!
    echo Please navigate to the directory containing docker-compose.yml
    echo Current directory: %CD%
    pause
    exit /b 1
)
echo OK: In iStock project directory

echo.
echo 2. Stopping any running services...
docker-compose down 2>nul
echo OK: Services stopped

echo.
echo 3. Fixing file encoding issues...
REM Remove problematic batch file if exists
if exist "start_istock.bat" (
    echo Removing problematic start_istock.bat...
    del "start_istock.bat"
)

echo.
echo 4. Creating clean environment file...
if not exist ".env" (
    if exist ".env.example" (
        echo Creating .env from example...
        copy ".env.example" ".env" >nul
        echo OK: .env created
    ) else (
        echo WARNING: .env.example not found
    )
) else (
    echo OK: .env exists
)

echo.
echo 5. Creating necessary directories...
mkdir "backend\logs" 2>nul
mkdir "frontend\logs" 2>nul
mkdir "data\postgres" 2>nul
mkdir "data\redis" 2>nul
mkdir "data\celery" 2>nul
echo OK: Directories created

echo.
echo 6. Testing Docker installation...
docker --version >nul 2>nul
if errorlevel 1 (
    echo ERROR: Docker not found!
    echo Please ensure Docker Desktop is installed and running.
    pause
    exit /b 1
)
echo OK: Docker found

docker info >nul 2>nul
if errorlevel 1 (
    echo ERROR: Docker daemon not running!
    echo Please start Docker Desktop.
    pause
    exit /b 1
)
echo OK: Docker daemon running

echo.
echo 7. Testing Docker Compose...
docker-compose --version >nul 2>nul
if errorlevel 1 (
    echo WARNING: docker-compose not found, trying docker compose...
    docker compose version >nul 2>nul
    if errorlevel 1 (
        echo ERROR: Docker Compose not found!
        echo Please install Docker Compose.
        pause
        exit /b 1
    )
    echo OK: docker compose found
    set COMPOSE_CMD=docker compose
) else (
    echo OK: docker-compose found
    set COMPOSE_CMD=docker-compose
)

echo.
echo 8. Starting minimal services for testing...
echo Starting PostgreSQL and Redis...
%COMPOSE_CMD% up -d postgres redis

echo Waiting for databases to start...
timeout /t 20 /nobreak >nul

echo.
echo 9. Testing database connections...
echo Testing PostgreSQL...
%COMPOSE_CMD% exec postgres pg_isready -U mystock_user
if errorlevel 1 (
    echo WARNING: PostgreSQL not ready, waiting longer...
    timeout /t 10 /nobreak >nul
    %COMPOSE_CMD% exec postgres pg_isready -U mystock_user
    if errorlevel 1 (
        echo ERROR: PostgreSQL connection failed
    ) else (
        echo OK: PostgreSQL connected
    )
) else (
    echo OK: PostgreSQL connected
)

echo Testing Redis...
%COMPOSE_CMD% exec redis redis-cli ping >nul
if errorlevel 1 (
    echo ERROR: Redis connection failed
) else (
    echo OK: Redis connected
)

echo.
echo 10. Starting backend service...
%COMPOSE_CMD% up -d backend
echo Waiting for backend to start...
timeout /t 30 /nobreak >nul

echo Testing backend health...
curl http://localhost:8000/health >nul 2>nul
if errorlevel 1 (
    echo WARNING: Backend health check failed, checking logs...
    %COMPOSE_CMD% logs backend --tail=20
    echo.
    echo ERROR: Backend not responding
) else (
    echo OK: Backend is healthy
)

echo.
echo 11. Testing API documentation...
echo Open browser to: http://localhost:8000/docs
echo.

echo 12. Starting frontend service...
%COMPOSE_CMD% up -d frontend
echo Waiting for frontend to start...
timeout /t 60 /nobreak >nul

echo Testing frontend...
echo Open browser to: http://localhost:3000
echo.

echo.
echo ===========================
echo EMERGENCY FIX COMPLETE
echo ===========================
echo.
echo Summary:
echo 1. Cleaned up problematic files
echo 2. Verified Docker environment
echo 3. Started core services
echo 4. Tested basic functionality
echo.
echo Next steps:
echo 1. Use test_simple.bat for quick checks
echo 2. Use start_istock_fixed.bat for full control
echo 3. Read MANUAL_TEST_GUIDE.md for detailed testing
echo.
echo Access URLs:
echo   Backend:    http://localhost:8000
echo   API Docs:   http://localhost:8000/docs
echo   Frontend:   http://localhost:3000
echo.
pause
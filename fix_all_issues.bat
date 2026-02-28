@echo off
echo iStock Comprehensive Fix Script
echo ===============================
echo.

echo Step 1: Checking current directory...
if not exist "docker-compose.yml" (
    echo ERROR: Not in iStock project directory!
    echo Please navigate to: G:\openclaw\workspace\_system\agent-home\myStock-AI
    pause
    exit /b 1
)
echo OK: In iStock directory
echo.

echo Step 2: Fixing Docker PATH issues...
REM Try to find Docker
where docker >nul 2>nul
if errorlevel 1 (
    echo Docker not in PATH, trying to add...
    
    REM Common Docker installation paths
    if exist "C:\Program Files\Docker\Docker\resources\bin\docker.exe" (
        set "DOCKER_PATH=C:\Program Files\Docker\Docker\resources\bin"
    ) elseif exist "%LOCALAPPDATA%\Docker\resources\bin\docker.exe" (
        set "DOCKER_PATH=%LOCALAPPDATA%\Docker\resources\bin"
    ) else (
        echo ERROR: Could not find Docker executable
        echo Please ensure Docker Desktop is installed and running
        echo See FIX_DOCKER_PATH.md for help
        pause
        exit /b 1
    )
    
    echo Found Docker at: %DOCKER_PATH%
    set "PATH=%DOCKER_PATH%;%PATH%"
) else (
    echo OK: Docker found in PATH
)

echo.
echo Step 3: Testing Docker commands...
docker --version
if errorlevel 1 (
    echo ERROR: Docker command failed
    pause
    exit /b 1
)

docker-compose --version
if errorlevel 1 (
    echo WARNING: docker-compose not found, trying docker compose...
    docker compose version
    if errorlevel 1 (
        echo ERROR: Docker Compose not available
    ) else (
        echo OK: docker compose (plugin) available
    )
) else (
    echo OK: docker-compose available
)

echo.
echo Step 4: Creating minimal frontend (if missing)...
if not exist "frontend\package.json" (
    echo Frontend missing, creating minimal version...
    call create_minimal_frontend.bat
) else (
    echo OK: Frontend package.json exists
)

echo.
echo Step 5: Creating essential directories...
mkdir backend\logs 2>nul
mkdir frontend\logs 2>nul
mkdir data\postgres 2>nul
mkdir data\redis 2>nul
mkdir data\celery 2>nul
echo OK: Directories created

echo.
echo Step 6: Creating .env file if missing...
if not exist ".env" (
    if exist ".env.example" (
        echo Creating .env from example...
        copy ".env.example" ".env" >nul
        echo OK: .env created (modify as needed)
    ) else (
        echo WARNING: .env.example not found
    )
) else (
    echo OK: .env exists
)

echo.
echo Step 7: Stopping any running services...
docker-compose down 2>nul
echo OK: Services stopped

echo.
echo Step 8: Building Docker images...
echo This may take several minutes...
docker-compose build backend
if errorlevel 1 (
    echo ERROR: Failed to build backend image
    echo Check Docker logs and available resources
    pause
    exit /b 1
)
echo OK: Backend image built

echo.
echo Step 9: Starting core services...
docker-compose up -d postgres redis backend
if errorlevel 1 (
    echo ERROR: Failed to start services
    pause
    exit /b 1
)
echo OK: Core services started

echo.
echo Step 10: Waiting for services to be ready...
echo Waiting 30 seconds for services to initialize...
timeout /t 30 /nobreak >nul

echo.
echo Step 11: Testing service health...
echo Testing PostgreSQL...
docker-compose exec postgres pg_isready -U mystock_user
if errorlevel 1 (
    echo WARNING: PostgreSQL not ready yet
) else (
    echo OK: PostgreSQL ready
)

echo Testing Redis...
docker-compose exec redis redis-cli ping >nul
if errorlevel 1 (
    echo WARNING: Redis not responding
) else (
    echo OK: Redis responding
)

echo Testing Backend API...
curl http://localhost:8000/health >nul 2>nul
if errorlevel 1 (
    echo WARNING: Backend not responding yet
    echo Check logs with: docker-compose logs backend
) else (
    echo OK: Backend API responding
)

echo.
echo Step 12: Starting frontend (if available)...
if exist "frontend\package.json" (
    echo Starting frontend service...
    docker-compose up -d frontend
    timeout /t 20 /nobreak >nul
    echo Frontend started (may take time to build)
) else (
    echo SKIP: Frontend not configured
)

echo.
echo ===============================
echo FIX COMPLETE
echo ===============================
echo.
echo Summary:
echo 1. Docker environment: FIXED
echo 2. Frontend structure: CREATED (if missing)
echo 3. Core services: STARTED
echo 4. Health checks: PERFORMED
echo.
echo Access URLs:
echo   Backend API:    http://localhost:8000
echo   API Docs:       http://localhost:8000/docs
echo   Frontend App:   http://localhost:3000 (if available)
echo.
echo Management commands:
echo   Check status:   docker-compose ps
echo   View logs:      docker-compose logs -f
echo   Stop services:  docker-compose down
echo.
echo Next steps:
echo 1. Wait 1-2 minutes for full startup
echo 2. Test: http://localhost:8000/health
echo 3. Test: http://localhost:8000/docs
echo 4. If frontend: http://localhost:3000
echo.
echo For problems:
echo 1. Check logs: docker-compose logs
echo 2. Read: MANUAL_TEST_GUIDE.md
echo 3. Read: FIX_DOCKER_PATH.md
echo.
pause
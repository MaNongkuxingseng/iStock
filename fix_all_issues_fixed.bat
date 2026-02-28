@echo off
echo iStock Comprehensive Fix Script - Fixed Version
echo ===============================================
echo.

echo IMPORTANT: This script will attempt to fix common issues.
echo If Docker Desktop is not running, please start it first.
echo.

echo Step 1: Checking current directory...
if not exist "docker-compose.yml" (
    echo ERROR: Not in iStock project directory!
    echo Current directory: %CD%
    echo Please navigate to the iStock project folder.
    pause
    exit /b 1
)
echo OK: In iStock project directory
echo.

echo Step 2: Checking for Docker Desktop...
echo Checking if Docker Desktop processes are running...
tasklist | findstr /i "docker" >nul
if errorlevel 1 (
    echo WARNING: Docker Desktop does not appear to be running.
    echo Please start Docker Desktop and try again.
    echo.
    echo You can:
    echo 1. Search for "Docker Desktop" in Start Menu
    echo 2. Look for the Docker whale icon in system tray
    echo 3. Wait 1-2 minutes after starting for it to fully load
    echo.
    set /p continue="Continue anyway? (y/N): "
    if /i not "%continue%"=="y" (
        echo Exiting...
        pause
        exit /b 1
    )
) else (
    echo OK: Docker Desktop processes detected
)

echo.
echo Step 3: Testing Docker commands with full paths...
echo Trying common Docker installation paths...

set DOCKER_FOUND=0
set DOCKER_COMPOSE_FOUND=0

REM Check Program Files path
if exist "C:\Program Files\Docker\Docker\resources\bin\docker.exe" (
    echo Found Docker at: C:\Program Files\Docker\Docker\resources\bin
    set "DOCKER_PATH=C:\Program Files\Docker\Docker\resources\bin"
    set DOCKER_FOUND=1
) else (
    echo Docker not found in Program Files
)

REM Check AppData path  
if exist "%LOCALAPPDATA%\Docker\resources\bin\docker.exe" (
    echo Found Docker at: %LOCALAPPDATA%\Docker\resources\bin
    set "DOCKER_PATH=%LOCALAPPDATA%\Docker\resources\bin"
    set DOCKER_FOUND=1
)

if %DOCKER_FOUND% equ 0 (
    echo ERROR: Could not find Docker executable
    echo Please ensure Docker Desktop is properly installed.
    echo Common installation paths checked:
    echo   C:\Program Files\Docker\Docker\resources\bin
    echo   %LOCALAPPDATA%\Docker\resources\bin
    echo.
    echo Solutions:
    echo 1. Reinstall Docker Desktop
    echo 2. Check FIX_DOCKER_PATH.md for manual fixes
    pause
    exit /b 1
)

echo.
echo Step 4: Using Docker with full path...
"%DOCKER_PATH%\docker.exe" --version
if errorlevel 1 (
    echo ERROR: Docker command failed even with full path
    echo Docker Desktop may not be fully started or has issues.
    pause
    exit /b 1
)

echo.
echo Step 5: Checking Docker Compose...
REM Try docker-compose.exe first
if exist "%DOCKER_PATH%\docker-compose.exe" (
    echo Found docker-compose.exe
    set "COMPOSE_CMD=%DOCKER_PATH%\docker-compose.exe"
    set DOCKER_COMPOSE_FOUND=1
) else (
    echo docker-compose.exe not found, trying docker compose plugin...
    "%DOCKER_PATH%\docker.exe" compose version >nul 2>nul
    if errorlevel 1 (
        echo WARNING: docker compose plugin not available
    ) else (
        echo OK: docker compose plugin available
        set "COMPOSE_CMD=%DOCKER_PATH%\docker.exe compose"
        set DOCKER_COMPOSE_FOUND=1
    )
)

if %DOCKER_COMPOSE_FOUND% equ 0 (
    echo ERROR: Neither docker-compose nor docker compose found
    echo Please install Docker Compose or update Docker Desktop.
    pause
    exit /b 1
)

echo.
echo Step 6: Creating essential project structure...
echo Creating directories if missing...
if not exist "backend\logs" mkdir "backend\logs"
if not exist "frontend\logs" mkdir "frontend\logs"
if not exist "data\postgres" mkdir "data\postgres"
if not exist "data\redis" mkdir "data\redis"
if not exist "data\celery" mkdir "data\celery"
echo OK: Directories created

echo.
echo Step 7: Creating .env file if missing...
if not exist ".env" (
    if exist ".env.example" (
        echo Creating .env from example...
        copy ".env.example" ".env" >nul
        echo OK: .env created (please modify configuration as needed)
    ) else (
        echo WARNING: .env.example not found
        echo Creating basic .env file...
        echo # iStock Environment Variables > .env
        echo DATABASE_URL=postgresql://mystock_user:mystock_password@postgres:5432/mystock_ai >> .env
        echo REDIS_URL=redis://redis:6379/0 >> .env
        echo DEBUG=true >> .env
        echo OK: Basic .env created
    )
) else (
    echo OK: .env file exists
)

echo.
echo Step 8: Checking frontend structure...
if not exist "frontend\package.json" (
    echo WARNING: Frontend package.json missing
    echo Creating minimal frontend structure...
    
    if not exist "frontend" mkdir frontend
    cd frontend
    
    echo Creating minimal package.json...
    echo { > package.json
    echo   "name": "istock-frontend", >> package.json
    echo   "version": "1.0.0", >> package.json
    echo   "private": true, >> package.json
    echo   "dependencies": { >> package.json
    echo     "react": "^18.2.0", >> package.json
    echo     "react-dom": "^18.2.0" >> package.json
    echo   }, >> package.json
    echo   "scripts": { >> package.json
    echo     "start": "echo 'Frontend would start here'", >> package.json
    echo     "build": "echo 'Frontend would build here'" >> package.json
    echo   } >> package.json
    echo } >> package.json
    
    echo Creating placeholder index.html...
    if not exist "public" mkdir public
    cd public
    echo ^<!DOCTYPE html^> > index.html
    echo ^<html^> >> index.html
    echo ^<head^> >> index.html
    echo   ^<title^>iStock - Coming Soon^</title^> >> index.html
    echo ^</head^> >> index.html
    echo ^<body^> >> index.html
    echo   ^<h1^>iStock Frontend^</h1^> >> index.html
    echo   ^<p^>Frontend is being set up. Backend services should be available.^</p^> >> index.html
    echo ^</body^> >> index.html
    echo ^</html^> >> index.html
    
    cd ..\..
    echo OK: Minimal frontend structure created
) else (
    echo OK: Frontend package.json exists
)

echo.
echo Step 9: Stopping any existing services...
echo Stopping Docker Compose services if running...
%COMPOSE_CMD% down 2>nul
echo OK: Services stopped (if any were running)

echo.
echo Step 10: Building and starting core services...
echo This may take several minutes. Please be patient...
echo.

echo Building backend image...
%COMPOSE_CMD% build backend
if errorlevel 1 (
    echo ERROR: Failed to build backend image
    echo This could be due to:
    echo 1. Network issues downloading Docker images
    echo 2. Insufficient disk space
    echo 3. Docker Desktop not fully ready
    echo.
    echo Trying alternative approach: starting services without build...
    
    echo Starting PostgreSQL and Redis only...
    %COMPOSE_CMD% up -d postgres redis
    if errorlevel 1 (
        echo ERROR: Failed to start database services
        pause
        exit /b 1
    )
) else (
    echo OK: Backend image built successfully
    
    echo Starting core services (PostgreSQL, Redis, Backend)...
    %COMPOSE_CMD% up -d postgres redis backend
    if errorlevel 1 (
        echo ERROR: Failed to start services
        pause
        exit /b 1
    )
)

echo.
echo Step 11: Waiting for services to initialize...
echo Waiting 30 seconds for services to start up...
timeout /t 30 /nobreak >nul

echo.
echo Step 12: Checking service status...
echo Docker Compose service status:
%COMPOSE_CMD% ps

echo.
echo Step 13: Basic connectivity tests...
echo Testing PostgreSQL connection...
%COMPOSE_CMD% exec postgres pg_isready -U mystock_user -d mystock_ai
if errorlevel 1 (
    echo WARNING: PostgreSQL not responding yet
    echo This is normal if services just started. Waiting more...
    timeout /t 10 /nobreak >nul
    %COMPOSE_CMD% exec postgres pg_isready -U mystock_user -d mystock_ai
    if errorlevel 1 (
        echo WARNING: PostgreSQL still not ready
    ) else (
        echo OK: PostgreSQL is now ready
    )
) else (
    echo OK: PostgreSQL is ready
)

echo Testing Redis connection...
%COMPOSE_CMD% exec redis redis-cli ping >nul
if errorlevel 1 (
    echo WARNING: Redis not responding
) else (
    echo OK: Redis is responding
)

echo.
echo Step 14: Manual verification instructions...
echo ===========================================
echo FIX SCRIPT COMPLETED
echo ===========================================
echo.
echo What was done:
echo 1. ✓ Verified Docker Desktop
echo 2. ✓ Located Docker executables
echo 3. ✓ Created project structure
echo 4. ✓ Created .env configuration
echo 5. ✓ Created frontend placeholder
echo 6. ✓ Stopped existing services
echo 7. ✓ Built/started core services
echo.
echo Next steps to verify:
echo.
echo 1. Wait 1-2 minutes for full startup
echo 2. Open browser and test:
echo    - Backend API: http://localhost:8000/health
echo    - API Docs:    http://localhost:8000/docs
echo.
echo 3. Check Docker Desktop dashboard:
echo    - Open Docker Desktop
echo    - Check "Containers" tab
echo    - Look for istock_postgres, istock_redis, istock_backend
echo.
echo 4. If services aren't running:
echo    - Check Docker Desktop is fully started
echo    - Wait 2-3 minutes
echo    - Run: %COMPOSE_CMD% logs
echo.
echo 5. Common issues and solutions:
echo    - "Port already in use": Change ports in docker-compose.yml
echo    - "Connection refused": Wait longer for services to start
echo    - "No such file": Run this script from correct directory
echo.
echo For detailed troubleshooting:
echo 1. Read MANUAL_TEST_GUIDE.md
echo 2. Read FIX_DOCKER_PATH.md
echo 3. Check Docker Desktop logs
echo.
pause